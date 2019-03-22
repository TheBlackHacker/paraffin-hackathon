from __future__ import print_function
import sys
import cv2
import mss
import numpy
import time
from random import randint

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

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": 500, "height": 500}
    # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
    # So we will call this function in a loop till we are done selecting all objects
    while "Screen capturing":
        img = numpy.array(sct.grab(monitor))
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

# Initialize MultiTracker
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)

old_p1 = (0,0)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 500, "height": 500}

    while "Screen capturing":
        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Process video and track objects
        frame = img[:, :, :-1]

        # get updated location of objects in subsequent frames
        success, boxes = multiTracker.update(frame)

        # draw tracked objects
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            # Neu p1 giam thi sang trai, p1 tang thi sang phai
            if p1[0] > old_p1[0]+10 or p1[0] < old_p1[0]-10:
                if old_p1[0] < p1[0]:
                    print("right")
                if old_p1[0] > p1[0]:
                    print("left")
            # Neu p2 giam thi cui xuong, p2 tang thi len
            if p1[1] > old_p1[1]+10 or p1[1] < old_p1[1]-10:
                if old_p1[1] < p1[1]:
                    print("down")
                if old_p1[1] > p1[1]:
                    print("up")
            old_p1 = p1

        # show frame
        cv2.imshow('MultiTracker', frame)

        # time.sleep(2)

        # quit on ESC button
        if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
            break