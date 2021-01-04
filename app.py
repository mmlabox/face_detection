import time
import edgeiq
import pandas as pd
from distance import *
from influxdb import DataFrameClient
import environ


def main():
    env = environ.Env()
    environ.Env.read_env()
    host = env('DB_HOST')
    port = env('DB_PORT')
    database = env('DB_DATABASE')
    username = env('DB_USER')
    password = env('DB_PASSWORD')
    measurement = env('DB_MEASUREMENT')

    facial_detector = edgeiq.ObjectDetection(
            "alwaysai/res10_300x300_ssd_iter_140000")
    facial_detector.load(engine=edgeiq.Engine.DNN)

    print("Engine: {}".format(facial_detector.engine))
    print("Accelerator: {}\n".format(facial_detector.accelerator))
    print("Model:\n{}\n".format(facial_detector.model_id))

    client = DataFrameClient(host=host, port=port, database=database, username=username, password=password)

    # Uses streamer to stream video and output to be viewed in browser (localhost:5000)
    # Temporary for developing/testing purposes, can be removed once connected to timeflux/influx etc (output = dataframe)

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as webcam, \
                edgeiq.Streamer() as streamer:
            time.sleep(2.0)
            fps.start()

            while True:
                frame = webcam.read()
                text = [""]
                face = 0
                d = []
                
                results = facial_detector.detect_objects(
                        frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                        frame, results.predictions, colors=facial_detector.colors)


                for prediction in results.predictions:
                    face += 1
                    text.append("{}: {:2.2f}%".format(
                        prediction.label + " " + str(face), prediction.confidence * 100))
                    
                text.append("Number of faces detected: " + str(face))

                if len(results.predictions) > 1:
                    (frame, text, df) = get_distances(frame, results.predictions, text)
                    print(df)
                    client.write_points(df, measurement, batch_size=1000)

                streamer.send_data(frame, text)
                fps.update()

                if streamer.check_exit():
                    break

    finally:
        fps.stop()
        text.append("FPS:".format(fps.compute_fps))

        print("[INFO] elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
