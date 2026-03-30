import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Assuming marriage_cert_final is in your current directory
try:
    from marriage_cert_final import generate_full_certificate
except ImportError:
    generate_full_certificate = None

class MarriageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Municipal Form No. 97 - Digital Registry")
        
        # 1. Setup Scrollable Canvas
        canvas_width = 800
        canvas_height = 900
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.v_scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        
        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # 2. Load and Set the Form Background Image
        try:
            self.img = Image.open("form.jpg")
            self.img = self.img.resize((780, 1150), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
            self.canvas.config(scrollregion=(0, 0, 800, 1300))
        except FileNotFoundError:
            print("Error: Background image not found. Ensure 'form.jpg' is in the folder.")

        # --- DYNAMIC UI STATE ---
        self.active_check_btn = None
        self.active_check_window = None

        # --- HELPER: Style and Logic ---
        def apply_style(entry_widget):
            entry_widget.is_locked = False # Custom property to track state
            entry_widget.config(
                bg="#ADD8E6", relief="flat", highlightthickness=1,
                highlightbackground="gray", highlightcolor="black",
                bd=0, font=("Helvetica", 8)
            )
            # Bind click event to show the check icon
            entry_widget.bind("<FocusIn>", lambda e: self.position_check_icon(entry_widget))

        # --- 3. Floating Entry Fields ---
        
        # Header Info
        self.ent_prov = tk.Entry(root, width=25); apply_style(self.ent_prov)
        self.canvas.create_window(240, 95, window=self.ent_prov)

        self.ent_city = tk.Entry(root, width=25); apply_style(self.ent_city)
        self.canvas.create_window(270, 113, window=self.ent_city)

        # Section 1: Names (Husband)
        self.ent_h_first = tk.Entry(root, width=30); apply_style(self.ent_h_first)
        self.canvas.create_window(300, 142, window=self.ent_h_first)
        self.ent_h_mid = tk.Entry(root, width=30); apply_style(self.ent_h_mid)
        self.canvas.create_window(300, 157, window=self.ent_h_mid)
        self.ent_h_last = tk.Entry(root, width=30); apply_style(self.ent_h_last)
        self.canvas.create_window(300, 172, window=self.ent_h_last)

        # Section 1: Names (Wife)
        self.ent_w_first = tk.Entry(root, width=30); apply_style(self.ent_w_first)
        self.canvas.create_window(600, 142, window=self.ent_w_first)
        self.ent_w_mid = tk.Entry(root, width=30); apply_style(self.ent_w_mid)
        self.canvas.create_window(600, 157, window=self.ent_w_mid)
        self.ent_w_last = tk.Entry(root, width=30); apply_style(self.ent_w_last)
        self.canvas.create_window(600, 172, window=self.ent_w_last)

        # Section 2: Birth Info (Husband)
        self.ent_h_day = tk.Entry(root, width=4); apply_style(self.ent_h_day)
        self.canvas.create_window(195, 197, window=self.ent_h_day)
        self.ent_h_month = tk.Entry(root, width=10); apply_style(self.ent_h_month)
        self.canvas.create_window(270, 197, window=self.ent_h_month)
        self.ent_h_year = tk.Entry(root, width=6); apply_style(self.ent_h_year)
        self.canvas.create_window(347, 198, window=self.ent_h_year)
        self.ent_h_age = tk.Entry(root, width=4); apply_style(self.ent_h_age)
        self.canvas.create_window(430, 198, window=self.ent_h_age)

        # Section 2: Birth Info (Wife)
        self.ent_w_day = tk.Entry(root, width=4); apply_style(self.ent_w_day)
        self.canvas.create_window(490, 199, window=self.ent_w_day)
        self.ent_w_month = tk.Entry(root, width=10); apply_style(self.ent_w_month)
        self.canvas.create_window(565, 199, window=self.ent_w_month)
        self.ent_w_year = tk.Entry(root, width=6); apply_style(self.ent_w_year)
        self.canvas.create_window(640, 199, window=self.ent_w_year)
        self.ent_w_age = tk.Entry(root, width=4); apply_style(self.ent_w_age)
        self.canvas.create_window(725, 199, window=self.ent_w_age)

        # 4. Generate Button
        self.btn = tk.Button(root, text="PRINT TO PDF", bg="#27ae60", fg="white", 
                             font=("Arial", 11, "bold"), command=self.print_pdf)
        self.canvas.create_window(400, 1200, window=self.btn)

    # --- UI INTERACTION LOGIC ---

    def position_check_icon(self, widget):
        """Moves the check button to the active entry field safely."""
        # Force geometry calculations so width is accurate
        self.root.update_idletasks()

        if self.active_check_window:
            self.canvas.delete(self.active_check_window)

        btn_text = "✎" if widget.is_locked else "✔"
        btn_bg = "#f39c12" if widget.is_locked else "#27ae60"
        
        self.active_check_btn = tk.Button(self.root, text=btn_text, bg=btn_bg, fg="white",
                                          font=("Arial", 7, "bold"), bd=1,
                                          command=lambda: self.toggle_field_state(widget))
        
        # Safe loop: Only check items that are Canvas 'windows'
        for item in self.canvas.find_all():
            if self.canvas.type(item) == "window":
                if self.canvas.itemcget(item, "window") == str(widget):
                    x, y = self.canvas.coords(item)
                    width = widget.winfo_width() / 2
                    self.active_check_window = self.canvas.create_window(x + width + 15, y, window=self.active_check_btn)
                    break

    def toggle_field_state(self, widget):
        """Toggles between Blue (Edit) and White (Transparent/Locked) mode."""
        if not widget.is_locked:
            widget.config(bg="white", highlightthickness=0)
            widget.is_locked = True
        else:
            widget.config(bg="#ADD8E6", highlightthickness=1)
            widget.is_locked = False
        
        self.position_check_icon(widget)

    def print_pdf(self):
        data = {
            'province': self.ent_prov.get().upper(),
            'city_municipality': self.ent_city.get().upper(),
            'h_first': self.ent_h_first.get().upper(),
            'h_day': self.ent_h_day.get(),
            'h_month': self.ent_h_month.get(),
            'h_year': self.ent_h_year.get(),
            'h_age': self.ent_h_age.get(),
            'show_template': False 
        }
        
        if generate_full_certificate:
            try:
                generate_full_certificate("Marriage_Output.pdf", data, show_template=False)
                messagebox.showinfo("Success", "Generated PDF successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "PDF generator module not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarriageApp(root)
    root.mainloop()