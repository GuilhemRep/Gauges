import re
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime

import drawing

test = False

max_allowed_speed = 70

# Dimensions of video
height = 800
width = 200

# Error altitude; displayed_altitude + alt_error = real_altitude
alt_error = -50.

# name of video
name = "MAH04551"

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
fps = 30
path = "..."
data = open(path + name+".txt", "r")
video_filename = path +name+"_data.avi"
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))


# Extract data
data = re.findall(r'<trkpt lat=\"(.*?)\" lon=\"(.*?)\">\n<ele>(.*?)</ele>\n<time>(.*?)</time>(.*?)<ns3:hr>(.*?)</ns3:hr>(.*?)</trkpt>', data.read(), flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)

# Raw data
lat_ = []
lon_ = []
z_ = []
hr_=[]
time_ = []

initial_time = datetime.fromisoformat(data[0][3].replace("Z", "+00:00")).timestamp()

print("Initial length:",len(data))

for i in range(len(data)):
  # Only keep point if vertical speed possible
  if i>0 and abs(float(data[i][2])-float(data[i-1][2]))<max_allowed_speed:
    lat_.append(float(data[i][0]))
    lon_.append(float(data[i][1]))
    z_.append(float(data[i][2])+ alt_error)
    hr_.append(int(data[i][5]))
    time_.append(int(datetime.fromisoformat(data[i][3].replace("Z", "+00:00")).timestamp()-initial_time))
    # time_.append(datetime.fromisoformat(data[i][3].replace("Z", "+00:00")).time())
  
print("Removed",len(data)-len(time_), "bad points")


# Add missing data
i=0
while i<len(time_)-1:
  dt = time_[i+1]-time_[i]
  if dt!=1:
    print("Missing", dt-1, ("point " if dt==2 else "points"), "at time",time_[i])
    missing_time = []
    missing_hr = []
    missing_z = []
    missing_lat = []
    missing_lon = []
    for t in range(1,dt):
      missing_time.append(int(((dt-t)*time_[i] + t*time_[i+t])//dt))
      missing_hr.append(int(((dt-t)*hr_[i] + t*hr_[i+t])//dt))
      missing_z.append(int(((dt-t)*z_[i] + t*z_[i+t])//dt))
      missing_lat.append(((dt-t)*lat_[i] + t*lat_[i+t])//dt)
      missing_lon.append(((dt-t)*lon_[i] + t*lon_[i+t])//dt)
    time_[i+1:i+1] = missing_time
    hr_[i+1:i+1] = missing_hr
    z_[i+1:i+1] = missing_z
    lat_[i+1:i+1] = missing_lat
    lon_[i+1:i+1] = missing_lon
    i+=dt+1
  else:
    i+=1

# Test the absence of missing points
for i in range(len(time_)-1):
  if time_[i+1] - time_[i] != 1:
    print("error",i)
  # assert time_[i+1] - time_[i] == 1

corrected_length = len(time_)
print("Corrected length:",corrected_length)


# Interpolation algo (= linear if spline_constant = 2)
interpol_constant = 15 # Desired number of values per second in the generated video
assert fps%interpol_constant == 0

spline_constant = 2
assert spline_constant>0
def spline(l,i):
  assert len(l) == spline_constant
  def f(x):
    t=0
    for k in range(spline_constant):
      tt = 1
      for j in range(spline_constant):
        if j!=k:
          tt*= (x-j)
      for j in range(spline_constant):
        if j!=k:
          tt/= (k-j)
      t+=tt*l[k]
    return t
  return (f(i/interpol_constant))


# Cleaned data
x = []
y = []
z = []
hr = []
time = []
lat = []
lon = []



# Computed data
speed = []

north_speed = []
east_speed = []

horizontal_speed = []

glide_ratio = []

number_of_frames = len(time_)-spline_constant

def hspeed(lat1,lat2, lon1,lon2):
  lat1 *= np.pi / 180.0
  lon1 *= np.pi / 180.0
  lat2 *= np.pi / 180.0
  lon2 *= np.pi / 180.0

  r = 6378100 + z[i]; # Altitude from center of the earth (lol)

  rho1 = r * np.cos(lat1)
  z1 = r * np.sin(lat1)
  x1 = rho1 * np.cos(lon1)
  y1 = rho1 * np.sin(lon1)

  rho2 = r * np.cos(lat2)
  z2 = r * np.sin(lat2)
  x2 = rho2 * np.cos(lon2)
  y2 = rho2 * np.sin(lon2)

  dot = (x1 * x2 + y1 * y2 + z1 * z2)
  cos_theta = dot / (r * r)
  theta = np.arccos(cos_theta)

  return(interpol_constant* r * theta)

# Interpolation of heart rate
for i in range(number_of_frames):
  for k in range(interpol_constant):
    time.append(time_[i])

    hr_interpol = spline(hr_[i:i+spline_constant:1],k) # Spline
    hr.append(hr_interpol) 

    z_interpol = spline(z_[i:i+spline_constant:1],k) # Spline
    z.append(z_interpol)

  # Interpolation of speed
for i in range(number_of_frames):
  current_horizontal_speed = hspeed(lat_[i], lat_[i+1], lon_[i], lon_[i+1])

  current_vertical_speed = z_[i]-z_[i+1]
  gr = current_horizontal_speed/current_vertical_speed

  current_horizontal_speed = round(current_horizontal_speed,1)
  current_vertical_speed = round(current_vertical_speed, 1)
  gr = round(gr,1)
  
  
  for _ in range(interpol_constant):
    # north_speed.append(ns)
    # east_speed.append(es)
    horizontal_speed.append(current_horizontal_speed)
    if np.abs(gr)<100:
      glide_ratio.append(gr)
    else:
      glide_ratio.append(0)

    # glide_ratio.append(current_horizontal_speed)
    speed.append(current_vertical_speed)

min_alt = min(z)
max_alt = max(z)
  
min_hr = min(hr)
max_hr = max(hr)

max_speed = max(speed)
min_speed = min(speed)

max_gr = max(glide_ratio)
min_gr = min(glide_ratio)

number_of_frames = len(speed)

assert (number_of_frames==len(time)
      and number_of_frames==len(hr)
      and number_of_frames==len(z) 
      and number_of_frames==len(speed)
      and number_of_frames==len(glide_ratio))

print("Length after interpolation:",len(z))

# Position of gauges
org_hr = (width//2,100)
org_alt = (width//2,270)
org_speed = (width//2,460)
org_glide = (width//2,600)

org_time = (-190,360)

print("Starting generation of video...")
c = 0
for i in range(200 if test else number_of_frames):
  # print(i)
  if c<=i-200:
    c+=200
    print(i,"/",number_of_frames)
  for _ in range(fps//interpol_constant):
      frame = np.zeros((height, width, 3), dtype=np.uint8)
      frame = drawing.gauge_heart_rate(frame, hr[i], org_hr, min_hr, max_hr)
      frame = drawing.gauge_altitude(frame, z[i], org_alt, speed[i])
      frame = drawing.gauge_speed(frame, speed[i], org_speed, min_speed, max_speed)
      frame = drawing.gauge_glide_ratio(frame, glide_ratio[i], org_glide, min_gr, max_gr)
      frame = frame.astype(np.uint8)
      out.write(frame)
# cv2.putText(frame, "Tt", (210,190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),1)
print(number_of_frames,"/",number_of_frames, "-----> Finished!")

out.release()