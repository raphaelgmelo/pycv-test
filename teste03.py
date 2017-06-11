# coding=utf-8
# Notas:
#   Como a transformada Hough é muito espeífica e não robusta
#   O ajuste dospaâmetros é muito sensível para uso geral
#   Não há resolução suficiente para Hough determinar circulos
#     pequenos com certezasm afetar grandemente para
#     círculos com diâmetros maiores ou ainda com outras
#     formas silimares (polígonos com muitos lados)

import argparse, sys, os.path
import numpy as np
import cv2

def HoughLines(_image):
    lines = cv2.HoughLinesP(image=_image,
                            # rho=1,
                            # theta=np.pi/180,
                            # threshold=15,
                            # #lines=np.array([]),
                            # minLineLength=30,
                            # maxLineGap=1)
                            rho=1,
                            theta=np.pi/180,
                            threshold=15,
                            #lines=np.array([]),
                            minLineLength=30,
                            maxLineGap=1)
    return lines

def HoughCircles(image,
                 _dp,        # accum_res / img_res
                 _minDist,   # minimun center distance
                 _param1,    # gradient
                 _param2,    # accumulator
                 _minRadius,
                 _maxRadius):
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT,
                               dp=_dp,
                               minDist=_minDist,
                               param1=_param1,
                               param2=_param2,
                               minRadius=_minRadius,
                               maxRadius=_maxRadius)

    # circles more than 20
    # dp=10,            # accum_res / img_res
    # minDist=120,      #
    # param1=100,       # gradient
    # param2=180,       # accumulator
    # minRadius=5,
    # maxRadius=115)

        # # circles until diameter
        # dp=1.2,           # accum_res / img_res / centro
        # minDist=40,       #
        # param1=30,        # gradient
        # param2=10,        # accumulator
        # minRadius=3,
        # maxRadius=6)

              # dp=2,            # accum_res / img_res
              # minDist=150,     #
              # param1=30,       # gradient
              # param2=15,       # accumulator
              # minRadius=0,
              # maxRadius=0)
    return circles

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagem", required = True, help = "path/image_name")
args = vars(ap.parse_args())

img_file = args["imagem"]
if not os.path.isfile(img_file):
    print "[" + img_file + "] não é erquivo!"
    sys.exit()

image = cv2.imread(img_file)
cv2.imshow("image", image)

output = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)

(thresh, im_bw) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow('bw', im_bw)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))

# erosion = cv2.erode(im_bw, kernel, iterations = 1)
# cv2.imshow('esorion', erosion)

# dilation = cv2.dilate(im_bw,kernel,iterations = 1)
# cv2.imshow('dilation', dilation)

opening = cv2.morphologyEx(im_bw, cv2.MORPH_OPEN, kernel)
cv2.imshow('open', opening)

# closing = cv2.morphologyEx(im_bw, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('close', closing)


edges = cv2.Canny(opening, 100, 200, apertureSize = 3)
cv2.imshow('edges', edges)

lines = HoughLines(edges)

if lines is None:
    None
    # print "Retas não encontradas"
    # sys.exit()
else:
#    print lines
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            cv2.line(output, (x1,y1), (x2,y2), (255,0,0), 2)

#cv2.imshow('hough', output)
#cv2.waitKey(0)

# circles = cv2.HoughCircles(opening, cv2.cv.CV_HOUGH_GRADIENT,
#                         # dp=10,            # accum_res / img_res
#                         # minDist=120,      #
#                         # param1=100-400,   # gradient
#                         # param2=180-220,   # accumulator
#                         # minRadius=5,
#                         # maxRadius=115)

    # circles more than 20
    # dp=10,            # accum_res / img_res
    # minDist=120,      #
    # param1=100,       # gradient
    # param2=180,       # accumulator
    # minRadius=5,
    # maxRadius=115)

        # # circles until diameter
        # dp=1.2,           # accum_res / img_res / centro
        # minDist=40,       #
        # param1=30,        # gradient
        # param2=10,        # accumulator
        # minRadius=3,
        # maxRadius=6)

              # dp=2,            # accum_res / img_res
              # minDist=150,     #
              # param1=30,       # gradient
              # param2=15,       # accumulator
              # minRadius=0,
              # maxRadius=0)

circles = HoughCircles(opening,
#                         # dp=10,            # accum_res / img_res
#                         # minDist=120,      #
#                         # param1=100-400,   # gradient
#                         # param2=180-220,   # accumulator
#                         # minRadius=5,
#                         # maxRadius=115)

    # circles more than 20
    # dp=10,            # accum_res / img_res
    # minDist=120,      #
    # param1=100,       # gradient
    # param2=180,       # accumulator
    # minRadius=5,
    # maxRadius=115)

        # # circles until diameter 20
        1.2,           # accum_res / img_res / centro
        40,       #
        30,        # gradient
        10,        # accumulator
        3,
        6)

              # dp=2,            # accum_res / img_res
              # minDist=150,     #
              # param1=30,       # gradient
              # param2=15,       # accumulator
              # minRadius=0,
              # maxRadius=0)


if circles is None:
    print "Circulos não encontrados"
    sys.exit()

circles = np.uint16(np.around(circles))
#print circles

for i in circles[0,:]:
    x = i[0]
    y = i[1]
    r = i[2]
#    crop = edges[y-r-2:y+r+2,x-r-2:x+r+2] # Not exactly but doesn't matter
    crop = edges[y-r:y+r,x-r:x+r] # Not exactly but doesn't matter    lines = HoughLines(crop)
    if lines is None:
        cv2.circle(output,(x,y),r,(255,0,255),2)
        #cv2.circle(output,(x,y),2,(0,0,255),3)
        if 2*i[2] > 10: maior_que_10 = u">"
        else: maior_que_10 = u"≤"
        print(u"Círculo em (%d,%d) com diâmetro %d %s 10" % (i[0],i[1],2*i[2],maior_que_10))

cv2.imshow('circles (green)', output)
#cv2.imshow('input - output', np.hstack([image, output]))

cv2.waitKey(0)
cv2.destroyAllWindows()

