import pytesseract
from PIL import Image

def image_to_text(image):
    """
    Convert image to text using Tesseract OCR.
    Args:
        image: PIL Image object
    Returns:
        str: Extracted text
    """
    return pytesseract.image_to_string(image)

def image_to_bboxes(image, bbox_type):
    """
    Extract bounding boxes from image using Tesseract OCR.
    Args:
        image: PIL Image object
        bbox_type: str, one of "word", "line", "paragraph", "block", or "page"
    Returns:
        list: List of dictionaries containing bounding box coordinates
    """
    bbox_type_map = {
        'word': 1,
        'line': 2,
        'paragraph': 3,
        'block': 4,
        'page': 5
    }

    # get data with bounding boxes
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    #filter boxes based on the specified level
    level = bbox_type_map[bbox_type]
    boxes = []

    for i in range(len(data['level'])):
        if data['level'][i] == level:
            boxes.append({
                'x_min': data['left'][i],
                'y_min': data['top'][i],
                'x_max': data['left'][i] + data['width'][i],
                'y_max': data['top'][i] + data['height'][i]
            })

    return boxes