from fpdf import FPDF
from fpdf.enums import XPos, YPos  # Import the new enum values


class PDF(FPDF):
    def __init__(self, orientation="portrait", unit="mm", format="A4"):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('NotoSans', '', 'assets/NotoSans.ttf')
        self.set_font("NotoSans", size=11)
        self.add_page()
        # Ensure the font is added before using it
    def header(self):
        self.image("assets/11.png", x=50, y=8, w=25, h=25)
        self.set_y(15)
        self.set_x(80)
        self.cell(0, 10, "TA.L.A. (Tagalog Lemmatizer Algorithm)", align="L")
        self.ln(30)

    def add_list(self, items):
        # Add the list of items to the PDF
        self.multi_cell(0, 7, f"{items}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        self.set_font("helvetica", style="I", size=12)
        self.set_text_color(169, 169, 169)  # Set font color to grey
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


if __name__ == "__main__":
    # Create PDF object
    pdf = PDF()
    text = "This is a test document with Unicode support. “"
    pdf.add_list(text)
    pdf.output("output.pdf")