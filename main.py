import os
from tkinter import *
from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak

class BookGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.document = SimpleDocTemplate(self.filename, pagesize=A4)
        self.elements = []
        self.styles = getSampleStyleSheet()
        self.page_number = 0

    def add_text(self, text):
        """Adds text to the document."""
        paragraph = Paragraph(text, self.styles['Normal'])
        self.elements.append(paragraph)
        self.elements.append(Spacer(1, 0.2 * inch)) 

    def add_image(self, image_path, width=2 * inch):
        """Adds an image to the document."""
        img = Image(image_path, width=width, height=None)  
        self.elements.append(img)
        self.elements.append(Spacer(1, 0.2 * inch)) 

    def add_page_number(self):
        """Adds a page number to the document."""
        self.page_number += 1
        self.elements.append(Paragraph(f"Page {self.page_number}", self.styles['Normal']))

    def build(self):
        """Builds the PDF document."""
        self.document.build(self.elements, onFirstPage=self._on_page)

    def _on_page(self, canvas, doc):
        """Callback for adding content to each page."""
        canvas.saveState()
        canvas.drawString(500, 10, f"Page {self.page_number}")  
        canvas.restoreState()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Book Generator")
        
        self.book = None
        self.create_widgets()

    def create_widgets(self):
        Label(self.root, text="Enter Text:").pack(pady=5)
        self.text_entry = Text(self.root, height=5, width=40)
        self.text_entry.pack(pady=5)

        Button(self.root, text="Add Text", command=self.add_text).pack(pady=5)

        Button(self.root, text="Add Image", command=self.add_image).pack(pady=5)

        Button(self.root, text="Generate PDF", command=self.generate_pdf).pack(pady=20)

        self.filename_entry = Entry(self.root, width=40)
        self.filename_entry.pack(pady=5)
        self.filename_entry.insert(0, "output_book.pdf")

    def add_text(self):
        text = self.text_entry.get("1.0", END).strip()
        if text:
            if self.book is None:
                self.book = BookGenerator(self.filename_entry.get())
            self.book.add_text(text)
            self.text_entry.delete("1.0", END)
            messagebox.showinfo("Success", "Text added!")
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def add_image(self):
        image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if image_path:
            if self.book is None:
                self.book = BookGenerator(self.filename_entry.get())
            self.book.add_image(image_path)
            messagebox.showinfo("Success", "Image added!")

    def generate_pdf(self):
        if self.book is not None:
            self.book.add_page_number()  
            self.book.build()
            messagebox.showinfo("Success", f"PDF generated: {self.filename_entry.get()}")
        else:
            messagebox.showwarning("Error", "No content to generate PDF.")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
