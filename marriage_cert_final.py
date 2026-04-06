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

    # Helper for Top-Left mm coordinates
    def draw(text, x_mm, y_mm, size=9, bold=False):
        if not text: return
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        # Convert Y from top-down mm to ReportLab bottom-up points
        c.drawString(x_mm * mm, height - (y_mm * mm), str(text))

    # --- PAGE 1 LOGIC ---
    if data.get('page', 1) == 1:
        # Header
        draw(data.get('province', ''), 52, 29)
        draw(data.get('city_municipality', ''), 52, 34)
        draw(data.get('registry_no', ''), 165, 30, size=10, bold=True)

        # Section 1: Names (Husband & Wife)
        draw(data.get('h_first', ''), 65, 43)
        draw(data.get('h_middle', ''), 65, 48)
        draw(data.get('h_last', ''), 65, 53)
        draw(data.get('w_first', ''), 145, 43)
        draw(data.get('w_middle', ''), 145, 48)
        draw(data.get('w_last', ''), 145, 53)

        # Section 2: Date of Birth & Age
        # Husband
        draw(data.get('h_day', ''), 54, 62)
        draw(data.get('h_month', ''), 75, 62)
        draw(data.get('h_year', ''), 103, 62)
        draw(data.get('h_age', ''), 130, 62)
        # Wife
        draw(data.get('w_day', ''), 138, 62)
        draw(data.get('w_month', ''), 155, 62)
        draw(data.get('w_year', ''), 180, 62)
        draw(data.get('w_age', ''), 203, 62)

        #SECTION 3: PLACE OF BIRTH
        #HUSBAND
        draw(data.get('h_pob_city', ''), 55 ,70)
        draw(data.get('h_pob_prov', ''), 70, 70)
        draw(data.get('h_pob_ctry', ''), 100, 70)
        #Wife
        draw(data.get('w_pob_city', ''), 140, 70)
        draw(data.get('w_pob_prov', ''), 160, 70)
        draw(data.get('w_pob_ctry', ''), 180, 70)

        # Section 4: Sex & Citizenship
        # Husband
        draw(data.get('h_sex', ''), 55, 78)
        draw(data.get('h_citizen', ''), 95, 78)
        # Wife
        draw(data.get('w_sex', ''), 140, 78)
        draw(data.get('w_citizen', ''), 175, 78)

        # Section 5: Residence
        # Husband
        draw(data.get('h_res', ''), 55, 82)
        # Wife
        draw(data.get('w_res', ''), 140, 82)


        # Section 6: Relationship
        # Husband
        draw(data.get('h_rel', ''), 55, 89)
        draw(data.get('w_rel', ''), 140, 89)

        # Section 7: Civil Status
        # Husband
        draw(data.get('h_status', ''), 55, 93)
        # Wife
        draw(data.get('w_status', ''), 140, 93)

        # Section 8: Name Of Father
        # Husband
        draw(data.get('hf_first', ''), 55, 99)
        draw(data.get('hf_mid', ''), 65, 99)
        draw(data.get('hf_last', ''), 75, 99)
        # Wife
        draw(data.get('wf_first', ''), 140, 99)
        draw(data.get('wf_first', ''), 145, 99)
        draw(data.get('wf_last', ''), 155, 99)

        # Section 9: Father Citizenship
        # Husband
        draw(data.get('hf_citizen', ''), 55, 105)
        # Wife
        draw(data.get('wf_citizen', ''), 140, 105)

        # Section 18: Contracting Parties Recap
        draw(data.get('h_full_name', ''), 85, 185, bold=True)
        draw(data.get('w_full_name', ''), 155, 185, bold=True)
        
        # Sec 18 Checkboxes
        if data.get('sec18_entered'):
            draw("/", 82, 198, size=12, bold=True)
        else:
            draw("/", 147, 198, size=12, bold=True)

        # Section 19: Solemnizing Officer & License Details
        if data.get('license_type') == 'a':
            draw("/", 22, 227, size=12, bold=True)
            draw(data.get('license_no', ''), 60, 228)
            draw(data.get('issued_on', ''), 115, 228)
            draw(data.get('issued_at', ''), 165, 228)
        elif data.get('license_type') == 'b':
            draw("/", 22, 235, size=12, bold=True)
        elif data.get('license_type') == 'c':
            draw("/", 22, 243, size=12, bold=True)

        # Section 20a: Witnesses
        witnesses = data.get('witnesses', [])
        for i, name in enumerate(witnesses[:4]):
            x_pos = 25 if i % 2 == 0 else 110
            y_pos = 265 if i < 2 else 272
            draw(name, x_pos, y_pos, size=8)

    # --- PAGE 2 LOGIC ---
    elif data.get('page') == 2:
        draw(data.get('aff_officer', ''), 60, 110, bold=True)
        draw(data.get('aff_office', ''), 150, 110)
        draw(data.get('aff_address', ''), 60, 125)
        
        # Affidavit Checkboxes
        aff_type = data.get('aff_type', '')
        if aff_type == 'a': draw("/", 25, 155, size=12, bold=True)
        elif aff_type == 'b': draw("/", 25, 168, size=12, bold=True)
        elif aff_type == 'c': draw("/", 25, 180, size=12, bold=True)

    c.save()