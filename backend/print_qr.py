from fpdf import FPDF
from PIL import Image
import os

def generate_pdf(qr_folder, output_pdf):
    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    qr_size = 80  # Taille des QR codes augmentée
    page_width = 210
    page_height = 297
    
    # Calcul des positions pour centrer les tickets dans chaque quart de la page
    center_x = [page_width * 0.25, page_width * 0.75]
    center_y = [page_height * 0.25, page_height * 0.75]
    
    title_font_size = 14
    text_font_size = 10
    
    qr_files = [f for f in os.listdir(qr_folder) if f.endswith(".png")]
    qr_files.sort()  # Trier les fichiers pour un ordre cohérent
    
    positions = [(x, y) for y in center_y for x in center_x]
    
    for i, qr_file in enumerate(qr_files):
        x, y = positions[i % 4]  # Position sur la page
        
        # Centrer chaque QR code sur son quart
        x -= qr_size / 2
        y -= qr_size / 2
        
        # Extraire le numéro du fichier
        ticket_number = os.path.splitext(qr_file)[0]
        
        # Ajouter le titre "Bal des bières 2025"
        pdf.set_xy(x, y - 25)
        pdf.set_font("Arial", "B", title_font_size)
        pdf.cell(qr_size, 5, "Bal des bières 2025", 0, 1, "C")
        
        # Ajouter "TICKET"
        pdf.set_xy(x, y - 15)
        pdf.set_font("Arial", "B", text_font_size)
        pdf.cell(qr_size, 5, f"TICKET {ticket_number}", 0, 1, "C")
        
        # Ajouter le QR Code
        pdf.image(os.path.join(qr_folder, qr_file), x, y, qr_size, qr_size)
        
        # Ajouter la phrase sous le QR code
        pdf.set_xy(x, y + qr_size + 5)
        pdf.set_font("Arial", "", 8)
        pdf.multi_cell(qr_size, 4, "Ce ticket est à présenter aux organisateurs\n afin d'obtenir une prévente bracelet", 0, "C")
        
        # Ajouter une nouvelle page si nécessaire
        if (i + 1) % 4 == 0 and i + 1 < len(qr_files):
            pdf.add_page()
    
    pdf.output(output_pdf)

# Utilisation
generate_pdf("qrcodes", "tickets.pdf")
