import cv2 as cv
import edgeiq
from math import sqrt, pow

# Average length and width of a human face
length = 12
width = 14

def get_distances(frame, predictions, text):
    for i in range(len(predictions)):
        scale_1 = sqrt(predictions[i].box.area)/sqrt(length*width)

        for j in range(i+1, len(predictions)):
            # scale_2 = sqrt(predictions[j].box.area)/sqrt(length*width)
            eucl_dist = predictions[i].box.compute_distance(predictions[j].box)
            dist = eucl_dist / scale_1

            # Draw some unnecessary lines between faces
            # color = (66,245,93)
            # cv.line(frame, (int(predictions[i].box.center[0]), int(predictions[i].box.center[1])), 
            # (int(predictions[j].box.center[0]), int(predictions[j].box.center[1])), color, 6)

            text.append("Distance in cm between face " + str(i+1) + " and " + str(j+1) + ": {:.2f} cm".format(dist))
    return (frame, text)