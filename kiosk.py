"""
This file runs on a Raspberry Pi on the kiosk.
"""
import sys
sys.path = [p for p in sys.path if 'ros' not in p]
import time
import cv2
from arduino_comm import ArduinoComm
from FacialRecognition.identify_face import FaceIdentifier
from BuffaloHat.buffalo_detect import detectHat
from QRScan.scan import read_qr_code


class Kiosk:

    def __init__(self, qr_code_camera_id, mugshot_camera_id, facial_recognition_model_path, frame_rate=10):
        self.qr_code_camera = cv2.VideoCapture(qr_code_camera_id) if qr_code_camera_id is not None else None
        self.mugshot_camera = cv2.VideoCapture(mugshot_camera_id) if mugshot_camera_id is not None else None
        self.face_identifier = FaceIdentifier(facial_recognition_model_path)
        self.arduino_comm = ArduinoComm()
        self.frame_rate = frame_rate
        self.frames_left_to_drop = 0

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
        # Resolve the names of all the people in the frame
        faces = self.face_identifier.predict_from_cv2_frame(frame)
        names_in_frame = list({name for name, loc in faces})

        # Look for a buffalo hat
        wearing_buffalo_hat = detectHat(frame)

        return names_in_frame, wearing_buffalo_hat

    def check_application_with_server(self, application_id, names, is_wearing_hat):
        print('Checking with server')
        # TODO: Send the data to the server
        # Temporary behavior:
        if 'Kyle_Combes' in names or is_wearing_hat:
            print('verified')
            self.arduino_comm.approve()
            time.sleep(20)
        else:
            print('reject')
            self.arduino_comm.reject()
            time.sleep(5)

    def handle_server_response(self, response):
        raise NotImplementedError()

    def run(self):
        while True:
            self.check_cameras()


if __name__ == '__main__':
    Kiosk(qr_code_camera_id=1,
          mugshot_camera_id=0,
          facial_recognition_model_path='FacialRecognition/trained_knn_model.clf'
          ).run()
