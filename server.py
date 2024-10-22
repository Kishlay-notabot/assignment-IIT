from flask import Flask, request, jsonify
from PIL import Image
import base64
import io
import contextlib
from tesseract import image_to_text, image_to_bboxes

app = Flask(__name__)

VALID_BBOX_TYPES = ["word", "line", "paragraph", "block", "page"]

def decode_base64_image(base64_string):
    try:
        #decode base64 and open as image
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))

        #convert to RGB if needed and return
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception:
        return None

def validate_image(image):
    if image is None:
        return False
    try:
        #check if it's a valid PIL Image
        return isinstance(image, Image.Image)
    except Exception:
        return False

@app.route('/api/get-text', methods=['POST'])
def get_text():
    #check for JSON data
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": {
                "message": "Content-Type must be application/json"
            }
        }), 400

    data = request.get_json()

    #check for base64_image in request
    if 'base64_image' not in data:
        return jsonify({
            "success": False,
            "error": {
                "message": "base64_image is required"
            }
        }), 400

    try:
        #decode base64 image
        image = decode_base64_image(data['base64_image'])

        # Validate image
        if not validate_image(image):
            return jsonify({
                "success": False,
                "error": {
                    "message": "Invalid base64_image."
                }
            }), 400

        #extract text using the same function as the test
        with contextlib.closing(image):
            text = image_to_text(image)

            return jsonify({
                "success": True,
                "result": {
                    "text": text
                }
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "message": str(e)
            }
        }), 500
    finally:
        #image closed or not
        if 'image' in locals():
            try:
                image.close()
            except:
                pass

@app.route('/api/get-bboxes', methods=['POST'])
def get_bboxes():
    #check for JSON data
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": {
                "message": "Content-Type must be application/json"
            }
        }), 400

    data = request.get_json()

    #check for required fields
    if 'base64_image' not in data or 'bbox_type' not in data:
        return jsonify({
            "success": False,
            "error": {
                "message": "base64_image and bbox_type are required"
            }
        }), 400

    #validate bbox_type
    if data['bbox_type'] not in VALID_BBOX_TYPES:
        return jsonify({
            "success": False,
            "error": {
                "message": "Invalid bbox_type."
            }
        }), 400

    try:
        #decode base64 image
        image = decode_base64_image(data['base64_image'])

        #validate image
        if not validate_image(image):
            return jsonify({
                "success": False,
                "error": {
                    "message": "Invalid base64_image."
                }
            }), 400

        #get bboxes
        with contextlib.closing(image):
            boxes = image_to_bboxes(image, data['bbox_type'])

            return jsonify({
                "success": True,
                "result": {
                    "bboxes": boxes
                }
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": {
                "message": str(e)
            }
        }), 500
    finally:
        #ensure image is closed if it exists
        if 'image' in locals():
            try:
                image.close()
            except:
                pass

if __name__ == '__main__':
    app.run(debug=True)