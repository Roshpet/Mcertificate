import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os 
import win32api 
import win32print

# Assuming marriage_cert_final is in your current directory
try:
    from marriage_cert_final import generate_full_certificate
except ImportError:
    generate_full_certificate = None

class MarriageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Municipal Form No. 97 - Digital Registry")
        
        # --- 1. NAVIGATION BAR ---
        self.nav_bar = tk.Frame(root, bg="#2c3e50")
        self.nav_bar.pack(side="top", fill="x")

        self.btn_p1 = tk.Button(self.nav_bar, text="PAGE 1", command=lambda: self.show_page(1), bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        self.btn_p1.pack(side="left", padx=10, pady=5)

        self.btn_p2 = tk.Button(self.nav_bar, text="PAGE 2", command=lambda: self.show_page(2), bg="#34495e", fg="white", font=("Arial", 10, "bold"))
        self.btn_p2.pack(side="left", padx=10, pady=5)
        
        # 2. Setup Scrollable Canvas
        canvas_width = 800
        canvas_height = 850
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.v_scroll = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)
        
        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- DYNAMIC UI STATE ---
        self.active_check_btn = None
        self.active_check_window = None
        
        # FIXED: Initialize with 0 so NO checkbox is selected by default
        self.settlement_var = tk.IntVar(value=0) 
        self.license_type_var = tk.IntVar(value=0)
        self.affidavit_lic_var = tk.IntVar(value=0) 

        # Start on Page 1
        self.show_page(1)

    def show_page(self, page_num):
        """Clears the canvas and redraws the requested page."""
        self.canvas.delete("all")
        if page_num == 1:
            self.load_page_one()
        elif page_num == 2:
            self.load_page_two()

    def apply_style(self, entry_widget):
        entry_widget.is_locked = False 
        entry_widget.config(bg="#ADD8E6", relief="flat", highlightthickness=1,
                            highlightbackground="gray", highlightcolor="black",
                            bd=0, font=("Helvetica", 8))

        # --- FORCE UPPERCASE WHILE TYPING ---
        def force_upper(*args):
            current_text = entry_widget.get()
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, current_text.upper())

        var = tk.StringVar()
        entry_widget.config(textvariable=var)
        var.trace_add("write", force_upper)

        entry_widget.bind("<FocusIn>", lambda e: self.position_check_icon(entry_widget))

    def update_section_18_names(self, event=None):
        """Automatically updates Section 18 based on Section 1 inputs."""
        h_full = f"{self.ent_h_first.get()} {self.ent_h_mid.get()} {self.ent_h_last.get()}".strip().upper()
        h_full = " ".join(h_full.split())
        self.ent_s18_hname.delete(0, tk.END)
        self.ent_s18_hname.insert(0, h_full)

        w_full = f"{self.ent_w_first.get()} {self.ent_w_mid.get()} {self.ent_w_last.get()}".strip().upper()
        w_full = " ".join(w_full.split())
        self.ent_s18_wname.delete(0, tk.END)
        self.ent_s18_wname.insert(0, w_full)

    def load_page_one(self):
        try:
            self.img = Image.open("form.jpg")
            self.img = self.img.resize((780, 1150), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
            self.canvas.config(scrollregion=(0, 0, 800, 1500)) 
        except FileNotFoundError:
            print("Error: form.jpg not found.")

        # --- PAGE 1 FIELDS ---
        self.ent_prov = tk.Entry(self.root, width=25); self.apply_style(self.ent_prov); self.canvas.create_window(240, 95, window=self.ent_prov)
        self.ent_city = tk.Entry(self.root, width=25); self.apply_style(self.ent_city); self.canvas.create_window(270, 113, window=self.ent_city)

        self.ent_h_first = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_first); self.canvas.create_window(300, 142, window=self.ent_h_first)
        self.ent_h_mid = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_mid); self.canvas.create_window(300, 157, window=self.ent_h_mid)
        self.ent_h_last = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_last); self.canvas.create_window(300, 172, window=self.ent_h_last)
        
        self.ent_w_first = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_first); self.canvas.create_window(600, 142, window=self.ent_w_first)
        self.ent_w_mid = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_mid); self.canvas.create_window(600, 157, window=self.ent_w_mid)
        self.ent_w_last = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_last); self.canvas.create_window(600, 172, window=self.ent_w_last)
        
        self.ent_s18_hname = tk.Entry(self.root, width=35); self.apply_style(self.ent_s18_hname); self.canvas.create_window(365, 610, window=self.ent_s18_hname)
        self.ent_s18_wname = tk.Entry(self.root, width=35); self.apply_style(self.ent_s18_wname); self.canvas.create_window(600, 610, window=self.ent_s18_wname)

        for entry in [self.ent_h_first, self.ent_h_mid, self.ent_h_last, self.ent_w_first, self.ent_w_mid, self.ent_w_last]:
            entry.bind("<KeyRelease>", self.update_section_18_names)

        self.ent_h_day = tk.Entry(self.root, width=4); self.apply_style(self.ent_h_day); self.canvas.create_window(195, 197, window=self.ent_h_day)
        self.ent_h_month = tk.Entry(self.root, width=10); self.apply_style(self.ent_h_month); self.canvas.create_window(270, 197, window=self.ent_h_month)
        self.ent_h_year = tk.Entry(self.root, width=6); self.apply_style(self.ent_h_year); self.canvas.create_window(347, 198, window=self.ent_h_year)
        self.ent_h_age = tk.Entry(self.root, width=4); self.apply_style(self.ent_h_age); self.canvas.create_window(430, 198, window=self.ent_h_age)
        self.ent_w_day = tk.Entry(self.root, width=4); self.apply_style(self.ent_w_day); self.canvas.create_window(490, 199, window=self.ent_w_day)
        self.ent_w_month = tk.Entry(self.root, width=10); self.apply_style(self.ent_w_month); self.canvas.create_window(565, 199, window=self.ent_w_month)
        self.ent_w_year = tk.Entry(self.root, width=6); self.apply_style(self.ent_w_year); self.canvas.create_window(640, 199, window=self.ent_w_year)
        self.ent_w_age = tk.Entry(self.root, width=4); self.apply_style(self.ent_w_age); self.canvas.create_window(725, 199, window=self.ent_w_age)
        
        self.ent_h_pob_city = tk.Entry(self.root, width=15); self.apply_style(self.ent_h_pob_city); self.canvas.create_window(205, 228, window=self.ent_h_pob_city)
        self.ent_h_pob_prov = tk.Entry(self.root, width=15); self.apply_style(self.ent_h_pob_prov); self.canvas.create_window(315, 228, window=self.ent_h_pob_prov)
        self.ent_h_pob_ctry = tk.Entry(self.root, width=10); self.apply_style(self.ent_h_pob_ctry); self.canvas.create_window(410, 228, window=self.ent_h_pob_ctry)
        self.ent_w_pob_city = tk.Entry(self.root, width=15); self.apply_style(self.ent_w_pob_city); self.canvas.create_window(505, 228, window=self.ent_w_pob_city)
        self.ent_w_pob_prov = tk.Entry(self.root, width=15); self.apply_style(self.ent_w_pob_prov); self.canvas.create_window(615, 228, window=self.ent_w_pob_prov)
        self.ent_w_pob_ctry = tk.Entry(self.root, width=10); self.apply_style(self.ent_w_pob_ctry); self.canvas.create_window(710, 228, window=self.ent_w_pob_ctry)
        
        self.ent_h_sex = tk.Entry(self.root, width=10); self.apply_style(self.ent_h_sex); self.canvas.create_window(200, 254, window=self.ent_h_sex)
        self.ent_h_citizen = tk.Entry(self.root, width=20); self.apply_style(self.ent_h_citizen); self.canvas.create_window(330, 255, window=self.ent_h_citizen)
        self.ent_w_sex = tk.Entry(self.root, width=10); self.apply_style(self.ent_w_sex); self.canvas.create_window(500, 255, window=self.ent_w_sex)
        self.ent_w_citizen = tk.Entry(self.root, width=20); self.apply_style(self.ent_w_citizen); self.canvas.create_window(625, 257, window=self.ent_w_citizen)
        
        self.ent_h_res = tk.Entry(self.root, width=45); self.apply_style(self.ent_h_res); self.canvas.create_window(295, 287, window=self.ent_h_res)
        self.ent_w_res = tk.Entry(self.root, width=45); self.apply_style(self.ent_w_res); self.canvas.create_window(595, 288, window=self.ent_w_res)
        
        self.ent_h_rel = tk.Entry(self.root, width=35); self.apply_style(self.ent_h_rel); self.canvas.create_window(265, 310, window=self.ent_h_rel)
        self.ent_w_rel = tk.Entry(self.root, width=35); self.apply_style(self.ent_w_rel); self.canvas.create_window(565, 310, window=self.ent_w_rel)
        self.ent_h_status = tk.Entry(self.root, width=35); self.apply_style(self.ent_h_status); self.canvas.create_window(265, 333, window=self.ent_h_status)
        self.ent_w_status = tk.Entry(self.root, width=35); self.apply_style(self.ent_w_status); self.canvas.create_window(565, 335, window=self.ent_w_status)
        self.ent_hf_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_hf_first); self.canvas.create_window(210, 361, window=self.ent_hf_first)
        self.ent_hf_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_hf_mid); self.canvas.create_window(305, 361, window=self.ent_hf_mid)
        self.ent_hf_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_hf_last); self.canvas.create_window(400, 361, window=self.ent_hf_last)
        self.ent_wf_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_wf_first); self.canvas.create_window(508, 363, window=self.ent_wf_first)
        self.ent_wf_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_wf_mid); self.canvas.create_window(603, 363, window=self.ent_wf_mid)
        self.ent_wf_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_wf_last); self.canvas.create_window(698, 363, window=self.ent_wf_last)
        self.ent_hf_citizen = tk.Entry(self.root, width=30); self.apply_style(self.ent_hf_citizen); self.canvas.create_window(305, 384, window=self.ent_hf_citizen)
        self.ent_wf_citizen = tk.Entry(self.root, width=30); self.apply_style(self.ent_wf_citizen); self.canvas.create_window(605, 386, window=self.ent_wf_citizen)
        self.ent_hm_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_hm_first); self.canvas.create_window(210, 414, window=self.ent_hm_first)
        self.ent_hm_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_hm_mid); self.canvas.create_window(305, 414, window=self.ent_hm_mid)
        self.ent_hm_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_hm_last); self.canvas.create_window(400, 414, window=self.ent_hm_last)
        self.ent_wm_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_wm_first); self.canvas.create_window(508, 416, window=self.ent_wm_first)
        self.ent_wm_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_wm_mid); self.canvas.create_window(603, 416, window=self.ent_wm_mid)
        self.ent_wm_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_wm_last); self.canvas.create_window(698, 416, window=self.ent_wm_last)
        self.ent_hm_citizen = tk.Entry(self.root, width=30); self.apply_style(self.ent_hm_citizen); self.canvas.create_window(305, 439, window=self.ent_hm_citizen)
        self.ent_wm_citizen = tk.Entry(self.root, width=30); self.apply_style(self.ent_wm_citizen); self.canvas.create_window(605, 440, window=self.ent_wm_citizen)
        self.ent_h_c_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_h_c_first); self.canvas.create_window(210, 470, window=self.ent_h_c_first)
        self.ent_h_c_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_h_c_mid); self.canvas.create_window(305, 470, window=self.ent_h_c_mid)
        self.ent_h_c_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_h_c_last); self.canvas.create_window(400, 470, window=self.ent_h_c_last)
        self.ent_w_c_first = tk.Entry(self.root, width=15); self.apply_style(self.ent_w_c_first); self.canvas.create_window(508, 471, window=self.ent_w_c_first)
        self.ent_w_c_mid = tk.Entry(self.root, width=15); self.apply_style(self.ent_w_c_mid); self.canvas.create_window(603, 471, window=self.ent_w_c_mid)
        self.ent_w_c_last = tk.Entry(self.root, width=15); self.apply_style(self.ent_w_c_last); self.canvas.create_window(698, 471, window=self.ent_w_c_last)
        self.ent_h_c_rel = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_c_rel); self.canvas.create_window(305, 491, window=self.ent_h_c_rel)
        self.ent_w_c_rel = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_c_rel); self.canvas.create_window(605, 492, window=self.ent_w_c_rel)
        self.ent_h_c_res = tk.Entry(self.root, width=45); self.apply_style(self.ent_h_c_res); self.canvas.create_window(305, 521, window=self.ent_h_c_res)
        self.ent_w_c_res = tk.Entry(self.root, width=45); self.apply_style(self.ent_w_c_res); self.canvas.create_window(605, 522, window=self.ent_w_c_res)
        self.ent_pom_office = tk.Entry(self.root, width=40); self.apply_style(self.ent_pom_office); self.canvas.create_window(310, 541, window=self.ent_pom_office)
        self.ent_pom_city = tk.Entry(self.root, width=18); self.apply_style(self.ent_pom_city); self.canvas.create_window(510, 541, window=self.ent_pom_city)
        self.ent_pom_prov = tk.Entry(self.root, width=18); self.apply_style(self.ent_pom_prov); self.canvas.create_window(660, 541, window=self.ent_pom_prov)
        self.ent_dom_day = tk.Entry(self.root, width=5); self.apply_style(self.ent_dom_day); self.canvas.create_window(230, 570, window=self.ent_dom_day)
        self.ent_dom_month = tk.Entry(self.root, width=12); self.apply_style(self.ent_dom_month); self.canvas.create_window(295, 570, window=self.ent_dom_month)
        self.ent_dom_year = tk.Entry(self.root, width=8); self.apply_style(self.ent_dom_year); self.canvas.create_window(375, 570, window=self.ent_dom_year)
        self.ent_tom = tk.Entry(self.root, width=15); self.apply_style(self.ent_tom); self.canvas.create_window(630, 570, window=self.ent_tom)

        # Section 18 Checkboxes & Signatures
        self.chk_entered = tk.Checkbutton(self.root, variable=self.settlement_var, onvalue=1, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(304, 639, window=self.chk_entered)
        self.chk_not_entered = tk.Checkbutton(self.root, variable=self.settlement_var, onvalue=2, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(544, 639, window=self.chk_not_entered)
        self.ent_s18_sig_day = tk.Entry(self.root, width=5); self.apply_style(self.ent_s18_sig_day); self.canvas.create_window(590, 650, window=self.ent_s18_sig_day)
        self.ent_s18_sig_month = tk.Entry(self.root, width=15); self.apply_style(self.ent_s18_sig_month); self.canvas.create_window(690, 650, window=self.ent_s18_sig_month)
        
        # Section 19
        self.chk_lic_a = tk.Checkbutton(self.root, variable=self.license_type_var, onvalue=1, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 737, window=self.chk_lic_a)
        self.ent_lic_no = tk.Entry(self.root, width=23); self.apply_style(self.ent_lic_no); self.canvas.create_window(280, 739, window=self.ent_lic_no)
        self.ent_lic_issued_on = tk.Entry(self.root, width=23); self.apply_style(self.ent_lic_issued_on); self.canvas.create_window(470, 739, window=self.ent_lic_issued_on)
        self.ent_lic_issued_at = tk.Entry(self.root, width=28); self.apply_style(self.ent_lic_issued_at); self.canvas.create_window(650, 739, window=self.ent_lic_issued_at)
        self.chk_lic_b = tk.Checkbutton(self.root, variable=self.license_type_var, onvalue=2, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 761, window=self.chk_lic_b)
        self.ent_lic_art = tk.Entry(self.root, width=5); self.apply_style(self.ent_lic_art); self.canvas.create_window(475, 760, window=self.ent_lic_art)
        self.chk_lic_c = tk.Checkbutton(self.root, variable=self.license_type_var, onvalue=3, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 783, window=self.chk_lic_c)
        self.ent_off_name = tk.Entry(self.root, width=35); self.apply_style(self.ent_off_name); self.canvas.create_window(188, 805, window=self.ent_off_name)
        self.ent_off_pos = tk.Entry(self.root, width=25); self.apply_style(self.ent_off_pos); self.canvas.create_window(405, 805, window=self.ent_off_pos)
        self.ent_if_app = tk.Entry(self.root, width=35); self.apply_style(self.ent_if_app); self.canvas.create_window(620, 805, window=self.ent_if_app)
        
        # Section 20: Witnesses
        self.ent_wit1 = tk.Entry(self.root, width=25); self.apply_style(self.ent_wit1); self.canvas.create_window(155, 865, window=self.ent_wit1)
        self.ent_wit2 = tk.Entry(self.root, width=25); self.apply_style(self.ent_wit2); self.canvas.create_window(665, 865, window=self.ent_wit2)
        self.ent_wit3 = tk.Entry(self.root, width=25); self.apply_style(self.ent_wit3); self.canvas.create_window(328, 865, window=self.ent_wit3)
        self.ent_wit4 = tk.Entry(self.root, width=25); self.apply_style(self.ent_wit4); self.canvas.create_window(500, 865, window=self.ent_wit4)

        # PAGE 1 PRINT BUTTON
        self.btn_print_p1 = tk.Button(self.root, text="PRINT PAGE 1 ONLY", bg="#27ae60", fg="white", 
                                      font=("Arial", 11, "bold"), command=self.print_pdf_p1)
        self.canvas.create_window(400, 1200, window=self.btn_print_p1)

    def load_page_two(self):
        try:
            self.img2 = Image.open("form_page2.png")
            self.img2 = self.img2.resize((780, 1150), Image.Resampling.LANCZOS)
            self.bg_img2 = ImageTk.PhotoImage(self.img2)
            self.canvas.create_image(0, 0, image=self.bg_img2, anchor="nw")
            self.canvas.config(scrollregion=(0, 0, 800, 1500))
        except FileNotFoundError:
            self.canvas.create_text(400, 200, text="Please upload form_page2.png", font=("Arial", 14))

        # --- PAGE 2 WITNESSES ---
        self.ent_p2_wit1 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit1); self.canvas.create_window(124, 65, window=self.ent_p2_wit1)
        self.ent_p2_wit2 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit2); self.canvas.create_window(290, 65, window=self.ent_p2_wit2)
        self.ent_p2_wit3 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit3); self.canvas.create_window(469, 65, window=self.ent_p2_wit3)
        self.ent_p2_wit4 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit4); self.canvas.create_window(636, 65, window=self.ent_p2_wit4)
        self.ent_p2_wit5 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit5); self.canvas.create_window(124, 100, window=self.ent_p2_wit5)
        self.ent_p2_wit6 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit6); self.canvas.create_window(290, 100, window=self.ent_p2_wit6)
        self.ent_p2_wit7 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit7); self.canvas.create_window(469, 100, window=self.ent_p2_wit7)
        self.ent_p2_wit8 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit8); self.canvas.create_window(636, 100, window=self.ent_p2_wit8)

        # PAGE 2 PRINT BUTTON
        self.btn_print_p2 = tk.Button(self.root, text="PRINT PAGE 2 ONLY", bg="#e67e22", fg="white", 
                                      font=("Arial", 11, "bold"), command=self.print_pdf_p2)
        self.canvas.create_window(400, 1200, window=self.btn_print_p2)

    def position_check_icon(self, widget):
        self.root.update_idletasks()
        if self.active_check_window:
            self.canvas.delete(self.active_check_window)
        btn_text = "✎" if widget.is_locked else "✔"
        btn_bg = "#f39c12" if widget.is_locked else "#27ae60"
        self.active_check_btn_ui = tk.Button(self.root, text=btn_text, bg=btn_bg, fg="white",
                                          font=("Arial", 7, "bold"), bd=1,
                                          command=lambda: self.toggle_field_state(widget))
        for item in self.canvas.find_all():
            if self.canvas.type(item) == "window" and self.canvas.itemcget(item, "window") == str(widget):
                x, y = self.canvas.coords(item)
                self.active_check_window = self.canvas.create_window(x + (widget.winfo_width() / 2) + 15, y, window=self.active_check_btn_ui)
                break

    def toggle_field_state(self, widget):
        widget.config(bg="white" if not widget.is_locked else "#ADD8E6", highlightthickness=0 if not widget.is_locked else 1)
        widget.is_locked = not widget.is_locked
        self.position_check_icon(widget)

    def print_pdf_p1(self):
        lic_type = {1: 'a', 2: 'b', 3: 'c'}.get(self.license_type_var.get(), '')
        data = {
            'page': 1, 
            'province': self.ent_prov.get().upper(),
            'city_municipality': self.ent_city.get().upper(),

            'h_first': self.ent_h_first.get().upper(),
            'h_middle': self.ent_h_mid.get().upper(),
            'h_last': self.ent_h_last.get().upper(),
            'h_day': self.ent_h_day.get(),
            'h_month': self.ent_h_month.get().upper(),
            'h_year': self.ent_h_year.get(),
            'h_age': self.ent_h_age.get(),
            'h_pob_city': self.ent_h_pob_city.get().upper(),
            'h_pob_prov': self.ent_h_pob_prov.get().upper(),
            'h_pob_ctry': self.ent_h_pob_ctry.get().upper(),
            'h_sex': self.ent_h_sex.get().upper(),
            'h_citizen': self.ent_h_citizen.get().upper(),
            'h_res': self.ent_h_res.get().upper(),
            'h_rel': self.ent_h_rel.get().upper(),
            'h_status': self.ent_h_status.get().upper(),
            'hf_first': self.ent_hf_first.get().upper(),
            'hf_mid': self.ent_hf_mid.get().upper(),
            'hf_last': self.ent_hf_last.get().upper(),
            'hf_citizen': self.ent_hf_citizen.get().upper(),
            'hm_first': self.ent_hm_first.get().upper(),
            'hm_mid': self.ent_hm_mid.get().upper(),
            'hm_last': self.ent_hm_last.get().upper(),
            'hm_citizen': self.ent_hm_citizen.get().upper(),
            'h_c_first': self.ent_h_c_first.get().upper(),
            'h_c_mid': self.ent_h_c_mid.get().upper(),
            'h_c_last': self.ent_h_c_last.get().upper(),
            'h_c_rel': self.ent_h_c_rel.get().upper(),
            'h_c_res': self.ent_h_c_res.get().upper(),

            'w_first': self.ent_w_first.get().upper(),
            'w_middle': self.ent_w_mid.get().upper(),
            'w_last': self.ent_w_last.get().upper(),
            'w_pob_city': self.ent_w_pob_city.get().upper(),
            'w_pob_prov': self.ent_w_pob_prov.get().upper(),
            'w_pob_ctry': self.ent_w_pob_ctry.get().upper(),
            'w_day': self.ent_w_day.get(),
            'w_month': self.ent_w_month.get().upper(),
            'w_year': self.ent_w_year.get(),
            'w_age': self.ent_w_age.get(),
            'w_sex': self.ent_w_sex.get().upper(),
            'w_citizen': self.ent_w_citizen.get().upper(),
            'w_res': self.ent_w_res.get().upper(),
            'w_rel': self.ent_w_rel.get().upper(),
            'w_status': self.ent_w_status.get().upper(),
            'wf_first': self.ent_wf_first.get().upper(),
            'wf_mid': self.ent_wf_mid.get().upper(),
            'wf_last': self.ent_wf_last.get().upper(),
            'wf_citizen': self.ent_wf_citizen.get().upper(),
            'wm_first': self.ent_wm_first.get().upper(),
            'wm_mid': self.ent_wm_mid.get().upper(),
            'wm_last': self.ent_wm_last.get().upper(),
            'wm_citizen': self.ent_wm_citizen.get().upper(),
            'w_c_first': self.ent_w_c_first.get().upper(),
            'w_c_mid': self.ent_w_c_mid.get().upper(),
            'w_c_last': self.ent_w_c_last.get().upper(),
            'w_c_rel': self.ent_w_c_rel.get().upper(),
            'w_c_res': self.ent_w_c_res.get().upper(),

            'pom_office': self.ent_pom_office.get().upper(),
            'pom_city': self.ent_pom_city.get().upper(),
            'pom_prov': self.ent_pom_prov.get().upper(),
            'dom_day': self.ent_dom_day.get().upper(),
            'dom_month': self.ent_dom_month.get().upper(),
            'dom_year': self.ent_dom_year.get().upper(),
            'tom': self.ent_tom.get().upper(),

            'h_full_name': self.ent_s18_hname.get().upper(),
            'w_full_name': self.ent_s18_wname.get().upper(),
            
            # FIXED: Uses self.settlement_var to toggle checks based on user input
            'marriage_settlement': self.settlement_var.get() == 1, 
            'no_marriage_settlement': self.settlement_var.get() == 2,
            
            's18_sig_day': self.ent_s18_sig_day.get().upper(),
            's18_sig_month': self.ent_s18_sig_month.get().upper(),
            'license_type': lic_type,
            'license_no': self.ent_lic_no.get().upper(),
            'issued_on': self.ent_lic_issued_on.get().upper(),
            'issued_at': self.ent_lic_issued_at.get().upper(),
            'art': self.ent_lic_art.get().upper(),
            'off_name': self.ent_off_name.get().upper(),
            'off_pos': self.ent_off_pos.get().upper(),
            'if_app': self.ent_if_app.get().upper(),
            'witnesses': [self.ent_wit1.get(), self.ent_wit2.get(), self.ent_wit3.get(), self.ent_wit4.get()]
        }
        self.execute_print(data, "Marriage_Page1.pdf")

    def print_pdf_p2(self):
        data = {
            'page': 2, 
            'p2_wit1': self.ent_p2_wit1.get().upper(),
            'p2_wit2': self.ent_p2_wit2.get().upper(),
            'p2_wit3': self.ent_p2_wit3.get().upper(),
            'p2_wit4': self.ent_p2_wit4.get().upper(),
            'p2_wit5': self.ent_p2_wit5.get().upper(),
            'p2_wit6': self.ent_p2_wit6.get().upper(),
            'p2_wit7': self.ent_p2_wit7.get().upper(),
            'p2_wit8': self.ent_p2_wit8.get().upper(),
        }
        self.execute_print(data, "Marriage_Page2.pdf")

    def execute_print(self, data, filename):
        if generate_full_certificate:
            try:
                generate_full_certificate(filename, data, show_template=False)
                if os.path.exists(filename):
                    abs_path = os.path.abspath(filename)
                    try:
                        win32api.ShellExecute(0, "printto", abs_path, f'"{win32print.GetDefaultPrinter()}"', ".", 0)
                        messagebox.showinfo("Success", "Sent to printer.")
                    except Exception:
                        os.startfile(abs_path)
            except Exception as e:
                messagebox.showerror("Error", f"Execution failed: {str(e)}")
        else:
            messagebox.showerror("Error", "PDF generator module not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarriageApp(root)
    root.mainloop()