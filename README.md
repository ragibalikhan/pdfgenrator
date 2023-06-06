# PDF Generator

This is a web application that generates a PDF document from a set of images and corresponding information provided in a data file. Users can upload images, enter information, and generate a PDF document containing the images and associated details.

## Live Web Application

You can access the live web application [here](https://pdf-genrator.onrender.com/).

## Setting up the Data

Before using the application, you need to structure your data appropriately. Follow these steps:

1. Create a file called `data.txt`.
2. Populate `data.txt` with the following information:

1, Videomate Banner, This a product known as the icon of Videomate, www.google.com
2, Videomate App Logo, This is also a product known as the App icon, www.google.com
3, Home Icon, This is a product known as an icon, but it is not the same, www.google.com
4, Videomate, This is a product known as the Videomate icon with an erased background, www.google.com
5, Home Icon 2, This is also a product known as an icon, www.google.com
6, Connect Logo, This is a product known as the Connect Fluence app icon, www.google.com

Each line represents an entry with the following structure: `id, title, info, link`. Use a comma (`,`) as the separator between each field. The `id` should correspond to the image number.

For example, the first line represents image number 1, titled "Videomate Banner," with the information "This a product known as the icon of Videomate." The `link` field should contain the URL associated with the image.

Ensure that the images referenced in `data.txt` are named according to their corresponding entry number. For instance, the image for the first entry should be named `1.png`, the second entry should have an image named `2.png`, and so on.

## Usage

1. Visit the live web application [here](https://pdf-genrator.onrender.com/).
2. Fill in the PDF title, image files, image width, and image height.
3. Upload the `data.txt` file and click on the "Generate PDF" button.
4. Once the PDF is generated, you can download it by clicking on the provided download link.

Please note that the generated PDF file and the uploaded images will be automatically deleted from the server after the download.

## Local Development

To set up the project locally and run it on your machine, follow these steps:

1. Clone the repository: `git clone https://github.com/ragibalikhan/pdf-generator.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the Flask application: `python main.py`
4. Access the application in your web browser at `http://localhost:5000`.

Make sure to have Python and Flask installed on your system.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
