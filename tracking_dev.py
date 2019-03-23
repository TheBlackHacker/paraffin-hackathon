from __future__ import print_function
import sys
import cv2
import mss
import numpy
import time
from pykeyboard import PyKeyboard
from random import randint
from PIL import Image

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD',
                'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']


def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[7]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)

    return tracker

bboxes = []
colors = []
first_image = 0

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 500, "height": 500}
    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while "Screen capturing":
        img = numpy.array(sct.grab(monitor))
        first_image = sct.grab(monitor)
        frame = img[:, :, :-1]
        # draw bounding boxes over objects
        # selectROI's default behaviour is to draw box starting from the center
        # when fromCenter is set to false, you can draw box starting from top left corner
        bbox = cv2.selectROI('MultiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        if (k == 113):  # q is pressed
            break

    print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

roi = 0
global_bbox = 0
# Initialize MultiTracker
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)
    current_img = numpy.array(first_image)
    global_bbox = bbox
    roi = current_img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]

hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

old_p1 = (0,0)
keyboard = PyKeyboard()

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 500, "height": 500}

    while "Screen capturing":
        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Process video and track objects
        frame = img[:, :, :-1]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        ret, track_window = cv2.CamShift(mask, global_bbox, term_criteria)

        pts = cv2.boxPoints(ret)
        pts = numpy.int0(pts)

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)

        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            # Neu p1 giam thi sang trai, p1 tang thi sang phai
            if p1[0] > old_p1[0]+10 or p1[0] < old_p1[0]-10:
                if old_p1[0] < p1[0]:
                    keyboard.press_key('d')
                    print("right")
                    time.sleep(0.2)
                    keyboard.release_key('d')
                if old_p1[0] > p1[0]:
                    keyboard.press_key('a')
                    print("left")
                    time.sleep(0.2)
                    keyboard.release_key('a')
            # Neu p2 giam thi cui xuong, p2 tang thi len
            if p1[1] > old_p1[1]+10 or p1[1] < old_p1[1]-10:
                if old_p1[1] < p1[1]:
                    keyboard.press_key('f')
                    print("down")
                    time.sleep(0.2)
                    keyboard.release_key('f')
                if old_p1[1] > p1[1]:
                    keyboard.press_key('r')
                    print("up")
                    time.sleep(0.2)
                    keyboard.release_key('r')
            old_p1 = p1

        # show frame
        cv2.imshow('MultiTracker', frame)

        # time.sleep(2)

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break