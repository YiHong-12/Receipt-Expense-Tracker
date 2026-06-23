import keras_ocr

# Keras OCR from:https://pypi.org/project/keras-ocr/
print("[SYSTEM] Booting up Keras-OCR Engine. Please wait...")
pipeline = keras_ocr.pipeline.Pipeline()
print("[SYSTEM] OCR Engine is ready!")

def extract_raw_text(image_path):
    images = [keras_ocr.tools.read(image_path)]
    preds = pipeline.recognize(images)[0]

    extracted_words = []
    for word, box in preds:
        # Extract all x and y coordinates from bounding box
        ys = [pt[1] for pt in box]
        xs = [pt[0] for pt in box]
        # Save structured result for each detected word
        extracted_words.append({
            "word": word,
            "y_min": float(min(ys)),
            "y_max": float(max(ys)),
            "x_min": float(min(xs)),
            "x_max": float(max(xs))
        })

    return extracted_words