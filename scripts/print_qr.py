from fpdf import FPDF
from PIL import Image
import os


def generate_pdf(qr_folder: str, output_pdf: str) -> None:
    """
    Generate a PDF file with the QR codes from the given folder.

    Args:
    qr_folder (str): The folder containing the QR code images.
    output_pdf (str): The output PDF file.
    """
    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    qr_size = 80  # QR code size in mm
    page_width = 210
    page_height = 297

    # Calcul positions to center QR codes on the page
    center_x = [page_width * 0.25, page_width * 0.75]
    center_y = [page_height * 0.25, page_height * 0.75]

    title_font_size = 14
    text_font_size = 10

    qr_files = [f for f in os.listdir(qr_folder) if f.endswith(".png")]
    qr_files.sort()  # Sort the files for consistency

    positions = [(x, y) for y in center_y for x in center_x]

    for i, qr_file in enumerate(qr_files):
        x, y = positions[i % 4]  # Position on the page

        # Center each QR code on a quarter of the page
        x -= qr_size / 2
        y -= qr_size / 2

        # Extract the ticket number from the file name
        ticket_number = os.path.splitext(qr_file)[0]

        # Add a title
        pdf.set_xy(x, y - 25)
        pdf.set_font("Arial", "B", title_font_size)
        pdf.cell(qr_size, 5, "Bal des bières 2025", 0, 1, "C")

        # Add "TICKET"
        pdf.set_xy(x, y - 15)
        pdf.set_font("Arial", "B", text_font_size)
        pdf.cell(qr_size, 5, f"TICKET {ticket_number}", 0, 1, "C")

        # Add the QR code
        pdf.image(os.path.join(qr_folder, qr_file), x, y, qr_size, qr_size)

        # Add the text below the QR code
        pdf.set_xy(x, y + qr_size + 5)
        pdf.set_font("Arial", "", 8)
        pdf.multi_cell(
            qr_size, 4, "Ce ticket est à présenter aux organisateurs\n afin d'obtenir une prévente bracelet", 0, "C")

        # Add a page break every 4 tickets
        if (i + 1) % 4 == 0 and i + 1 < len(qr_files):
            pdf.add_page()

    pdf.output(output_pdf)


if __name__ == "__main__":
    generate_pdf("qrcodes", "tickets.pdf")
