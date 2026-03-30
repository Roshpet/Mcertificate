from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_full_certificate(output_file, data, show_template=False):
    # Philippine Legal Size (8.5 x 13 inches)
    PH_LEGAL = (215.9 * mm, 330.2 * mm)
    width, height = PH_LEGAL
    c = canvas.Canvas(output_file, pagesize=PH_LEGAL)

    # 1. Background Template (Set to True only for testing/alignment)
    if show_template:
        # Replace with your actual filename
        c.drawImage("form.jpg", 0, 0, width=width, height=height)

    # Helper function for Top-Left coordinates
    def draw(text, x_mm, y_mm, size=10, bold=False):
        font = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(font, size)
        c.drawString(x_mm * mm, height - (y_mm * mm), str(text))

    # --- SECTION 1-14: PERSONAL DATA ---
    draw(data.get('province', ''), 35, 84)
    draw(data.get('registry_no', ''), 165, 84)
    
    # Husband Info
    draw(data.get('h_first', ''), 25, 122)
    draw(data.get('h_middle', ''), 25, 133)
    draw(data.get('h_last', ''), 25, 145)
    draw(f"{data.get('h_day','')}  {data.get('h_month','')}  {data.get('h_year','')}", 25, 165)
    draw(data.get('h_age', ''), 110, 165)

    # Wife Info
    draw(data.get('w_first', ''), 120, 122)
    draw(data.get('w_middle', ''), 120, 133)
    draw(data.get('w_last', ''), 120, 145)

    # --- SECTION 18: CERTIFICATION OF CONTRACTING PARTIES ---
    # Positioning text between pre-printed words
    draw(data.get('h_full_name', ''), 48, 191, size=9, bold=True)
    draw(data.get('w_full_name', ''), 125, 191, size=9, bold=True)
    
    # Checkboxes for Section 18
    if data.get('sec18_entered'):
        draw("X", 78.5, 203.5, size=11, bold=True) # Box: have entered
    else:
        draw("X", 143.5, 203.5, size=11, bold=True) # Box: have not entered

    # --- SECTION 19: SOLEMNIZING OFFICER ---
    draw(data.get('officer_name', ''), 52, 218, size=9)
    
    # Checkboxes for Section 19 (a, b, or c)
    if data.get('license_type') == 'a':
        draw("X", 19.5, 228.5, size=11, bold=True)
        draw(data.get('license_no', ''), 35, 231)
        draw(data.get('issued_on', ''), 105, 231)
        draw(data.get('issued_at', ''), 155, 231)
    elif data.get('license_type') == 'b':
        draw("X", 19.5, 241.5, size=11, bold=True)
    elif data.get('license_type') == 'c':
        draw("X", 19.5, 254.5, size=11, bold=True)

    # --- SECTION 20a: WITNESSES ---
    witnesses = data.get('witnesses', [])
    for i, name in enumerate(witnesses[:4]): # Limits to first 4 witnesses
        draw(name, 25, 285 + (i * 6), size=8)

    # --- SECTION 21 & 22: REGISTRATION ---
    draw(data.get('received_by_name', ''), 25, 315)
    draw(data.get('registered_by_name', ''), 120, 315)

    c.save()
    print(f"Success: {output_file} generated.")

# --- DATA OBJECT ---
marriage_info = {
    'province': 'SOUTHERN LEYTE',
    'registry_no': '2026-04-001',
    'h_first': 'ROSHPET JAY', 'h_middle': 'B.', 'h_last': 'DIAPOLET',
    'h_full_name': 'ROSHPET JAY B. DIAPOLET',
    'w_full_name': 'JANE SMITH DOE',
    'sec18_entered': True,
    'license_type': 'a',
    'license_no': 'ML-998877',
    'issued_on': 'March 01, 2026',
    'issued_at': 'Bontoc, Southern Leyte',
    'witnesses': ['John Doe', 'Mary Public', 'Peter Piper', 'Sarah Jenkins'],
    'received_by_name': 'OFFICER NAME HERE'
}

# Run the generator
generate_full_certificate("Marriage_Cert_Final.pdf", marriage_info, show_template=False)