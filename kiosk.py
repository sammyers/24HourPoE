"""
This file runs on a Raspberry Pi on the kiosk.
"""
import sys
sys.path = [p for p in sys.path if 'ros' not in p]
import requests
import time
import cv2
from arduino_comm import ArduinoComm
from FacialRecognition.identify_face import FaceIdentifier
from BuffaloHat.buffalo_detect import detectHat
from QRScan.scan import read_qr_code


class Kiosk:

    def __init__(self, qr_code_camera_id, mugshot_camera_id, facial_recognition_model_path, verification_endpoint, frame_rate=10):
        self.qr_code_camera = cv2.VideoCapture(qr_code_camera_id) if qr_code_camera_id is not None else None
        self.mugshot_camera = cv2.VideoCapture(mugshot_camera_id) if mugshot_camera_id is not None else None
        self.face_identifier = FaceIdentifier(facial_recognition_model_path)
        self.frame_rate = frame_rate
        self.frames_left_to_drop = 0
        self.verification_endpoint = verification_endpoint
        self.arduino_comm = ArduinoComm()

    def check_cameras(self):
        # Grab a frame from the QR code camera
        _, qr_frame = self.qr_code_camera.read()
        # Grab a frame from the mugshot camera (to prevent the buffer from filling up)
        _, ms_frame = self.mugshot_camera.read()

        # Check if we're supposed to ignore this frame
        if self.frames_left_to_drop > 0:
            self.frames_left_to_drop -= 1
        else:
            self.frames_left_to_drop = self.frame_rate

            # Check the visa document camera for a QR code on a document
            application_id = read_qr_code(qr_frame)

            if application_id is not None:
                print('Read QR code. Verifying identity...')
                names_in_frame, wearing_hat = self.check_identity(ms_frame)
                self.check_application_with_server(application_id, names_in_frame, wearing_hat)
            else:
                print('No QR code found.')

    def check_identity(self, frame):
        names_in_frame = dict()

        # Take 5 readings to get a more accurate idea of who is in the frame
        for _ in range(5):
            # Resolve the names of all the people in the frame
            faces = self.face_identifier.predict_from_cv2_frame(frame)
            names = {name for name, loc in faces}
            for name in names:
                if name in names_in_frame:
                    names_in_frame[name] += 1
                else:
                    names_in_frame[name] = 1

        # Only keep names that have appeared a lot
        names_in_frame = [name for name, count in names_in_frame.items() if count > 3]

        # Look for a buffalo hat
        wearing_buffalo_hat = detectHat(frame)

        return names_in_frame, wearing_buffalo_hat

    def check_application_with_server(self, application_id, names, is_wearing_hat):
        print('Checking with server')
        # TODO: Send the data to the server
        request_params = {
            'qrId': application_id,
            'wearingHat': is_wearing_hat,
            'names': names,
        }
        response = requests.post(self.verification_endpoint, json=request_params)
        if response.ok:
            result = response.json()
            if result['admitted']:
                print('Application approved')
                # self.arduino_comm.approve()
            else:
                print('Application denied')
                # self.arduino_comm.reject()

    def run(self):
        while True:
            self.check_cameras()


if __name__ == '__main__':
    Kiosk(qr_code_camera_id=1,
          mugshot_camera_id=0,
          facial_recognition_model_path='FacialRecognition/trained_knn_model.clf',
          verification_endpoint='http://10.7.24.49:5000/check-application'
          ).run()
