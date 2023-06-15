import cv2
import os
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from PIL import Image


def detect_faces_in_dataset():
    face_classifier = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml")

    dataset_dir = "../static/Images"  # Directory containing the images
    face_dataset_dir = "../static/face_dataset"  # Directory to save the detected face images

    if not os.path.exists(face_dataset_dir):
        os.makedirs(face_dataset_dir)

    for filename in os.listdir(dataset_dir):
        if filename.endswith(".jpg"):
            img_path = os.path.join(dataset_dir, filename)
            img = cv2.imread(img_path)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    face_img = img[y:y+h, x:x+w]
                    face_img = cv2.resize(face_img, (200, 200))
                    face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
                    
                    face_file_path = os.path.join(face_dataset_dir, filename)
                    cv2.imwrite(face_file_path, face_img)

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.destroyAllWindows()

def train_classifier():
    dataset_dir = "../static/face_dataset"

    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)
    ids = np.array(ids)

    # Train the classifier and save
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("../classifier.xml")

    return {'status': 'success'}
