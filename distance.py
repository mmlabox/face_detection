import edgeiq
import pandas as pd
from math import sqrt, pow
import time

# Average length and width of a human face
length = 12
width = 14

def get_distances(frame, predictions, text):
    faces = []
    other_faces = []
    distances = []
    times = []
    n = len(predictions)
    for i in range(n):
        scale_1 = sqrt(predictions[i].box.area)/sqrt(length*width)

        for j in range(i+1, n):
            # scale_2 = sqrt(predictions[j].box.area)/sqrt(length*width)
            eucl_dist = predictions[i].box.compute_distance(predictions[j].box)
            dist = eucl_dist / scale_1
           
            faces.append(i+1)
            other_faces.append(j+1)
            distances.append(dist)
            times.append(time.time())
            text.append("Distance in cm between face " + str(i+1) + " and " + str(j+1) + ": {:.2f} cm".format(dist))
    
    d = {'face': faces, 'other face': other_faces, 'dist': distances}
    df = pd.DataFrame(data=d, index=pd.to_datetime(times, unit='s', origin='unix'))
    return (frame, text, df)