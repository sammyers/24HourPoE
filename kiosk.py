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
from QRScan.scan import decode


class Kiosk:

    def __init__(self, qr_code_camera_id, mugshot_camera_id, facial_recognition_model_path):
        self.running = True
        self.looking_for_application = True
        self.qr_code_camera = cv2.VideoCapture(qr_code_camera_id) if qr_code_camera_id is not None else None
        self.mugshot_camera = cv2.VideoCapture(mugshot_camera_id) if mugshot_camera_id is not None else None
        self.face_identifier = FaceIdentifier(facial_recognition_model_path)
        self.arduino_comm = ArduinoComm()

    def check_for_qr_code(self):
        # Grab a frame from the QR code camera
        _, frame = self.qr_code_camera.read()

        qr_codes = decode(frame)
        if len(qr_codes) == 0:
            return None
        return qr_codes[0].data.decode()

    def process_image(self):
        # Grab a frame from the front-facing camera
        _, frame = self.mugshot_camera.read()

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
        while self.running:
            if self.looking_for_application:
                application_id = self.check_for_qr_code()
                if application_id is not None:
                    print('Read QR code:', application_id)

                    names_in_frame, wearing_hat = self.process_image()
                    print('Names in frame:', names_in_frame)
                    print('Wearing hat:', wearing_hat)
                    self.check_application_with_server(application_id, names_in_frame, wearing_hat)

            time.sleep(0.5)


if __name__ == '__main__':
    Kiosk(qr_code_camera_id=1,
          mugshot_camera_id=0,
          facial_recognition_model_path='FacialRecognition/trained_knn_model.clf'
          ).run()
