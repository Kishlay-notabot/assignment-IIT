# internship-assignment-IIT

### Steps to run the server code:
* Install Tesseract-OCR:
    - Linux: `sudo apt install tesseract-ocr`
    - Windows: Follow the installation steps provided in the documentation [here](https://tesseract-ocr.github.io/tessdoc/Installation.html)
* Setup a python virtual environment (optional)
* Clone the repository with `git clone https://github.com/Kishlay-notabot/assignment-IIT`  
* Change directory to the repo folder `cd internship-assignment-IIT`
* install dependencies for running server by `pip install -r requirements.txt`
* Start the server with `python server.py`
* Run the test with `python test.py`



# About the app

The python app above uses a Flask RESTful API as the server backend, PIL for image processing (basically converting to base64 back and forth) and has pytesseract as the dependency.

We have declared two wrapper functions in the file `tesseract.py` named `image_to_text` and `image_to_bboxes` which use the pytesseract `image_to_string()` function and `image_to_data()` respectively. Then it takes out the bbox (bounding box) data and outputs it in the specified format.


The server has two endpoints which accept image data as base64, and then give the following outputs:
- `/api/get-text`
    - gives the recognized text from the image
- `/api/get-bboxes`
    - gives the bounding box data of the content in the specified granularity (word, line, paragraph, block etc.)

There are 3 status codes which signal the success/failure of an operation:
* 200: Successful operation
* 400: Bad request (invalid input)
* 500: Server error
