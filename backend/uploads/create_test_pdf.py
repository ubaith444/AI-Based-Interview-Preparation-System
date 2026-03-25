from reportlab.pdfgen import canvas

def create_resume():
    c = canvas.Canvas("sample_resume.pdf")
    c.drawString(100, 750, "Sample Resume")
    c.drawString(100, 730, "John Doe")
    c.drawString(100, 710, "Experience: Software Engineer with 5 years of experience.")
    c.drawString(100, 690, "Skills: Python, FastAPI, JavaScript, React, SQL, MongoDB, Docker.")
    c.save()

if __name__ == "__main__":
    create_resume()
    print("Created sample_resume.pdf")
