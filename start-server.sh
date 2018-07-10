#!/bin/bash

python darknet-server.py -cf ./cfg/yolov3.cfg -df ./cfg/coco.data -wf ./yolov3.weights -ud ./upload -pf true -H localhost

