import cv2
import numpy as np
import math


def set_hd(camera):
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


def dist(p1, p2):
    (x1, y1), (x2, y2) = p1, p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def shortest_dist(p1, plist):
    short = dist(p1, plist[0])
    pfin = plist[0]
    for p2 in plist:
        if dist(p1, p2) < short and dist(p1, p2) != 0:
            short = dist(p1, p2)
            pfin = p2
    return pfin


def choose_hsv_range(cam):
    hsv = None
    while True:
        g, img = cam.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        height, width, colors = img.shape
        img = cv2.rectangle(img, (width/2+50, height/2+50), (width/2-50, height/2-50), (255, 0, 0))

        cv2.imshow('img', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    roi = hsv[width/2-50:width/2+50, height/2-50:height/2+50]
    mean = cv2.mean(roi)
    print mean
    uh = int(max_min(mean[0]+10, 2, 178))
    us = int(max_min(mean[1]+100, 2, 253))
    uv = int(max_min(mean[2]+100, 2, 253))
    lh = int(max_min(mean[0]-10, 2, 178))
    ls = int(max_min(mean[1]-100, 2, 253))
    lv = int(max_min(mean[2]-100, 2, 253))

    upper = np.array([uh, us, uv])
    lower = np.array([lh, ls, lv])
    cv2.destroyAllWindows()
    return upper, lower


def max_min(val, min, max):
    if val > max:
        return max
    elif val < min:
        return min
    return val

def hist_curve(im):
    h = np.zeros((300,256,3))
    if len(im.shape) == 2:
        color = [(255,255,255)]
    elif im.shape[2] == 3:
        color = [ (255,0,0),(0,255,0),(0,0,255) ]
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im],[ch],None,[256],[0,256])
        cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.int32(np.column_stack((np.arange(256).reshape(256,1),hist)))
        cv2.polylines(h,[pts],False,col)
    y = np.flipud(h)
    return y
