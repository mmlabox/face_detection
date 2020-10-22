import cv2 as cv
import edgeiq
import math

length = 12
width = 14

def get_distances(frame, predictions, text):
    for i in range(len(predictions)):
        scale = math.sqrt(predictions[i].box.area)/math.sqrt(length*width)
        for j in range(i+1, len(predictions)):
            dist = predictions[i].box.compute_distance(predictions[j].box)/scale

            # Draw some unnecessary lines between faces
            color = (66,245,93)
            cv.line(frame, (int(predictions[i].box.center[0]), int(predictions[i].box.center[1])), 
            (int(predictions[j].box.center[0]), int(predictions[j].box.center[1])), color, 6)

            if dist > 0.0:
                text.append("Distance between face " + str(i+1) + " and " + str(j+1) + ": {:.2f} " + " cm".format(dist))
    return (frame, text)