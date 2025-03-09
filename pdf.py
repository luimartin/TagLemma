from fpdf import FPDF
from fpdf.enums import XPos, YPos  # Import the new enum values
    
class pdf(FPDF):
    # Layout ('P','L')
    # Unit ('mm', 'cm', 'in')
    # format ('A3', 'A4' (default), 'A5', 'Letter', 'Legal', (100,150))
    # (layout, unit, format)
    def __init__(self, orientation = "portrait", unit = "mm", format = "A4"):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(auto = True, margin = 15)
        # required to instatiate
        self.add_page()
        self.set_font('times', '', 12)
    
    def add_list(self, items):
        # cell arguments(width, height(space between cells), content, xpos = x cursor position, ypos = y cursor position)
        self.multi_cell(0, 7, f"{items}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
    def footer(self):
        # Set position of the footer
        self.set_y(-15)
        # set font
        self.set_font('helvetica', 'I', 12)
        # Set font color grey
        self.set_text_color(169,169,169)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', align='C')
        
if __name__ == "__main__":
    # create FPDF object
    pdf = pdf()
    list = []
    for i in range(1, 41):
        list.append(f'This is line {i} :D')
    pdf.add_list(list)
    pdf.output('pdf_2.pdf')