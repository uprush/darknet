#!/bin/bash

IMG_NAME=$1

curl -XPOST -F file=@/var/www/html/images/$IMG_NAME http://localhost:8080/detect
