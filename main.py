import cv2
import time
import os
import platform

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect(frame, last_intruder):
    coordinates, _weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    is_intruder = False
    person = 1
    for x, y, w, h in coordinates:
        person += 1
        if x + w > 520 and y < 125:
            if time.time() - last_intruder > 3:
                if platform.system() == 'Linux':
                    os.system('spd-say "Alert, an intruder is coming"')
                elif platform.system() == 'Darwin':
                    os.system('say "Alert, an intruder is coming"')
                else:
                    print('Alert, an intruder is coming')
                    print('Sorry but there is no built in text to speech in windows')

                is_intruder = True

    return is_intruder


def intruder_detector():
    video = cv2.VideoCapture(0)
    print('Detecting people...')

    frame_rate = 3
    prev = 0
    last_intruder = 0

    while True:

        time_elapsed = time.time() - prev
        check, frame = video.read()

        if time_elapsed > 1. / frame_rate:
            prev = time.time()
            is_intruder = detect(frame, last_intruder)
            if is_intruder:
                last_intruder = time.time()


if __name__ == '__main__':
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    intruder_detector()
