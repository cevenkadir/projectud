import cv2, imutils, os
from skimage import measure
import numpy as np
import colorama
import datetime as dt

def are_there_particles(image, which='', add_mask=False):
    if np.shape(image) != ():
        #print('Scanning..', end='\r')
        trigger = False
        #image = image
        #image = cv2.imread('iki.png')
        #image = cv2.imread('test.bmp')
        gray_version = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.GaussianBlur(gray_version, (11, 11), 0)

        # threshold
        thresh = cv2.threshold(gray_version, 20, 255, cv2.THRESH_BINARY)[1]

        muons = measure.label(thresh, neighbors=4, background=0)
        mask = np.zeros(thresh.shape, dtype="uint8")

        for muon_i in np.unique(muons):
            if muon_i == 0:
                #print(colorama.Fore.RED + 'No muon!' + colorama.Style.RESET_ALL)
                continue

            muons_mask = np.zeros(thresh.shape, dtype="uint8")
            muons_mask[muons == muon_i] = 255

            num_pixels = cv2.countNonZero(muons_mask)


            print(colorama.Fore.YELLOW + "{}num of pix: {}".format(which, num_pixels)+ colorama.Style.RESET_ALL)
            if num_pixels > 2:
                currentDT = dt.datetime.now()
                print(colorama.Fore.GREEN + str(currentDT) + colorama.Style.RESET_ALL)
                trigger = True
                mask = cv2.add(mask, muons_mask)

        if add_mask:
            return (trigger, mask)
        else:
            return trigger

        #cv2.imshow('Test image', thresh)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

