# Import libraries
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
from werkzeug.datastructures import FileStorage


def process_file(file):
    # Path of the pdf
    PDF_file = "uploads/" + file.filename

    '''
    Part #1 : Converting PDF to images
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500)

    # Counter to store images of each page of PDF to image
    image_counter = 1

    # Iterate through all the pages stored above
    for page in pages:
        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        # ....
        # PDF page n -> page_n.jpg
        filename = "page_" + str(image_counter) + ".jpg"

        # Save the image of the page in system
        page.save(filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    '''
    Part #2 - Recognizing text from the images using OCR
    '''
    return ocr(image_counter, 1, image_counter - 1)


def ocr(image_counter, start, end):
    # Variable to get count of total number of pages
    filelimit = image_counter - 1

    # Creating a text file to write the output
    outfile = "out_text.txt"

    # Open the file in append mode so that
    # All contents of all images are added to the same file
    f = open(outfile, "a")
    f.truncate(0)
    # start = 1
    # end = filelimit
    assert (end <= filelimit)

    f.write("# coding: utf8\n")

    # Iterate from 1 to total number of pages
    for i in range(start, end + 1):
        # Set filename to recognize text from
        # Again, these files will be:
        # page_1.jpg
        # page_2.jpg
        # ....
        # page_n.jpg
        filename = "page_" + str(i) + ".jpg"

        # Recognize the text as string in image using pytesserct
        text = str((pytesseract.image_to_string(Image.open(filename))))

        # text = filter_gibberish(text)
        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')

        # Finally, write the processed text to the file.
        f.write(text)

    # Close the file after writing all the text.
    f.close()

    os.system("awk 'BEGIN { RS=\"\"; ORS=\"\\n\\n\"}{$1=$1}1' out_text.txt > text.txt")

    # Merging paragraphs/ formatting text from pdf
    # text = "awk 'BEGIN { RS=\"\"; ORS=\"\\n\\n\"}{$1=$1}1' out_text.txt > merged_blocks.txt"
    # print(text)
    file_loc = open('text.txt', 'rb')
    processed_file = FileStorage(file_loc)
    return processed_file
