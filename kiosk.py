"""
This file runs on a Raspberry Pi on the kiosk.
"""
import time
import cv2
from FacialRecognition.identify_face import FaceIdentifier


class Kiosk:

    def __init__(self, qr_code_camera_id, mugshot_camera_id):
        self.running = True
        self.looking_for_application = True
        self.qr_code_camera = cv2.VideoCapture(qr_code_camera_id) if qr_code_camera_id is not None else None
        self.mugshot_camera = cv2.VideoCapture(mugshot_camera_id) if mugshot_camera_id is not None else None
        self.face_identifier = FaceIdentifier()

    def check_for_qr_code(self):
        raise NotImplementedError()

    def process_image(self):
        # Grab a frame from the front-facing camera
        ret, frame = self.mugshot_camera.read()

        # Resolve the names of all the people in the frame
        faces = self.face_identifier.predict_from_cv2_frame(frame)
        names_in_frame = {name for name, loc in faces}

        # TODO: Look for a buffalo hat
        wearing_buffalo_hat = False

        return names_in_frame, wearing_buffalo_hat

    def check_application_with_server(self, application_id, name, is_wearing_hat):
        # TODO: Send the data to the server
        raise NotImplementedError()

    def handle_server_response(self, response):
        raise NotImplementedError()

    def run(self):
        while self.running:
            if self.looking_for_application:
                application_id = self.check_for_qr_code()
                if application_id is not None:
                    # TODO: Process app
                    pass

            time.sleep(0.5)


if __name__ == '__main__':
    Kiosk(qr_code_camera_id=None, mugshot_camera_id=0).run()
