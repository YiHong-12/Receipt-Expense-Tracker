import keras_ocr

# Keras OCR from:https://pypi.org/project/keras-ocr/
print("[SYSTEM] Booting up Keras-OCR Engine. Please wait...")
pipeline = keras_ocr.pipeline.Pipeline()
print("[SYSTEM] OCR Engine is ready!")

def extract_raw_text(image_path):
    images = [keras_ocr.tools.read(image_path)]
    preds = pipeline.recognize(images)[0]

    # Sort by top to bottom, then left to right (natural reading order)
    preds.sort(key=lambda x: (x[1][0][1], x[1][0][0]))
    
    extracted_words = [word for word, _ in preds]

    return extracted_words
