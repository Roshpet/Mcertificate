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
        
        # --- 1. NAVIGATION BAR (Added without touching canvas) ---
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
        self.settlement_var = tk.IntVar(value=0)
        self.license_type_var = tk.IntVar(value=0)
        
        # New variable for Page 2 Affidavit Checkboxes
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
        entry_widget.bind("<FocusIn>", lambda e: self.position_check_icon(entry_widget))

    def load_page_one(self):
        try:
            self.img = Image.open("form.jpg")
            self.img = self.img.resize((780, 1150), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
            self.canvas.config(scrollregion=(0, 0, 800, 1500)) 
        except FileNotFoundError:
            print("Error: form.jpg not found.")

        # --- PRESERVED PAGE 1 FIELDS ---
        self.ent_prov = tk.Entry(self.root, width=25); self.apply_style(self.ent_prov); self.canvas.create_window(240, 95, window=self.ent_prov)
        self.ent_city = tk.Entry(self.root, width=25); self.apply_style(self.ent_city); self.canvas.create_window(270, 113, window=self.ent_city)
        self.ent_h_first = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_first); self.canvas.create_window(300, 142, window=self.ent_h_first)
        self.ent_h_mid = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_mid); self.canvas.create_window(300, 157, window=self.ent_h_mid)
        self.ent_h_last = tk.Entry(self.root, width=30); self.apply_style(self.ent_h_last); self.canvas.create_window(300, 172, window=self.ent_h_last)
        self.ent_w_first = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_first); self.canvas.create_window(600, 142, window=self.ent_w_first)
        self.ent_w_mid = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_mid); self.canvas.create_window(600, 157, window=self.ent_w_mid)
        self.ent_w_last = tk.Entry(self.root, width=30); self.apply_style(self.ent_w_last); self.canvas.create_window(600, 172, window=self.ent_w_last)
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
        self.ent_pom_prov = tk.Entry(root, width=18); self.apply_style(self.ent_pom_prov); self.canvas.create_window(660, 541, window=self.ent_pom_prov)
        self.ent_dom_day = tk.Entry(root, width=5); self.apply_style(self.ent_dom_day); self.canvas.create_window(230, 570, window=self.ent_dom_day)
        self.ent_dom_month = tk.Entry(root, width=12); self.apply_style(self.ent_dom_month); self.canvas.create_window(295, 570, window=self.ent_dom_month)
        self.ent_dom_year = tk.Entry(root, width=8); self.apply_style(self.ent_dom_year); self.canvas.create_window(375, 570, window=self.ent_dom_year)
        self.ent_tom = tk.Entry(root, width=15); self.apply_style(self.ent_tom); self.canvas.create_window(630, 570, window=self.ent_tom)
        self.ent_s18_hname = tk.Entry(root, width=35); self.apply_style(self.ent_s18_hname); self.canvas.create_window(365, 610, window=self.ent_s18_hname)
        self.ent_s18_wname = tk.Entry(root, width=35); self.apply_style(self.ent_s18_wname); self.canvas.create_window(600, 610, window=self.ent_s18_wname)
        self.chk_entered = tk.Checkbutton(root, variable=self.settlement_var, onvalue=1, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(304, 639, window=self.chk_entered)
        self.chk_not_entered = tk.Checkbutton(root, variable=self.settlement_var, onvalue=2, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(544, 639, window=self.chk_not_entered)
        self.ent_s18_sig_day = tk.Entry(root, width=5); self.apply_style(self.ent_s18_sig_day); self.canvas.create_window(590, 650, window=self.ent_s18_sig_day)
        self.ent_s18_sig_month = tk.Entry(root, width=15); self.apply_style(self.ent_s18_sig_month); self.canvas.create_window(690, 650, window=self.ent_s18_sig_month)
        self.chk_lic_a = tk.Checkbutton(root, variable=self.license_type_var, onvalue=1, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 737, window=self.chk_lic_a)
        self.ent_lic_no = tk.Entry(root, width=23); self.apply_style(self.ent_lic_no); self.canvas.create_window(280, 739, window=self.ent_lic_no)
        self.ent_lic_issued_on = tk.Entry(root, width=23); self.apply_style(self.ent_lic_issued_on); self.canvas.create_window(470, 739, window=self.ent_lic_issued_on)
        self.ent_lic_issued_at = tk.Entry(root, width=28); self.apply_style(self.ent_lic_issued_at); self.canvas.create_window(650, 739, window=self.ent_lic_issued_at)
        self.chk_lic_b = tk.Checkbutton(root, variable=self.license_type_var, onvalue=2, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 761, window=self.chk_lic_b)
        self.ent_lic_art = tk.Entry(root, width=5); self.apply_style(self.ent_lic_art); self.canvas.create_window(475, 760, window=self.ent_lic_art)
        self.chk_lic_c = tk.Checkbutton(root, variable=self.license_type_var, onvalue=3, offvalue=0, bg="#ADD8E6"); self.canvas.create_window(85, 783, window=self.chk_lic_c)
        self.ent_off_name = tk.Entry(root, width=35); self.apply_style(self.ent_off_name); self.canvas.create_window(188, 805, window=self.ent_off_name)
        self.ent_off_pos = tk.Entry(root, width=25); self.apply_style(self.ent_off_pos); self.canvas.create_window(405, 805, window=self.ent_off_pos)
        self.ent_if_app = tk.Entry(root, width=35); self.apply_style(self.ent_if_app); self.canvas.create_window(620, 805, window=self.ent_if_app)
        self.ent_wit1 = tk.Entry(root, width=25); self.apply_style(self.ent_wit1); self.canvas.create_window(155, 865, window=self.ent_wit1)
        self.ent_wit2 = tk.Entry(root, width=25); self.apply_style(self.ent_wit2); self.canvas.create_window(665, 865, window=self.ent_wit2)
        self.ent_wit3 = tk.Entry(root, width=25); self.apply_style(self.ent_wit3); self.canvas.create_window(328, 865, window=self.ent_wit3)
        self.ent_wit4 = tk.Entry(root, width=25); self.apply_style(self.ent_wit4); self.canvas.create_window(500, 865, window=self.ent_wit4)

        # --- PAGE 1 PRINT BUTTON ---
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

        # --- NEW SECTION 20b: WITNESSES (Back Page) ---
        self.ent_p2_wit1 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit1)
        self.canvas.create_window(124, 65, window=self.ent_p2_wit1)
        self.ent_p2_wit2 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit2)
        self.canvas.create_window(290, 65, window=self.ent_p2_wit2)
        self.ent_p2_wit3 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit3)
        self.canvas.create_window(469, 65, window=self.ent_p2_wit3)
        self.ent_p2_wit4 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit4)
        self.canvas.create_window(636, 65, window=self.ent_p2_wit4)

        self.ent_p2_wit5 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit5)
        self.canvas.create_window(124, 100, window=self.ent_p2_wit5)
        self.ent_p2_wit6 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit6)
        self.canvas.create_window(290, 100, window=self.ent_p2_wit6)
        self.ent_p2_wit7 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit7)
        self.canvas.create_window(469, 100, window=self.ent_p2_wit7)
        self.ent_p2_wit8 = tk.Entry(self.root, width=25); self.apply_style(self.ent_p2_wit8)
        self.canvas.create_window(636, 100, window=self.ent_p2_wit8)

        # # --- AFFIDAVIT OF SOLEMNIZING OFFICER ---
        # self.ent_aff_name = tk.Entry(self.root, width=40); self.apply_style(self.ent_aff_name)
        # self.canvas.create_window(235, 385, window=self.ent_aff_name)
        # self.ent_aff_office = tk.Entry(self.root, width=35); self.apply_style(self.ent_aff_office)
        # self.canvas.create_window(700, 385, window=self.ent_aff_office)
        # self.ent_aff_address = tk.Entry(self.root, width=45); self.apply_style(self.ent_aff_address)
        # self.canvas.create_window(240, 420, window=self.ent_aff_address)
        # self.ent_aff_husband = tk.Entry(self.root, width=35); self.apply_style(self.ent_aff_husband)
        # self.canvas.create_window(460, 465, window=self.ent_aff_husband)
        # self.ent_aff_wife = tk.Entry(self.root, width=35); self.apply_style(self.ent_aff_wife)
        # self.canvas.create_window(720, 465, window=self.ent_aff_wife)

        # # Checkboxes (a through e)
        # self.chk_a = tk.Checkbutton(self.root, variable=self.affidavit_lic_var, onvalue=1, bg="#ADD8E6"); self.canvas.create_window(105, 500, window=self.chk_a)
        # self.chk_b = tk.Checkbutton(self.root, variable=self.affidavit_lic_var, onvalue=2, bg="#ADD8E6"); self.canvas.create_window(105, 542, window=self.chk_b)
        # self.chk_c = tk.Checkbutton(self.root, variable=self.affidavit_lic_var, onvalue=3, bg="#ADD8E6"); self.canvas.create_window(105, 580, window=self.chk_c)
        # self.chk_d = tk.Checkbutton(self.root, variable=self.affidavit_lic_var, onvalue=4, bg="#ADD8E6"); self.canvas.create_window(105, 655, window=self.chk_d)
        # self.chk_e = tk.Checkbutton(self.root, variable=self.affidavit_lic_var, onvalue=5, bg="#ADD8E6"); self.canvas.create_window(105, 695, window=self.chk_e)

        # # Footer Date/Place
        # self.ent_aff_sig_day = tk.Entry(self.root, width=5); self.apply_style(self.ent_aff_sig_day); self.canvas.create_window(550, 855, window=self.ent_aff_sig_day)
        # self.ent_aff_sig_place = tk.Entry(self.root, width=30); self.apply_style(self.ent_aff_sig_place); self.canvas.create_window(260, 885, window=self.ent_aff_sig_place)

        # --- PAGE 2 PRINT BUTTON ---
        self.btn_print_p2 = tk.Button(self.root, text="PRINT PAGE 2 ONLY", bg="#e67e22", fg="white", 
                                     font=("Arial", 11, "bold"), command=self.print_pdf_p2)
        self.canvas.create_window(400, 1200, window=self.btn_print_p2)

    # --- UI INTERACTION LOGIC ---
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
            if self.canvas.type(item) == "window":
                if self.canvas.itemcget(item, "window") == str(widget):
                    x, y = self.canvas.coords(item)
                    width = widget.winfo_width() / 2
                    self.active_check_window = self.canvas.create_window(x + width + 15, y, window=self.active_check_btn_ui)
                    break

    def toggle_field_state(self, widget):
        if not widget.is_locked:
            widget.config(bg="white", highlightthickness=0)
            widget.is_locked = True
        else:
            widget.config(bg="#ADD8E6", highlightthickness=1)
            widget.is_locked = False
        self.position_check_icon(widget)

    # --- PRINT LOGIC ---
    def print_pdf_p1(self):
        lic_type = {1: 'a', 2: 'b', 3: 'c'}.get(self.license_type_var.get(), '')
        data = {
            'page': 1,
            'province': self.ent_prov.get().upper(),
            'license_type': lic_type,
            'sec18_entered': self.settlement_var.get() == 1,
            'show_template': False 
        }
        self.execute_print(data, "Marriage_Page1.pdf")

    def print_pdf_p2(self):
        aff_type = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e'}.get(self.affidavit_lic_var.get(), '')
        data = {
            'page': 2,
            'aff_officer': self.ent_aff_name.get().upper(),
            'aff_type': aff_type,
            'show_template': False 
        }
        self.execute_print(data, "Marriage_Page2.pdf")

    def execute_print(self, data, filename):
        if generate_full_certificate:
            try:
                generate_full_certificate(filename, data, show_template=False)
                messagebox.showinfo("Success", f"Generated {filename} successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "PDF generator module not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarriageApp(root)
    root.mainloop()