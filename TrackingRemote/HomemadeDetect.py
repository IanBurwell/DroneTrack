import cv2
import numpy as np
import helpers as h
from itertools import combinations

cam = cv2.VideoCapture(0)
h.set_hd(cam)

upper, lower = h.choose_hsv_range(cam)
print lower, upper

while 1:
    g, img = cam.read()

    #cut out non-orange pixles
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #upper = np.array([20, 252, 250])
    #lower = np.array([0, 86, 20])
    trackhsv = cv2.inRange(hsv, lower, upper)
    track = cv2.bitwise_and(hsv, hsv, mask=trackhsv)

    #Get rid of noise with Morph
    track = cv2.cvtColor(cv2.cvtColor(track, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    track = cv2.morphologyEx(track, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    track = cv2.morphologyEx(track, cv2.MORPH_CLOSE, kernel)

    #find contours
    ret, tthresh = cv2.threshold(track, 0, 255, 0)
    track2, contours, hier = cv2.findContours(tthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #get rid of outliers that are far away
    centLst = []
    avgArea = 0
    for cont in contours:
        M = cv2.moments(cont)
        cX = int(M["m10"] / (M["m00"] + 0.00000001))
        cY = int(M["m01"] / (M["m00"] + 0.00000001))
        avgArea += cv2.contourArea(cont)
        centLst.append((cX, cY))
    combs = combinations(centLst, 2)
    avgDist = 0
    tot = 0
    for combo in combs:
        avgDist += h.dist(combo[0], combo[1])
        tot += 1
    avgDist /= tot+0.00000000000001
    avgArea /= tot+0.00000000000001

    contImg = img.copy()
    for i in range(0, len(contours)-1):
        if avgDist*avgArea > cv2.contourArea(contours[i])*h.dist(centLst[i], h.shortest_dist(centLst[i], centLst)):
            contImg = cv2.drawContours(contImg, contours, i, (0, 0, 255))
        else:
            contImg = cv2.drawContours(contImg, contours, i, (0, 255, 0))

    cv2.imshow('thresh', contImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
cam.release()