import re
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime


# Gauge settings
radius = 80
axes = (radius, radius)


# Colors
white = (255, 255, 255)
gray = (150, 150, 150)
red = (0, 30,255)
orange = (0, 165,255)
green = (0, 255,30)
blue =  (255, 180,180)
yellow =  (30, 255,255)
black = (0,0,0)

# Font settings
font = cv2.FONT_HERSHEY_DUPLEX
thickness = 2
bigscale = 1
baseline = 1
scale = 0.5

# For speed
def pprint(x):
  if x>=10:
    return str(x)
  elif x>0:
    return " "+str(x)
  else:
    return str(x)

# Size of letters
def l(s):
  return(cv2.getTextSize(s, font, scale, baseline)[0])
def L(s):
  return(cv2.getTextSize(s, font, bigscale, baseline)[0])


# Draw gauge
def gauge_heart_rate(image, hr, center, min_hr, max_hr):
    assert isinstance(hr, float)

    image = cv2.ellipse(image, center, axes, 0, 285, 350, white, thickness)
    image = cv2.ellipse(image, center, axes, 0, 190, 255, white, thickness)

    convert = hr - min_hr
    convert /= (max_hr - min_hr)
    convert *= np.pi
    convert += np.pi
    c = -np.cos(convert)
    s = -np.sin(convert)

    image = cv2.line(image,  (center[0] , center[1] ), (center[0] -int(9*radius//10*c), center[1] - int(9*radius//10*s)), white, 3)

    for j in range(1,9):
      if j%4!=0:
        c = -np.cos(j*np.pi/8)
        s = np.sin(j*np.pi/8)
        image = cv2.line(image,  (center[0] -int((7+(j%2)/2)*radius//8*c), center[1] - int((7+(j%2)/2)*radius//8*s)), (center[0] -int(radius*c), center[1] - int(radius*s)), (235,231,231), 1)
    
    hand_size_x = 3*L("99")[0]//4
    hand_size_y = 3*L("99")[1]//4
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] + hand_size_x, center[1] + hand_size_y), black, -1)
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] + hand_size_x, center[1] + hand_size_y), white, 1)

    hr = int(hr)

    if 60<=hr and hr<155:
      color_text=green
    elif 155<=hr and hr<170:
      color_text=yellow
    else:
      color_text = red

    image = cv2.putText(image, str(hr), (center[0]-L(str(hr))[0]//2,center[1]+L(str(hr))[1]//2) , cv2.FONT_HERSHEY_DUPLEX, bigscale, color_text, thickness, cv2.LINE_AA)
    
    
    half_hr = str(int((min_hr + max_hr)/2))
    min_hr = str(int(min_hr))
    max_hr = str(int(max_hr))


    image = cv2.putText(image, min_hr, (center[0]-radius-l(min_hr)[0]//2,center[1]+l(min_hr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, max_hr, (center[0]+radius-l(max_hr)[0]//2,center[1]+l(max_hr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, half_hr, (center[0]-l(half_hr)[0]//2,center[1]-radius+l(half_hr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)

    image = cv2.putText(image, "bpm", (center[0]-19,center[1]+30) , cv2.FONT_HERSHEY_DUPLEX, 0.6, white, 1, cv2.LINE_AA)
    return (image)

def gauge_speed(image, speed, center, min_speed, max_speed):

    # min_speed = 0
    # max_speed = 100

    # print(speed)

    # assert isinstance(speed, float)

    assert (min_speed<max_speed)

    # image = cv2.ellipse(image, center, axes, angle, startAngle, endAngle, white, thickness)
    image = cv2.ellipse(image, center, axes, 0, 285, 350, white, thickness)
    image = cv2.ellipse(image, center, axes, 0, 190, 255, white, thickness)
  
    convert = speed - min_speed
    convert /= (max_speed - min_speed)
    convert *= np.pi
    convert += np.pi
    c = -np.cos(convert)
    s = -np.sin(convert)
    image = cv2.line(image,  (center[0], center[1]), (center[0] -int(9*radius//10*c), center[1] - int(9*radius//10*s)), white, 3)
    
    for j in range(1,13):
      if j%6!=0:
        c = -np.cos(j*np.pi/12)
        s = np.sin(j*np.pi/12)
        image = cv2.line(image,  (center[0] -int((7+(j%2)/2)*radius//8*c), center[1] - int((7+(j%2)/2)*radius//8*s)), (center[0] -int(radius*c), center[1] - int(radius*s)), (235,231,231), 1)
    
    hand_size_x = 3*L("9999")[0]//4
    hand_size_y = 3*L("9999")[1]//4
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] +hand_size_x, center[1] +hand_size_y), black, -1)
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] +hand_size_x, center[1] +hand_size_y), white, 1)

    image = cv2.putText(image, pprint(speed), (center[0]-L(pprint(speed))[0]//2,center[1]+L(pprint(speed))[1]//2) , font, bigscale, white, thickness, cv2.LINE_AA)
    
    half_speed = str(int((min_speed + max_speed)/2))
    min_speed = str(int(min_speed))
    max_speed = str(int(max_speed))

    


    image = cv2.putText(image, min_speed, (center[0]-radius-l(min_speed)[0]//2,center[1]+l(min_speed)[1]//2) , font, scale, white, baseline, cv2.LINE_AA)
    image = cv2.putText(image, max_speed, (center[0]+radius-l(max_speed)[0]//2,center[1]+l(max_speed)[1]//2) , font, scale, white, baseline, cv2.LINE_AA)
    image = cv2.putText(image, half_speed, (center[0]-l(half_speed)[0]//2,center[1]-radius+l(half_speed)[1]//2 ), font, scale, white, baseline, cv2.LINE_AA)

    image = cv2.putText(image, "m/s", (center[0]-l("m/s")[0]//2,center[1]+30) , font, 0.6, white, baseline, cv2.LINE_AA)
    return (image)
  
def gauge_altitude(image, alt, center, speed):
    assert isinstance(alt, float)

    image = cv2.ellipse(image, center, axes, 0, 105, 172, white, thickness)
    image = cv2.ellipse(image, center, axes, 0, 188, 255, white, thickness)
    
    image = cv2.ellipse(image, center, axes, 0, 45, 75, yellow, thickness)
    image = cv2.ellipse(image, center, axes, 0, 10, 45, orange, thickness)
    image = cv2.ellipse(image, center, axes, 0, 285, 352, red, thickness)


    c = np.cos(alt*np.pi/2000+np.pi/2)
    s = np.sin(alt*np.pi/2000+np.pi/2)
    image = cv2.line(image,  (center[0] , center[1] ), (center[0] -int(9*radius//10*c), center[1] - int(9*radius//10*s)), white, 3)

    for j in range(1,17):
      if j%4!=0:
        c = -np.cos(j*np.pi/8)
        s = np.sin(j*np.pi/8)
        image = cv2.line(image,  (center[0] -int((7+(j%2)/2)*radius//8*c), center[1] - int((7+(j%2)/2)*radius//8*s)), (center[0] -int(radius*c), center[1] - int(radius*s)), (235,231,231), 1)
    
    hand_size_x = 4*L("9999")[0]//5
    hand_size_y = 4*L("9999")[1]//5
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] +hand_size_x, center[1] +hand_size_y), black, -1)
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] +hand_size_x, center[1] +hand_size_y), white, 1)


    color_text = gray
    # Color only during freefall
    if speed>8:
      if alt>2000:
        color_text=green
      elif alt>1500:
        color_text=yellow
      elif alt>1000:
        color_text=orange
      else:
        color_text = red

    image = cv2.putText(image, str(int(alt)), (center[0]-L(str(int(alt)))[0]//2,center[1]+L(str(int(alt)))[1]//2) , cv2.FONT_HERSHEY_DUPLEX, bigscale, color_text, thickness, cv2.LINE_AA)
    # echelle
    image = cv2.putText(image, "3k", (center[0]-radius-l("3k")[0]//2,center[1]+l("3k")[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, "1k", (center[0]+radius-l("1k")[0]//2,center[1]+l("1k")[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, "4k", (center[0]-l("4k")[0]//2,center[1]-radius+l("4k")[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, "2k", (center[0]-l("2k")[0]//2,center[1]+radius+l("2k")[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)

    image = cv2.putText(image, "m", (center[0]-l("m")[0]//2,center[1]+l("m")[1]//2+30) , cv2.FONT_HERSHEY_DUPLEX, 0.6, white, 1, cv2.LINE_AA)
    return (image)

def gauge_glide_ratio(image, gr, center, min_gr, max_gr):
    # assert isinstance(gr, float)
    assert (max_gr>=min_gr)

    image = cv2.ellipse(image, center, axes, 0, 285, 350, white, thickness)
    image = cv2.ellipse(image, center, axes, 0, 190, 255, white, thickness)

    convert = gr - min_gr
    convert /= (max_gr - min_gr)
    convert *= np.pi
    convert += np.pi
    c = -np.cos(convert)
    s = -np.sin(convert)

    image = cv2.line(image,  (center[0] , center[1] ), (center[0] -int(9*radius//10*c), center[1] - int(9*radius//10*s)), white, 3)

    for j in range(1,9):
      if j%4!=0:
        c = -np.cos(j*np.pi/8)
        s = np.sin(j*np.pi/8)
        image = cv2.line(image,  (center[0] -int((7+(j%2)/2)*radius//8*c), center[1] - int((7+(j%2)/2)*radius//8*s)), (center[0] -int(radius*c), center[1] - int(radius*s)), (235,231,231), 1)
    
    hand_size_x = 3*L("99")[0]//4
    hand_size_y = 3*L("99")[1]//4
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] + hand_size_x, center[1] + hand_size_y), black, -1)
    image = cv2.rectangle(image, (center[0] -hand_size_x, center[1] - hand_size_y), (center[0] + hand_size_x, center[1] + hand_size_y), white, 1)

    gr = int(gr)

    # if hr>60 and hr<145:
    #   color_text=green
    # elif hr<160:
    #   color_text=yellow
    # else:
    #   color_text = red
    color_text = red

    image = cv2.putText(image, str(gr), (center[0]-L(str(gr))[0]//2,center[1]+L(str(gr))[1]//2) , cv2.FONT_HERSHEY_DUPLEX, bigscale, color_text, thickness, cv2.LINE_AA)
    
    
    half_gr = str(int((min_gr + max_gr)/2))
    min_gr = str(int(min_gr))
    max_gr = str(int(max_gr))


    image = cv2.putText(image, min_gr, (center[0]-radius-l(min_gr)[0]//2,center[1]+l(min_gr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, max_gr, (center[0]+radius-l(max_gr)[0]//2,center[1]+l(max_gr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)
    image = cv2.putText(image, half_gr, (center[0]-l(half_gr)[0]//2,center[1]-radius+l(half_gr)[1]//2) , cv2.FONT_HERSHEY_DUPLEX, 0.5, white, 1, cv2.LINE_AA)

    image = cv2.putText(image, "m/m", (center[0]-19,center[1]+30) , cv2.FONT_HERSHEY_DUPLEX, 0.6, white, 1, cv2.LINE_AA)
    return (image)