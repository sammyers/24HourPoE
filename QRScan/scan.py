from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2


def read_qr_code(frame):
    detected_objects = pyzbar.decode(frame)
    if len(detected_objects) == 0:
        return None
    return detected_objects[0].data.decode()


# Display barcode and QR code location
def display(im, decoded_objects):
    points = []
    # Loop over all decoded objects
    for decodedObject in decoded_objects:
        points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4:
        hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
        hull = list(map(tuple, np.squeeze(hull)))
    else:
        hull = points

    # Number of points in the convex hull
    n = len(hull)

    # Draw the convex hull
    for j in range(0,n):
        cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

    # Display results
    cv2.imshow("Results", im)
    cv2.waitKey(1)


# Main
if __name__ == '__main__':

    cam = cv2.VideoCapture(0)

    while True:
        # Read image
        _, im = cam.read()

        decoded_objects = pyzbar.decode(im)
        display(im, decoded_objects)
