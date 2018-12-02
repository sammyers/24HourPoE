import sys
sys.path = [p for p in sys.path if 'ros' not in p]
import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier("BuffaloHat/cascade.xml")
eyeCascade = cv2.CascadeClassifier("BuffaloHat/haarcascade_eye.xml")

def confirmHat(image):
    b,g,r = cv2.split(image/255.0)
    avg = np.mean(image, axis=(0,1))
#    print(avg)
    return avg[0] > avg[1]+10 and avg[0] > avg[2]
    '''y = 16+0.299*r+0.578*g+0.114*b
    cb = 128+(-37.797*r-74.203*g+112*b)
    cr = 128+(112*r-93.786*g-18.214*b)
    ycbcr = cv2.merge((y,cb,cr))
    color = np.zeros((256,256,3), np.uint8)
    height, width, channels = ycbcr.shape
    colors = []
    for x in range(width):
        for y in range(height):
            point = ycbcr[y,x]
            if np.sqrt((point[1]-128)**2 + (point[2]-128)**2) >  16:
                color[int(point[1]),int(point[2])] = image[y,x]
                colors.append(point - 128)
    if len(colors) == 0:
        return False
    avg_color = np.mean(colors, axis=0)
    angle = np.arctan(avg_color[1]/avg_color[2])
    print(angle)
    if angle > -1.05 and angle < -.9:
        return True
    return False'''
    #cv2.imshow("color", color)

def detectHat(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(grey,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30),
                                         flags = cv2.CASCADE_SCALE_IMAGE)
    confirmed_faces = []
    for (x, y, w, h) in faces:
        
        #cv2.imshow("face",frame[y:y+h,x:x+w])
        eyes = eyeCascade.detectMultiScale(grey[y:y+h,x:x+w],
                                       scaleFactor=1.1,
                                       minNeighbors=5,
                                       minSize=(30, 30),
                                       flags = cv2.CASCADE_SCALE_IMAGE)
        if len(eyes) > 1:
            confirmed_faces.append((x,y,w,h))
    for (x, y, w, h) in confirmed_faces:
                hat = frame[max(y-h/2,0):y,x:x+w]
                #cv2.imshow("hat",hat)
                detected_hat = confirmHat(hat)
                #cv2.rectangle(frame, (x,y), (x+w, y-h/2), (255,0,0), 2)
                if detected_hat:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    return True
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return False

# Main
if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    while True:
        _, frame = cam.read()
        detectHat(frame)
        cv2.imshow("faces", frame)
        cv2.waitKey(1)


