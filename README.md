# PDF to Bionic PDF Converter

This Python script converts a standard PDF file into a "bionic reading" format. Bionic reading is a technique that guides the reader's eye by bolding the initial letters of each word, which some find enhances reading speed and comprehension.

This script processes the text content of each page in the input PDF, applies the bionic formatting, and then reconstructs a new PDF with the modified text, while also preserving any images present in the original document.

## Features

* **Converts PDF text to bionic format:** Bolds the first few letters of each word.
* **Adjustable bold character count:** The script currently bolds the first 3 characters of words longer than 3 letters (and the entire word if it's shorter). You can easily modify this in the code.
* **Preserves images:** Images from the original PDF are extracted and included in the output bionic PDF.
* **Simple command-line interface:** Just run the script and provide the path to your PDF file.

## Prerequisites

Before running the script, ensure you have the necessary Python libraries installed. You can install them using pip:

```bash
pip install PyMuPDF reportlab PyPDF2
