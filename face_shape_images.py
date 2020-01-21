import numpy as np
import cv2
import dlib
import math
from math import degrees
from imutils import face_utils
from glob import glob
import csv
from utilities import *
p = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)
import argparse
all_dist=[]
all_diff=[]
text = """
        -d --> Path to dataset
        """

parser = argparse.ArgumentParser(description = text)
parser.add_argument("--dataset", "-d", help="Path to your dataset", type=str ,required=True)
args = parser.parse_args()
dataset = args.dataset

for img in glob(dataset+"/*"):
    try:
        print(img.split('/')[-1])
        image_name=img.split('/')[-1]
        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)


        for (i, rect) in enumerate(rects):
            (x, y, w, h) = rect_to_bb(rect)
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            face_ratio = ratio((image.shape[1]*image.shape[0]), (w*h))
            bottom_of_fore_head = int((shape[21][0] + shape[22][0]) / 2), int((shape[21][1] + shape[22][1]) / 2)

            nose_point=shape[29]
            nose_distance=distance(shape[30], bottom_of_fore_head, 2)
            top_of_forehead = (bottom_of_fore_head[0], bottom_of_fore_head[1] - int(nose_distance))

            #classifier 1
            hoizontal_distance = distance(shape[14], shape[2], 2)
            virtical_distance = distance(shape[8], top_of_forehead, 2)
            x_center = shape[2][0] + int(hoizontal_distance / 2)
            y_center = shape[8][1] - int(virtical_distance / 2)

            face_length = distance(top_of_forehead, shape[8], 2)
            vertical_check_point = (face_length*100)/image.shape[0]
            cheek_length = distance(shape[2], shape[14], 2)
            horizontal_check_point = (cheek_length*100)/image.shape[0]
            check_point_1 = subtract(face_length, cheek_length)

            hoizontal_distance = distance(shape[14], shape[2], 2)
            virtical_distance = distance(shape[8], top_of_forehead, 2)
            x_center = shape[2][0] + int(hoizontal_distance / 2)
            y_center = shape[8][1] - int(virtical_distance / 2)
            face_center = x_center, y_center
            check_point = distance(face_center, shape[8], 2)
            check_point_percent = (check_point * 100) / image.shape[0]
            distance_list = []
            for n in range(0, 17):
                distance_list.append(distance(face_center, shape[n], 2))
            # print(image.shape)
            length_comp_2_image_height = [value * 100 / image.shape[0] for value in distance_list]
            # print('length_comp_2_image_height', length_comp_2_image_height)
            # print('#' * 30)
            # print('standard deviation of comp to image length', standard_dev(length_comp_2_image_height))
            # print('#' * 30)
            deviation = standard_dev(length_comp_2_image_height)
            # print('check point', check_point_1)

            #classifier 2
            eye_mid_l = int((shape[36][0] + shape[39][0]) / 2), int((
                        shape[36][1] + shape[39][1]) / 2)
            eye_mid_r = int((shape[42][0] + shape[45][0]) / 2), int((
                        shape[42][1] + shape[45][1]) / 2)

            mid_chik = int((shape[5][0]+shape[6][0])/2), int((shape[5][1]+shape[6][1])/2)
            mid_chik_1 = int((shape[10][0]+shape[11][0])/2), int((shape[10][1]+shape[11][1])/2)
            dist_v0 = distance(eye_mid_l, shape[6], 2)
            dist_v1 = distance(eye_mid_r, shape[10], 2)
            dist_v2 = distance(shape[27], shape[8], 2)

            change_v0_2_v1 = subtract(dist_v0, dist_v1)
            change_v1_2_v2 = subtract(dist_v1, dist_v2)

            # print('vertical changes*************', change_v0_2_v1, change_v1_2_v2)

            dist_v = [dist_v0, dist_v1, dist_v2]
            mean_v = sum(dist_v)/3
            v_check_point = h
            deviation_v = standard_dev([dist_v0, dist_v1, dist_v2])


            dist_h0 = distance(shape[0], shape[16], 2)
            dist_h1 = distance(shape[1], shape[15], 2)
            dist_h2 = distance(shape[2], shape[14], 2)
            dist_h3 = distance(shape[3], shape[13], 2)
            dist_h4 = distance(shape[4], shape[12], 2)
            dist_h5 = distance(shape[5], shape[11], 2)
            dist_h6 = distance(shape[6], shape[10], 2)
            dist_h7 = distance(shape[7], shape[9], 2)
            dist_h = [dist_h0, dist_h1, dist_h2, dist_h3, dist_h4, dist_h5, dist_h6, dist_h7]
            mean_h = sum(dist_h)/len(dist_h)

            deviation_h = standard_dev(dist_h)

            #angles
            list_of_slopes = []
            list_of_angles = []
            for n in range(0, 8):
                list_of_slopes.append(slope(nose_point, shape[n]))

            for n in range(0, 8):
                list_of_angles.append(angle(list_of_slopes[n]))
            # print(list_of_angles)
            # print('@'*35)
            # print('deviation',deviation)
            # print('check point',check_point_1,.18*face_length,.24*face_length)
            # print('mean and dev h and dev v',deviation_h,.36*mean_h,deviation_v,.08*mean_v)
            # print(list_of_angles[4])
            # print('@'*35)


            face_shape = 'none'
            if deviation > 1.9:
                print('rectangular/oval')
                if list_of_angles[4] > 42 and list_of_angles[4] < 51:
                    face_shape = 'Rectangle'
                else:
                    face_shape = 'Oval'
            elif deviation < 1.2:
                print('round/square')
                if list_of_angles[4] > 42 and list_of_angles[4] < 51:
                    face_shape = 'Square'
                else:
                    face_shape = 'Round'

            elif check_point_1 < .18*face_length:
                print('round/square')
                if list_of_angles[4] > 42 and list_of_angles[4] < 51:
                    face_shape = 'Square'
                else:
                    face_shape = 'Round'
            elif check_point_1 > 0.24*face_length:
                print('rectangle/oval')
                if list_of_angles[4]>42 and list_of_angles[4]<51:
                    face_shape = 'Rectangle'
                else:
                    face_shape = 'Oval'
            elif deviation_h < .36*mean_h and deviation_v < .085*mean_v:
                print('round/square from case 2')
                if list_of_angles[4] > 42 and list_of_angles[4] < 51:
                    face_shape = 'Square'
                else:
                    face_shape = 'Round'
            else:
                print('oval/rectangle')
                if list_of_angles[4] > 42 and list_of_angles[4] < 51:
                    face_shape = 'Rectangle 101'
                else:
                    face_shape = 'Oval 101'

            print(face_shape)
            cv2.putText(image, face_shape, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (220, 200, 255))
            cv2.imshow('image', image)
            cv2.waitKey(0)


    except Exception as e:
        print(e)
        pass
