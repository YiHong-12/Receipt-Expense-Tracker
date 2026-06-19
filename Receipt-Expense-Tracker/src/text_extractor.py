import sys
import tf_keras
import math
import cv2

import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(4)
tf.config.threading.set_inter_op_parallelism_threads(4)

sys.modules['tensorflow.keras'] = tf_keras
sys.modules['keras'] = tf_keras

import keras_ocr

#initialize pipeline
print("Loading OCR models into memory...")
pipeline = keras_ocr.pipeline.Pipeline()
print("Models loaded successfully.")

def ocr(image_path, pipeline):
    print("Starting to read image and extract text...")

    #read image
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not open or find the image: {image_path}.")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    max_width = 1000
    
    # Check if the image width (shape[1]) is larger than our max limit
    if image.shape[1] > max_width:
        # Calculate the scale factor to maintain the aspect ratio
        scale = max_width / image.shape[1]
        new_width = int(image.shape[1] * scale)
        new_height = int(image.shape[0] * scale)
        
        # Resize using INTER_AREA, which is best for shrinking images
        image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        print(f"--> Image resized to {new_width}x{new_height} to speed up processing.")

    #store predictions in a list of tuples (text, box_coordinates) tuples
    prediction_groups = pipeline.recognize([image])

    return prediction_groups[0]


#sorting function: https://shegocodes.medium.com/extract-text-from-image-left-to-right-and-top-to-bottom-with-keras-ocr-b56f098a6efe
def get_distance(predictions):
    #origin point
    x0, y0 = 0, 0

    #Generate dictionary
    detections = []

    for group in predictions:
        # Get center point of bounding box
        top_left_x, top_left_y = group[1][0]
        bottom_right_x, bottom_right_y = group[1][1]
        center_x = (top_left_x + bottom_right_x) / 2
        center_y = (top_left_y + bottom_right_y) / 2
        # Use the Pythagorean Theorem to solve for distance from origin
        distance_from_origin = math.dist([x0,y0], [center_x, center_y])
        # Calculate difference between y and origin to get unique rows
        distance_y = center_y - y0
        # Append all results
        detections.append({
                            'text':group[0],
                            'center_x':center_x,
                            'center_y':center_y,
                            'distance_from_origin':distance_from_origin,
                            'distance_y':distance_y
                        })
    return detections

def distinguish_rows(lst, thresh=15):
    #Function to help distinguish unique rows
    
    sublists = [] 
    for i in range(0, len(lst)-1):
        if lst[i+1]['distance_y'] - lst[i]['distance_y'] <= thresh:
            if lst[i] not in sublists:
                sublists.append(lst[i])
            sublists.append(lst[i+1])
        else:
            yield sublists
            sublists = [lst[i+1]]
    yield sublists

def extract_text(image_path, thresh,pipeline):
    predictions = ocr(image_path, pipeline)
    predictions = get_distance(predictions)

    #Sort by Y-coordinate
    predictions = sorted(predictions, key=lambda x: x['distance_y'])

    #Group into distinct rows
    predictions = list(distinguish_rows(predictions, thresh))
    predictions = list(filter(lambda x:x!=[], predictions))
   
    ordered_rows = []

    for row_index,pr in enumerate(predictions):
        #sort words in this specific row
        sorted_row = sorted(pr, key=lambda x: x['center_x'])

        row_data = {
            'row_index': row_index,
            'data':[{'text': item['text'], 'x':item['center_x']} for item in sorted_row] 
        }
        ordered_rows.append(row_data)

    return ordered_rows

extracted_text = extract_text('Receipt_1.jpg', 15, pipeline)
print(extracted_text)