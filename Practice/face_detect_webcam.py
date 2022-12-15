"""
 face detection on webcam (laptops only)
 * @author:
 * uP2 - Fall 2022
"""
import cv2
import argparse
from time import sleep
import KalmanAssoc

from face_detect_img import face_detect, draw_face_boxes, draw_face_obj_boxes

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_path", type=str, default="data/webcam_out.mp4")
    parser.add_argument("--casc_Path", type=str, default="haarcascade_frontalface_default.xml")
    args = parser.parse_args()

    # get the paths
    out_video_name = args.out_path
    cascPath = args.casc_Path
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0) # 0 for webcam, this number will change for other ports
    out_video = cv2.VideoWriter(out_video_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (320, 240))

    # Save Past positions
    associator = KalmanAssoc.FaceAssociator(30, 100)

    while True:
        if not video_capture.isOpened():
            print('Unable to load camera.')
            sleep(5)
            pass

        ret, frame = video_capture.read()
        frame_resized = cv2.resize(frame, (320, 240))
        faces = face_detect(frame_resized, faceCascade)

        out_faces = associator.face_predict(faces)
        print("Status")
        print(str(len(associator.active_faces)) + ", " + str(len(associator.predicted_faces)) + ", " + str(len(faces)) + ", " + str(len(out_faces)))

        # image_out = draw_face_boxes(frame_resized, out_faces)
        image_out = draw_face_obj_boxes(frame_resized, associator.active_faces)

        # Display the resulting frame
        cv2.imshow('Video', image_out)
        out_video.write(image_out)

        # Press q to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    out_video.release()
    video_capture.release()
    cv2.destroyAllWindows()
