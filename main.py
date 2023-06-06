from flask import Flask, render_template, request, send_file, url_for
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from PIL import Image

app = Flask(__name__)


def generate_pdf(pdf_title, image_folder, text_file, output_file, image_width, image_height):
    c = canvas.Canvas(output_file, pagesize=letter)

    c.setFont("Helvetica", 16)
    c.setFillColor(colors.HexColor("#ADD8E6"))
    c.drawString(50, 750, f"{pdf_title}")

    image_files = get_image_files(image_folder)
    text_data = read_text_file(text_file)

    page_counter = 1  # Keep track of the number of pages

    for i, (image_id, image_path) in enumerate(image_files):
        if i >= len(text_data):
            break

        if i > 0 and i % 3 == 0:
            # If the current image count is a multiple of 3, add a new page
            c.showPage()
            page_counter += 1

        if page_counter > 1:
            # If it's not the first page, set the PDF title again at the top
            c.setFont("Helvetica", 16)
            c.setFillColor(colors.HexColor("#ADD8E6"))
            c.drawString(50, 750, f"{pdf_title} - Page {page_counter}")

        # Adjust the image size to fit on the right side
        c.drawImage(image_path, 50, 600 - (i % 3) * 200, width=image_width, height=image_height)

        # Calculate the positions for title, information, and link
        image_x = 50
        image_y = 600 - (i % 3) * 200
        title_x = image_x + image_width + 20
        title_y = image_y + image_height / 2 + 20

        # Set the title color
        c.setFillColor(colors.HexColor("#ADD8E6"))

        # Draw the title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(title_x, title_y, f"{text_data[i]['title']}")

        # Set the information style (bold)
        info_style = ParagraphStyle('info_style')
        info_style.fontName = 'Helvetica-Bold'
        info_style.fontSize = 12
        info_style.leading = 14

        # Calculate the available space for information and link
        available_height = title_y - (image_y - 20)
        info_height = 0.5 * available_height
        link_height = 0.3 * available_height

        # Calculate the positions for information and link
        info_x = title_x
        info_y = title_y - info_height - 10
        link_x = info_x
        link_y = info_y - link_height - 10

        # Draw the information
        info = Paragraph(f"Information: {text_data[i]['info']}", info_style)
        info.wrap(300, info_height)
        info.drawOn(c, info_x, info_y)

        # Set the link style (underlined)
        link_style = ParagraphStyle('link_style')
        link_style.fontName = 'Helvetica'
        link_style.fontSize = 12
        link_style.leading = 14
        link_style.textColor = colors.blue
        link_style.underline = 1

        # Draw the link
        link = Paragraph(f"Link: <u>{text_data[i]['link']}</u>", link_style)
        link.wrap(300, link_height)
        link.drawOn(c, link_x, link_y)

    c.save()


def get_image_files(folder):
    image_files = []
    for file in os.listdir(folder):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            image_id = os.path.splitext(file)[0]  # Extract the ID from the file name
            image_files.append((image_id, os.path.join(folder, file)))
    return image_files


def get_image_dimensions(image_path):
    img = Image.open(image_path)
    return img.width, img.height


def read_text_file(text_file):
    text_data = []
    with open(text_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                image_id, title, info, link = line.split(',')
                text_data.append({
                    'id': image_id.strip(),
                    'title': title.strip(),
                    'info': info.strip(),
                    'link': link.strip()
                })
    return text_data


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_title = request.form['pdf_title']
        image_files = request.files.getlist('image_files')
        text_file = request.files['text_file']
        image_width = int(request.form['image_width'])
        image_height = int(request.form['image_height'])

        # Save uploaded files
        image_folder = 'images'
        text_file_path = os.path.join(app.root_path, text_file.filename)
        image_folder_path = os.path.join(app.root_path, image_folder)

        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        text_file.save(text_file_path)
        for image_file in image_files:
            image_file_path = os.path.join(image_folder_path, image_file.filename)
            image_file.save(image_file_path)

        output_file = f"{pdf_title}.pdf"
        generate_pdf(pdf_title, image_folder_path, text_file_path, output_file, image_width, image_height)

        # Provide download link for the generated PDF file
        download_url = url_for('download', filename=output_file)
        return render_template('success.html', download_url=download_url)

    return render_template('home.html')


@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.root_path, filename)
    try:
        # Send the file to the user for download
        response = send_file(file_path, as_attachment=True)

        # Delete the images and data.txt file
        image_folder_path = os.path.join(app.root_path, 'images')
        text_file_path = os.path.join(app.root_path, 'data.txt')

        if os.path.exists(image_folder_path):
            for file in os.listdir(image_folder_path):
                file_path = os.path.join(image_folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(image_folder_path)

        if os.path.exists(text_file_path):
            os.remove(text_file_path)

        # Delete the generated PDF file
        if os.path.exists(file_path):
            os.remove(file_path)

        return response
    except Exception as e:
        # Handle any errors that occur during file deletion
        return str(e)


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


if __name__ == '__main__':
    app.run(debug=True)
