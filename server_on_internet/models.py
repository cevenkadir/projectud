from django.db import models

from recording_muons_on_pc.detecting_spar import are_there_particles

import os, cv2, imutils
from skimage import measure
import numpy as np

from django.utils import timezone

import datetime as dt


class Muon(models.Model):
    angle = models.FloatField('Calculated angle',default=0)
    detection_time = models.DateTimeField('Detection date', default=timezone.now())
    image = models.ImageField('Muon image', upload_to='muons/', default='muons/muon_2019_4_18_14_17_12_650984.webp')
    cropped_image = models.ImageField('Cropped muon image', upload_to='muons/cropped/', default='')

    def process_muon(self):
        img = cv2.imread(self.image.path)
        height, width = img.shape[:2]

        mask = are_there_particles(img, add_mask=True)[1]

        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

        #exclude the particles if there are more than one at the same time
        if len(cnts) == 1:
            c = cnts[0]
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)

            cX = int(np.ceil(cX))
            cY = int(np.ceil(cY))
            radius = int(np.ceil(radius)) * 2 + 5


            box = cv2.minAreaRect(c)

            #lengths of the muon
            lengths = [int(np.round(l_i + 1)) for l_i in box[1]]

            #thickness of sensor (micrometer)
            d = 10

            #size of a pixel (micrometer)
            a = 6

            delta_ls = np.abs(lengths[0] - lengths[1])

            calculated_angle = np.rad2deg(np.arctan((a * delta_ls)/d))
            print(calculated_angle)

            self.angle = calculated_angle

            #setting the creation
            creation_time = dt.datetime.strptime(os.path.basename(self.image.name), 'muon_%Y-%m-%d_%H%M%S.%f.jpg')
            self.detection_time = creation_time

            coordinates_ys = [(cY - radius), (cY + radius)]
            coordinates_xs = [(cX - radius), (cX + radius)]

            if coordinates_ys[0] < 0:
                coordinates_ys[0] = 0
            if coordinates_ys[1] > (height-1):
                coordinates_ys[1] = height-1
            if coordinates_xs[0] < 0:
                coordinates_xs[0] = 0
            if coordinates_xs[1] > (width-1):
                coordinates_xs[1] = width-1

            cropped_img = img[coordinates_ys[0]:coordinates_ys[1], coordinates_xs[0]:coordinates_xs[1]]
            cv2.imwrite(self.image.path, cropped_img, [cv2.IMWRITE_JPEG_QUALITY])

            self.save()
        else:
            self.image.delete(save=True)
            self.delete()

def context_numbers_of_muons(request):
    try:
        return {'number_of_muons': Muon.objects.count()}
    except:
        return {'number_of_muons': 0}

