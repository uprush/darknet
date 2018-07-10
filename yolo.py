#!/usr/env python2
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import argparse
import sys
import os

import cv2

sys.path.append(os.path.join(os.getcwd(),'python/'))
import darknet as dn

class YoloResult(object):
    def __init__(self, obj_name, score, boundingbox):
        self.obj_name = obj_name
        self.score = score
        self.x_min = boundingbox[0] - boundingbox[2]/2 -1
        self.y_min = boundingbox[1] - boundingbox[3]/2 -1
        self.width = boundingbox[2]
        self.height = boundingbox[3]

    def get_detect_result(self):
        resultdict = { 'obj_name' : self.obj_name,
                       'score' : self.score,
                       'bounding_box' : {
                           'x_min' : self.x_min,
                           'y_min' : self.y_min,
                           'width' : self.width,
                           'height' : self.height }
                       }
        return resultdict

    def show(self):
        print("obj_name: %s" % self.obj_name)
        print("score   : %.3f" % self.score)
        print("x_min   : %.2f" % self.x_min)
        print("y_min   : %.3f" % self.y_min)
        print("width   : %.3f" % self.width)
        print("height  : %.3f" % self.height)


class Yolo(object):
    def __init__(self, cfgfilepath, weightfilepath, datafilepath):
        print(cfgfilepath)
        print(weightfilepath)
        self.net = dn.load_net(cfgfilepath, weightfilepath, 0)
        self.meta = dn.load_meta(datafilepath)

    def detect(self, filepath, thresh=0.25):
        raw_results = dn.detect(self.net, self.meta, filepath, thresh)

        return [ YoloResult(raw_result[0], raw_result[1], raw_result[2]) for raw_result in raw_results ]

    def insert_rectangle(self, filepath, yolo_results, outputdir='outputdir'):
        img = cv2.imread(filepath, 1)
        for yolo_result in yolo_results:
            obj_name = yolo_result.obj_name
            x = yolo_result.x_min
            y = yolo_result.y_min
            w = yolo_result.width
            h = yolo_result.height

            cv2.rectangle(img, (int(x), int(y)), (int(x+w)+1, int(y+h)+1), (0,255,0), 1)
            cv2.putText(img, obj_name, (int(x) -1, int(y) -1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

        inputfilename = filepath.split(os.path.sep)[-1]

        outputfilename = '%s_pred.%s' % (inputfilename.split('.')[0], inputfilename.split('.')[-1])
        outputfilepath = os.path.join(outputdir, outputfilename)
        cv2.imwrite(outputfilepath, img)

        return outputfilepath

def importargs():
    parser = argparse.ArgumentParser('This is the python script of yolo.This is only detect the objects')

    parser.add_argument("--cfgfilepath", "-cf", help = "config filepath  of darknet", type=str)
    parser.add_argument("--datafilepath", "-df", help = "datafilepath of darknet", type=str)
    parser.add_argument("--weightfilepath", "-wf", help = "weight filepath of darknet")
    parser.add_argument("--imagefilepath", "-if", help = "image filepath you want to detect")
    parser.add_argument("--thresh", "-th", help = "thresh hold of yolo detection", type=float, required=False, default=0.25)

    args = parser.parse_args()

    file_exist_flag = True

    if args.cfgfilepath:
        assert os.path.exists(args.cfgfilepath), "cfgfilepath of %s does not exist" % args.cfgfilepath
    else:
        file_exist_flag = False
        print("cfgfilepath is needed")

    if args.datafilepath:
        assert os.path.exists(args.datafilepath), "datafilepath of %s does not exist" % args.datafilepath
    else:
        file_exist_flag = False
        print("datafilepath is needed")

    if args.weightfilepath:
        assert os.path.exists(args.weightfilepath), "weightfilepath of %s does not exist" % args.weightfilepath
    else:
        file_exist_flag = False
        print("weightfilepath is needed")

    if args.imagefilepath:
        assert os.path.exists(args.weightfilepath), "imagefilepath of %s does not exist" % args.imagefilepath
    else:
        file_exist_flag = False
        print("imagefilepath is needed")

    if file_exist_flag is False:
        parser.print_usage()
        sys.exit(1)

    return args.cfgfilepath, args.datafilepath, args.weightfilepath, args.imagefilepath, args.thresh

def main():
    cfgfilepath, datafilepath, weightfilepath, imagefilepath, thresh = importargs()

    yolo = Yolo(cfgfilepath, weightfilepath, datafilepath)
    yolo_results = yolo.detect(imagefilepath, thresh)

    for yolo_result in yolo_results:
        yolo_result.show()

    yolo.insert_rectangle(imagefilepath, yolo_results)

if __name__ == "__main__":
    main()
