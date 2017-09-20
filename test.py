# coding=utf-8
# Notas:
#   Como a transformada Hough é muito específica e não robusta
#   O ajuste dos parâmetros é muito sensível para uso geral
#   Não há resolução suficiente para Hough determinar circulos
#     pequenos com certeza sem afetar grandemente para
#     círculos com diâmetros maiores ou ainda com outras
#     formas silimares (polígonos com muitos lados)

# evironmenta data:       env.txt
# output images:          <imagefilename>-o.png
# result data:            output.txt
# run program for view:   original + outuput (side by side)

# Tested in: osx 10.11.6, python 3.6, opencv 3.3

import argparse, sys, os.path
import numpy as np
import cv2

def HoughLines(_image):
    lines = cv2.HoughLinesP(image=_image,
                            rho=1,
                            theta=np.pi/180,
                            threshold=15,
                            minLineLength=30,
                            maxLineGap=1)
    return lines

def HoughCircles(image,
                 _dp,        # delta center             # 1-10
                 _minDist,   # minimun center distance  #
                 _param1,    # gradient                 # 30-150
                 _param2,    # accumulator              # 10-180
                 _minRadius,                            # 3
                 _maxRadius):                           # 115
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT,
                               dp=_dp,
                               minDist=_minDist,
                               param1=_param1,
                               param2=_param2,
                               minRadius=_minRadius,
                               maxRadius=_maxRadius)
    return circles

def find_circles(circles, edges, output):
    if circles is None:
        None
        # print u"Círculos não encontrados"
        # sys.exit()
        return None

    circles = np.uint16(np.around(circles))
    #print circles

    for i in circles[0,:]:
        x = i[0]
        y = i[1]
        r = i[2]
        crop = edges[y-r:y+r,x-r:x+r] # Not exactly but doesn't matter
        lines = HoughLines(crop)
        if lines is None:
            cv2.circle(output,(x,y),r,(255,0,255),2)
            maior_que_10 = u"≥" if 2*i[2] >= 10 else "<"
            print(u"Círculo em (%d,%d) com diâmetro %d %s 10" % (i[0],i[1],2*i[2],maior_que_10))

####################
#   program main   #
####################

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagem", required = True, help = "path/image_name")
args = vars(ap.parse_args())

filename = args["imagem"]
if not os.path.isfile(filename):
    print("[" + filename + "] não é erquivo!")
    sys.exit()

image = cv2.imread(filename)
#cv2.imshow("image", image)

output = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray", gray)

# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# cv2.imshow("blurred", blurred)

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

cv2.imshow('lines', output)
#cv2.waitKey(0)

# circles with diameter up to 12
circles = HoughCircles(opening,
                       1.2,     # delta center
                       40,      # min distance
                       30,      # gradient
                       12,      # accumulator
                       2,       # min radio
                       6)       # max radio
find_circles(circles, edges, output)

# circles with diameter 12 or more
circles = HoughCircles(opening,
                       10,      # delta center
                       120,     # min distance
                       100,     # gradient
                       180,     # accumulator
                       6,       # min radio
                       115)     # max radio
find_circles(circles, edges, output)

ofilename = filename
ofilename = os.path.splitext(filename)[0]+'-o.png'
#cv2.imwrite(ofilename, output)

cv2.imshow('circles (purple)', output)
#cv2.imshow('input - output', np.hstack([image, output]))

cv2.waitKey(0)
cv2.destroyAllWindows()

