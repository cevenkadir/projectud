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

    def process_muon(self):
        img = cv2.imread(self.image.path)
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
            radius = int(np.ceil(radius)) * 2

            cropped_img = img[(cY - radius):(cY + radius), (cX - radius):(cX + radius)]
            #cropped_img_file_name = f'muon_{creation_time_obj.year}_{creation_time_obj.month}_{creation_time_obj.day}_{creation_time_obj.hour}_{creation_time_obj.minute}_{creation_time_obj.second}_{creation_time_obj.microsecond}.webp'
            #cv2.imwrite(cropped_img_file_name, cropped_img, [cv2.IMWRITE_WEBP_QUALITY])

            box = cv2.minAreaRect(c)

            #lengths of the muon
            lengths = [int(np.round(l_i + 1)) for l_i in box[1]]

            #thickness of sensor (micrometer)
            d = 140

            #size of a pixel (micrometer)
            a = 6

            delta_ls = np.abs(lengths[0] - lengths[1])

            calculated_angle = np.rad2deg(np.arctan((a * delta_ls)/d))
            print(calculated_angle)

            self.angle = calculated_angle

            #setting the creation
            creation_time = dt.datetime.strptime(os.path.basename(self.image.name), 'muon_%Y-%m-%d_%H%M%S.%f.jpg')
            self.detection_time = creation_time

            self.save()
        else:
            self.image.delete(save=True)
            self.delete()

def context_numbers_of_muons(request):
    return {'number_of_muons': Muon.objects.count()}
