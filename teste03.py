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

#lines = cv2.HoughLinesP(edges, 1, np.pi/180, 15, 100, 2)

lines = cv2.HoughLinesP(image=edges,
                        rho=1,
                        theta=np.pi/180,
                        threshold=15,
                        #lines=np.array([]),
                        minLineLength=30,
                        maxLineGap=1)
if lines is not None:
#     print "Não existem retas"
#     sys.exit()
# else:
    print lines
    for x in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[x]:
            cv2.line(output, (x1,y1), (x2,y2), (255,0,0), 2)

#cv2.imshow('hough', output)
#cv2.waitKey(0)

circles = cv2.HoughCircles(opening, cv2.cv.CV_HOUGH_GRADIENT,
#               dp=10,            # accum_res / img_res
#               minDist=120,      #
#               param1=100-400,   # gradient
#               param2=180-220,   # accumulator
#               minRadius=5,
#               maxRadius=115)

              dp=10,            # accum_res / img_res
              minDist=120,      #
              param1=100,       # gradient
              param2=180,       # accumulator
              minRadius=5,
              maxRadius=115)

              # dp=1.5,           # accum_res / img_res / centro
              # minDist=80,       #
              # param1=30,        # gradient
              # param2=15,        # accumulator
              # minRadius=4,
              # maxRadius=115)

              # dp=2,            # accum_res / img_res
              # minDist=150,     #
              # param1=30,       # gradient
              # param2=15,       # accumulator
              # minRadius=0,
              # maxRadius=0)

for i in circles[0,:]:
    if 2*i[2] > 10: maior_que_10 = u">"
    else: maior_que_10 = u"≤"
    print(u"Círculo em (%d,%d) com diâmetro %d %s 10" % (i[0],i[1],2*i[2],maior_que_10))


circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    cv2.circle(output,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(output,(i[0],i[1]),2,(0,0,255),3)

#cv2.imshow('circles', output)
cv2.imshow('input - output', np.hstack([image, output]))

cv2.waitKey(0)
cv2.destroyAllWindows()
