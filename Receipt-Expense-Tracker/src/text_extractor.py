import keras_ocr

def extract_raw_text(image_path):
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read(image_path)]
    preds = pipeline.recognize(images)[0]

    # Sort by top to bottom, then left to right (natural reading order)
    preds.sort(key=lambda x: (x[1][0][1], x[1][0][0]))
    
    return [word for word, _ in preds]
