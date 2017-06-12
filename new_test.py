# coding=utf-8
# Está é uma aproximação rápida com melhor chance de sucesso
# para imgens genéricas.
# Precisaria combinar melhor os métodos e processos de forma a ficar robusta

import argparse
import cv
import numpy as np

# carregar imagem
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagem", required = True, help = "path/imagem")
args = vars(ap.parse_args())

# carregar imagem
orig = cv.LoadImage(args["imagem"])

cv.Smooth(orig, orig, cv.CV_GAUSSIAN, 3, 3)

# criar imagens temporarias
grey_scale = cv.CreateImage(cv.GetSize(orig), 8, 1)
processed = cv.CreateImage(cv.GetSize(orig), 8, 1)

# imagem em cinzas
cv.CvtColor(orig, grey_scale, cv.CV_RGB2GRAY)

# Pré-processando imagens cinzas
cv.Erode(grey_scale, processed, None, 10)
#cv.ShowImage("erode", processed)
cv.Dilate(processed, processed, None, 10)
#cv.ShowImage("dilate", processed)
cv.Canny(processed, processed, 5, 70, 3)
#cv.ShowImage("canny", processed)
cv.Smooth(processed, processed, cv.CV_GAUSSIAN, 15, 15)
cv.ShowImage("Imagem pre-procesada", processed)

storage = cv.CreateMemStorage(0)

# 'processed' será modificado!
contours = cv.FindContours(processed, storage, cv.CV_RETR_EXTERNAL)
#cv.ShowImage("depois de FindContours", processed)

cv.DrawContours(orig, contours, cv.RGB(0,255,0), cv.RGB(255,0,0), 2, 3, cv.CV_AA, (0, 0))

def contour_iterator(contour):
  while contour:
    yield contour
    contour = contour.h_next()

for c in contour_iterator(contours):
  # Qde de pontos deve ser ≥ 6 para cv.FitEllipse2
  if len(c) >= 6:
    # Copiar o contorno em um array de (x,y)'s
    PointArray = cv.CreateMat(1, len(c), cv.CV_32FC2)

    for (i, (x, y)) in enumerate(c):
      PointArray[0, i] = (x, y)

    # Encaixar elipse ao contorno
    (center, size, angle) = cv.FitEllipse2(PointArray)

    # Converter dados float da elipse para inteiros
    center = (cv.Round(center[0]), cv.Round(center[1]))
    size = (cv.Round(size[0] * 0.5), cv.Round(size[1] * 0.5))

    # Plot elipse
    cv.Ellipse(orig, center, size, angle, 0, 360, cv.RGB(255,0,0), 2,cv.CV_AA, 0)

cv.ShowImage("imagem original", orig)
#cv.ShowImage("post-process", processed)
cv.WaitKey(0)
