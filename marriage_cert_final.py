from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_full_certificate(output_file, data, show_template=False):
    # PH Legal Size (approx 8.5 x 13 in)
    PH_LEGAL = (215.9 * mm, 330.2 * mm)
    width, height = PH_LEGAL
    c = canvas.Canvas(output_file, pagesize=PH_LEGAL)

    # Background for testing
    if show_template:
        # Toggle between page 1 and page 2 template based on data
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

        # Section 1: Names
        draw(data.get('h_first', ''), 65, 43)
        draw(data.get('h_middle', ''), 65, 48)
        draw(data.get('h_last', ''), 65, 53)
        draw(data.get('w_first', ''), 145, 43)
        draw(data.get('w_middle', ''), 145, 48)
        draw(data.get('w_last', ''), 145, 53)

        # Section 2: Date of Birth & Age
        draw(data.get('h_day', ''), 54, 62)
        draw(data.get('h_month', ''), 75, 62)
        draw(data.get('h_year', ''), 103, 62)
        draw(data.get('h_age', ''), 130, 62)

        # Section 4: Sex & Citizenship
        draw(data.get('h_sex', ''), 55, 78)
        draw(data.get('h_citizen', ''), 95, 78)
        draw(data.get('w_sex', ''), 140, 78)
        draw(data.get('w_citizen', ''), 175, 78)

        # Section 18: Contracting Parties Recap
        draw(data.get('h_full_name', ''), 85, 185, bold=True)
        draw(data.get('w_full_name', ''), 155, 185, bold=True)
        
        # Sec 18 Checkboxes
        if data.get('sec18_entered'):
            draw("X", 82, 198, size=12, bold=True)
        else:
            draw("X", 147, 198, size=12, bold=True)

        # Section 19: Solemnizing Officer
        if data.get('license_type') == 'a':
            draw("X", 22, 227)
            draw(data.get('license_no', ''), 60, 228)
            draw(data.get('license_date', ''), 115, 228)
            draw(data.get('license_place', ''), 165, 228)
        elif data.get('license_type') == 'b':
            draw("X", 22, 235)
        elif data.get('license_type') == 'c':
            draw("X", 22, 243)

        # Section 20a: Witnesses
        witnesses = data.get('witnesses', [])
        for i, name in enumerate(witnesses[:4]):
            x_pos = 25 if i % 2 == 0 else 110
            y_pos = 265 if i < 2 else 272
            draw(name, x_pos, y_pos, size=8)

    # --- PAGE 2 LOGIC ---
    elif data.get('page') == 2:
        draw(data.get('aff_name', ''), 60, 110, bold=True)
        draw(data.get('aff_office', ''), 150, 110)
        draw(data.get('aff_address', ''), 60, 125)
        
        # Affidavit Checkboxes
        aff_type = data.get('aff_type', '')
        if aff_type == 'a': draw("X", 25, 155)
        elif aff_type == 'b': draw("X", 25, 168)
        elif aff_type == 'c': draw("X", 25, 180)

    c.save()