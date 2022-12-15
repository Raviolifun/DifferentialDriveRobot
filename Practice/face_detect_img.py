"""
 face detection on images
 * @author:
 * uP2 - Fall 2022
"""
import cv2
import sys
import argparse


def face_detect(image, faceCascade):
    """
        Inputs: image (numpy array) and faceCascade XML model
        Output: faces (https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Detect faces in an image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def draw_face_boxes(image, faces):
    # draw bounding boxes for all faces in image
    if faces is None:
        return image
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return image


def draw_face_obj_boxes(image, faces):
    # draw bounding boxes for all faces in image
    if faces is None:
        return image
    for face in faces:
        cv2.rectangle(image, (face.x, face.y), (face.x + face.w, face.y + face.h), (0, 255, 0), 2)
        cv2.putText(image, str(face.ID), (face.x, face.y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
    return image


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", type=str, default="data/test_image.png")
    parser.add_argument("--casc_Path", type=str, default="haarcascade_frontalface_default.xml")
    args = parser.parse_args()

    # Get user supplied values
    imagePath = args.img_path
    cascPath = args.casc_Path
    image = cv2.imread(args.img_path)

    if image is None:
        print ("Image is not found!")
    else:
        # Create the haar cascade
        faceCascade = cv2.CascadeClassifier(cascPath)
        faces = face_detect(image, faceCascade)
        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        image = draw_face_boxes(image, faces)
        out_im_name = imagePath.replace(".", "_out.")
        cv2.imwrite(out_im_name, image)
        print("Saved image: {0}".format(out_im_name))
