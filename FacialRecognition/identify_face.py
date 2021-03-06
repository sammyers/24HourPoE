"""
This code is taken from GitHub user ageitgey's face_recognition/examples/face_recognition_knn.py.

This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.
When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.
Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under eucledian distance)
in its training set, and performing a majority vote (possibly weighted) on their label.
For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.
* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.
Usage:
1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.
2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.
3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.
NOTE: This example requires scikit-learn to be installed! You can install it with pip:
$ pip3 install scikit-learn
"""

import sys
sys.path = [p for p in sys.path if 'ros' not in p]
import math
from sklearn import neighbors
import os.path
import pickle
import cv2
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

ALLOWED_EXTENSIONS = {'jpg'}


class FaceIdentifier:

    def __init__(self, model_save_path=None):
        self.model_save_path = model_save_path

        # Load the KNN model
        self.knn_clf = None
        if os.path.isfile(model_save_path):
            with open(model_save_path, 'rb') as f:
                self.knn_clf = pickle.load(f)

    def train(self, train_dir, n_neighbors=None, knn_algo='ball_tree', verbose=False):
        """
        Trains a k-nearest neighbors classifier for face recognition.
        :param train_dir: directory that contains a sub-directory for each known person, with its name.
         (View in source code to see train_dir example tree structure)
         Structure:
            <train_dir>/
            /-- <person1>/
            /   /-- <somename1>.jpeg
            /   /-- <somename2>.jpeg
            /   /-- ...
            /-- <person2>/
            /   /-- <somename1>.jpeg
            /   /-- <somename2>.jpeg
            /-- ...
        :param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
        :param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
        :param verbose: verbosity of training
        :return: returns knn classifier that was trained on the given data.
        """
        X = []
        y = []

        # Loop through each person in the training set
        for class_dir in os.listdir(train_dir):
            if not os.path.isdir(os.path.join(train_dir, class_dir)):
                continue

            # Loop through each training image for the current person
            for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
                image = face_recognition.load_image_file(img_path)
                face_bounding_boxes = face_recognition.face_locations(image)

                if len(face_bounding_boxes) != 1:
                    # If there are no people (or too many people) in a training image, skip the image.
                    if verbose:
                        print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                else:
                    # Add face encoding for current image to the training set
                    X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                    y.append(class_dir)

        # Determine how many neighbors to use for weighting in the KNN classifier
        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(X))))
            if verbose:
                print("Chose n_neighbors automatically:", n_neighbors)

        # Create and train the KNN classifier
        self.knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
        self.knn_clf.fit(X, y)

        # Save the trained KNN classifier
        if self.model_save_path:
            with open(self.model_save_path, 'wb') as f:
                pickle.dump(self.knn_clf, f)

    def predict_from_cv2_frame(self, frame, distance_threshold=0.6):
        """
        Recognizes faces in given image using a trained KNN classifier
        :param X_img_path: path to image to be recognized
        :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
               of mis-classifying an unknown person as a known one.
        :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """
        if self.knn_clf is None:
            raise Exception('Model must be loaded or trained before making predictions.')

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        if len(face_encodings) == 0:
            return []

        # Use the KNN model to find the best matches for the test face
        closest_distances = self.knn_clf.kneighbors(face_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(face_encodings))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
                 zip(self.knn_clf.predict(face_encodings), face_locations, are_matches)]

    def frame_contains_person(self, frame, full_name):
        """
        Checks a cv2 frame to see if it contains a particular person.
        :param frame: the cv2 frame
        :param full_name: the person's full name (e.g. William George-Sampo)
        :return: whether or not that person is in the frame
        """
        for name, _ in self.predict_from_cv2_frame(frame):
            if name == full_name:
                return True
        return False


if __name__ == "__main__":
    from time import sleep
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    identifier = FaceIdentifier(model_save_path="trained_knn_model.clf")
    print("Training KNN classifier...")
    identifier.train("train", n_neighbors=2)
    print("Training complete!")

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        faces = identifier.predict_from_cv2_frame(frame)

        # Display results overlaid on an image
        for name, (top, right, bottom, left) in faces:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            name = name.replace('_', ' ')
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        sleep(0.5)

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
