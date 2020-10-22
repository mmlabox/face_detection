import cv2 as cv
import edgeiq
import numpy as np
import math

def get_distances(frame, predictions, text):
    #for prediction in predictions:
    for i in range(len(predictions)):
       # for other_pred in predictions:
       for j in range(i+1, len(predictions)):
            #if predictions[i] is not other_pred:
                color = (66,245,93)
                dist = predictions[i].box.compute_distance(predictions[j].box)

                cv.line(frame, (int(predictions[i].box.center[0]), int(predictions[i].box.center[1])), 
                (int(predictions[j].box.center[0]), int(predictions[j].box.center[1])), color, 6)

                if dist > 0.0:
                    text.append("Distance between face " + str(i+1) + " and " + str(j+1) + ": {:.2f} ".format(dist))
    return (frame, text)