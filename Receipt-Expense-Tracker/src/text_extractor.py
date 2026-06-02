import sys
import tf_keras
import math

sys.modules['tensorflow.keras'] = tf_keras
sys.modules['keras'] = tf_keras

import keras_ocr

def ocr(image_path):
    #initialize pipeline
    pipeline = keras_ocr.pipeline.Pipeline()

    #read image
    image = keras_ocr.tools.read(image_path)

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

def extract_text(image_path, thresh, order='yes'):
    predictions = ocr(image_path)
    predictions = get_distance(predictions)
    predictions = list(distinguish_rows(predictions, thresh))
    # Remove all empty rows
    predictions = list(filter(lambda x:x!=[], predictions))
    # Order text detections in human readable format
    ordered_preds = []
    ylst = ['yes', 'y']
    for pr in predictions:
        if order in ylst: 
            row = sorted(pr, key=lambda x:x['distance_from_origin'])
            for each in row: 
                ordered_preds.append(each['text'])
    return ordered_preds

final_text_flow = extract_text('Receipt_3.png', thresh=15, order='yes')
print(final_text_flow)