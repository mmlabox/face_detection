import time
import edgeiq
from distance import *

def main():
    facial_detector = edgeiq.ObjectDetection(
            "alwaysai/res10_300x300_ssd_iter_140000")
    facial_detector.load(engine=edgeiq.Engine.DNN)

    print("Engine: {}".format(facial_detector.engine))
    print("Accelerator: {}\n".format(facial_detector.accelerator))
    print("Model:\n{}\n".format(facial_detector.model_id))

    fps = edgeiq.FPS()

    try:
        with edgeiq.WebcamVideoStream(cam=0) as webcam, \
                edgeiq.Streamer() as streamer:
            time.sleep(2.0)
            fps.start()

            while True:
                frame = webcam.read()
                text = [""]
                face = 1
                
                results = facial_detector.detect_objects(
                        frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                        frame, results.predictions, colors=facial_detector.colors)

                for prediction in results.predictions:
                    text.append("{}: {:2.2f}%".format(
                        prediction.label + " " + str(face), prediction.confidence * 100))
                    text.append("Position: " + str(face) + " {}" .format(prediction.box.center))
                    face += 1
                face = 0

                if len(results.predictions) > 0:
                    (frame, text) = get_distances(frame, results.predictions, text)

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
