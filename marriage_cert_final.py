from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_full_certificate(output_file, data, show_template=False):
    # PH Legal Size (approx 8.5 x 13 in)
    PH_LEGAL = (215.9 * mm, 330.2 * mm)
    width, height = PH_LEGAL
    c = canvas.Canvas(output_file, pagesize=PH_LEGAL)

    # Background for testing alignment
    if show_template:
        template = "form.jpg" if data.get('page', 1) == 1 else "form_page2.png"
        c.drawImage(template, 0, 0, width=width, height=height)

    # Helper for Top-Left mm coordinates with Dynamic Font Sizing
    def draw(text, x_mm, y_mm, size=9, bold=False, max_width_mm=None):
        if not text: return
        
        text_str = str(text)
        font = "Helvetica-Bold" if bold else "Helvetica"
        current_size = size
        
        # Logic to shrink font if it's too wide for the box
        if max_width_mm:
            max_width_pts = max_width_mm * mm
            text_width = c.stringWidth(text_str, font, current_size)
            
            # Reduce font size until it fits (minimum 5pt)
            while text_width > max_width_pts and current_size > 5:
                current_size -= 0.5
                text_width = c.stringWidth(text_str, font, current_size)

        c.setFont(font, current_size)
        # Convert Y from top-down mm to ReportLab bottom-up points
        c.drawString(x_mm * mm, height - (y_mm * mm), text_str)

    # --- PAGE 1 LOGIC ---
    if data.get('page', 1) == 1:
        # Header
        draw(data.get('province', ''), 40, 15, max_width_mm=60)
        draw(data.get('city_municipality', ''), 52, 20, max_width_mm=60)
        draw(data.get('registry_no', ''), 165, 30, size=10, bold=True)

        # Section 1: Names (Husband & Wife)
        draw(data.get('h_first', ''), 60, 29, max_width_mm=65)
        draw(data.get('h_middle', ''), 60, 33, max_width_mm=65)
        draw(data.get('h_last', ''), 60, 38, max_width_mm=65)
        draw(data.get('w_first', ''), 140, 29, max_width_mm=65)
        draw(data.get('w_middle', ''), 140, 33, max_width_mm=65)
        draw(data.get('w_last', ''), 140, 38, max_width_mm=65)

        # Section 2: Date of Birth & Age
        draw(data.get('h_day', ''), 49, 47)
        draw(data.get('h_month', ''), 68, 47)
        draw(data.get('h_year', ''), 91, 47)
        draw(data.get('h_age', ''), 117, 47)
        draw(data.get('w_day', ''), 132, 47)
        draw(data.get('w_month', ''), 152, 47)
        draw(data.get('w_year', ''), 172, 47)
        draw(data.get('w_age', ''), 199, 47)

        # SECTION 3: PLACE OF BIRTH
        draw(data.get('h_pob_city', ''), 43 ,57, max_width_mm=23)
        draw(data.get('h_pob_prov', ''), 68, 57, max_width_mm=32)
        draw(data.get('h_pob_ctry', ''), 103, 57, max_width_mm=25)
        draw(data.get('w_pob_city', ''), 129, 57, max_width_mm=23)
        draw(data.get('w_pob_prov', ''), 154, 57, max_width_mm=27)
        draw(data.get('w_pob_ctry', ''), 183, 57, max_width_mm=25)

        # Section 4: Sex & Citizenship
        draw(data.get('h_sex', ''), 55, 65)
        draw(data.get('h_citizen', ''), 95, 65, max_width_mm=35)
        draw(data.get('w_sex', ''), 140, 65)
        draw(data.get('w_citizen', ''), 175, 65, max_width_mm=35)

        # Section 5: Residence
        draw(data.get('h_res', ''), 55, 75, max_width_mm=80)
        draw(data.get('w_res', ''), 140, 75, max_width_mm=80)

        # Section 6: Religion
        draw(data.get('h_rel', ''), 54, 84, max_width_mm=75)
        draw(data.get('w_rel', ''), 139, 84, max_width_mm=75)

        # Section 7: Civil Status
        draw(data.get('h_status', ''), 55, 89)
        draw(data.get('w_status', ''), 140, 89)

        # Section 8: Name Of Father
        draw(data.get('hf_first', ''), 45, 99, max_width_mm=24)
        draw(data.get('hf_mid', ''), 70, 99, max_width_mm=28)
        draw(data.get('hf_last', ''), 100, 99, max_width_mm=30)
        draw(data.get('wf_first', ''), 130, 99, max_width_mm=24)
        draw(data.get('wf_mid', ''), 155, 99, max_width_mm=24)
        draw(data.get('wf_last', ''), 180, 99, max_width_mm=30)

        # Section 9: Father Citizenship
        draw(data.get('hf_citizen', ''), 55, 106, max_width_mm=80)
        draw(data.get('wf_citizen', ''), 140, 106, max_width_mm=80)

        # Section 10: Maiden Name of Mother
        draw(data.get('hm_first', ''), 44, 116, max_width_mm=24)
        draw(data.get('hm_mid', ''), 69, 116, max_width_mm=28)
        draw(data.get('hm_last', ''), 100, 116, max_width_mm=30)
        draw(data.get('wm_first', ''), 130, 116, max_width_mm=24)
        draw(data.get('wm_mid', ''), 157, 116, max_width_mm=24)
        draw(data.get('wm_last', ''), 180, 116, max_width_mm=30)

        # Section 11: Mother Citizenship
        draw(data.get('hm_citizen', ''), 55, 124, max_width_mm=80)
        draw(data.get('wm_citizen', ''), 140, 124, max_width_mm=80)

        # Section 12: Person Who Give Consent
        draw(data.get('h_c_first', ''), 45, 134, max_width_mm=24)
        draw(data.get('h_c_mid', ''), 73, 134, max_width_mm=20)
        draw(data.get('h_c_last', ''), 95, 134, max_width_mm=24)
        draw(data.get('w_c_first', ''), 130, 134, max_width_mm=24)
        draw(data.get('w_c_mid', ''), 157, 134, max_width_mm=20)
        draw(data.get('w_c_last', ''), 180, 134, max_width_mm=24)

        # Section 13: Relationship
        draw(data.get('h_c_rel', ''), 55, 140, max_width_mm=80)
        draw(data.get('w_c_rel', ''), 140, 140, max_width_mm=80)

        # Section 14: Residence
        draw(data.get('h_c_res', ''), 43, 150, max_width_mm=80)
        draw(data.get('w_c_res', ''), 129, 150, max_width_mm=80)

        # Section 15: Place of Marriage
        draw(data.get('pom_office', ''), 50, 157, max_width_mm=80)
        draw(data.get('pom_city', ''), 130, 157, max_width_mm=25)
        draw(data.get('pom_prov', ''), 160, 157, max_width_mm=30)

        # Section 16: Date of Marriage
        draw(data.get('dom_day', ''), 60, 166)
        draw(data.get('dom_month', ''), 80, 166)
        draw(data.get('dom_year', ''), 100, 166)

        # Section 17: Time of Marriage
        draw(data.get('tom', ''), 165, 166, max_width_mm=30)

        # Section 18: Contracting Parties Recap
        draw(data.get('h_full_name', ''), 72, 178, bold=True, max_width_mm=60)
        draw(data.get('w_full_name', ''), 140, 178, bold=True, max_width_mm=60)
        

        if data.get('marriage_settlement') == True:
        # Adjust these coordinates (x, y) to line up exactly with your form's box
            draw("✓", 82, 187, size=12, bold=True)

        # Checkbox for 'not entered into a marriage settlement'
        if data.get('no_marriage_settlement') == True:
            # Adjust these coordinates (x, y) to line up exactly with your form's box
            draw("✓", 149, 187, size=12, bold=True)

        draw(data.get('s18_sig_day', ''), 160, 190)
        draw(data.get('s18_sig_month', ''), 190, 190)

        # Section 19: Solemnizing Officer & License Details
        if data.get('license_type') == 'a':
            draw("✔", 19, 220, size=15, bold=True)
            draw(data.get('license_no', ''), 60, 220, max_width_mm=50)
            draw(data.get('issued_on', ''), 115, 220, max_width_mm=45)
            draw(data.get('issued_at', ''), 155, 220, max_width_mm=50)
        elif data.get('license_type') == 'b':
            draw("✔", 19, 227, size=15, bold=True)
            draw(data.get('art', ''), 127, 226, max_width_mm=20)
        elif data.get('license_type') == 'c':
            draw("✔", 20, 233, size=15, bold=True)
        
        draw(data.get('off_name', ''), 25, 240, max_width_mm=70)
        draw(data.get('off_pos', ''), 90, 240, max_width_mm= 50)
        draw(data.get('if_app', ''), 145, 240, max_width_mm=70)


        # Section 20a: Witnesses
        witnesses = data.get('witnesses', [])
        name1 = witnesses[0] if len(witnesses) > 0 else ''
        name2 = witnesses[1] if len(witnesses) > 1 else ''
        name3 = witnesses[2] if len(witnesses) > 2 else ''
        name4 = witnesses[3] if len(witnesses) > 3 else ''

        draw(name1, 20, 260, size=12, max_width_mm=40)
        draw(name3, 70, 260, size=12, max_width_mm=40)
        draw(name4, 115, 260, size=12, max_width_mm=40) 
        draw(name2, 160, 260, size=12, max_width_mm=40) 
         
        

    # --- PAGE 2 LOGIC ---
    elif data.get('page') == 2:
        # draw(data.get('aff_officer', ''), 60, 110, bold=True, max_width_mm=80)
        # draw(data.get('aff_office', ''), 150, 110, max_width_mm=60)
        # draw(data.get('aff_address', ''), 60, 125, max_width_mm=140)
        
        # aff_type = data.get('aff_type', '')
        # if aff_type == 'a': draw("✔", 25, 155, size=12, bold=True)
        # elif aff_type == 'b': draw("✔", 25, 168, size=12, bold=True)
        # elif aff_type == 'c': draw("✔", 25, 180, size=12, bold=True)

        draw(data.get('p2_wit1', ''), 10, 5, size=12, max_width_mm=40)
        draw(data.get('p2_wit2', ''), 60, 5, size=12, max_width_mm=40)
        draw(data.get('p2_wit3', ''), 105, 5, size=12, max_width_mm=40)
        draw(data.get('p2_wit4', ''), 155, 5, size=12, max_width_mm=40)
        draw(data.get('p2_wit5', ''), 10, 15, size=12, max_width_mm=40)
        draw(data.get('p2_wit6', ''), 60, 15, size=12, max_width_mm=40)
        draw(data.get('p2_wit7', ''), 105, 15, size=12, max_width_mm=40)
        draw(data.get('p2_wit8', ''), 155, 15, size=12, max_width_mm=40)

    c.save()