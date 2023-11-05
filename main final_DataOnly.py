# This script continuously grabs frames from the camera and displays them after processing them.

# Import packages
import cv2 # OpenCV
import os  # for smooth exit
import cvzone # to show FPS and draw augmented reality, and display multiple outputs
import numpy as np # generate mask matrix
#to use ISS API we import the following:
import urllib.request
import json
import imutils
import time

start = time.time()
# Import Base map (without clouds)
# base_map = cv2.imread('Base_map.png')
# cv2.imshow('Base', base_map)
# cv2.waitKey(0)

# Create an object that displays the FPS
FPSC = cvzone.FPS()

## Cyclone icon -for augmented view-
# carWarning = cv2.imread("D:/Program Files/EaseUS RecExperts/3436777.png", cv2.IMREAD_UNCHANGED)
# carWarning = resize(carWarning, width=20, inter=cv2.INTER_CUBIC)
# hw, ww, cw = carWarning.shape

# Open the camera //here you specify the stream input, either providing a file path string to be opened, or
# selecting camera ID integer number to capture its stream (camera ID number starts from 0 as for built-in camera)
CameraCapture = cv2.VideoCapture(0)#"Live ISS stream record short.mp4") # or import a video like '/dataset/All-Way Pedestrian Crossing.mp4'

# Check if the camera is opened
if not CameraCapture.isOpened():
    print('Unable to open camera!')
    os._exit(1)
print('Camera is attached successfully')

#---------------------------------------------------------------------------
# Check our conditions like location from GPS data and daylight level to start capturing the view
# detect location from GPS data
Near_Oman = 0
#check conditions (open iss.bin and read last line to extract lon/lat coordinates)
Near_Oman = 0
lon = 0
lat = 0
region = ""

# Tile sigmentation x = [w, h]
tile = {
    '79': [99, 688],
    '78': [99, 589],
    '91': [2, 688],
    '35': [492, 1130],
    '23': [590, 1130],
    '11': [687, 1130],

    '93': [2, 900],
    '94': [2, 1024],
    '95': [2, 1130],
    '82': [99, 1024],
    '83': [99, 1130],

    '26': [492, 197],

    '60': [198, 2],
    '48': [295, 2],
    '37': [393, 100],
    '25': [492, 100],
    '13': [590, 100],
    '14': [590, 197],
    '2': [687, 197],

    '68': [198, 786],
    '69': [198, 900],
    '55': [295, 688],
    '56': [295, 786],
    '57': [295, 900],
    '58': [295, 1024],
    '59': [295, 1130],
    '44': [393, 786],
    '45': [393, 900],
    '46': [393, 1024],
    '47': [393, 1130],
    '32': [492, 786],
    '33': [492, 900],
    '34': [492, 1024],
    '21': [590, 900],

    '65': [198, 492],
    '64': [198, 393],
    '77': [99, 492],
    '76': [99, 393],
    '87': [2, 296],
    '88': [2, 393],
    '89': [2, 492],

    '86': [2, 197],
    '74': [99, 197],
    '75': [99, 296],

    '22': [590, 1024],
    '10': [687, 1024],

    '73': [99, 100],
    '61': [198, 100],

    '1': [687, 100],
    '81': [99, 900],

    '62': [198, 197],
    '63': [198, 296],
    '52': [295, 393],
    '51': [295, 296],
    '50': [295, 197],
    '38': [393, 197],

    '20': [590, 786],
    '8': [687, 786],
    '9': [687, 900],
    '7': [687, 688],

    '70': [198, 1024],
    '71': [198, 1130],

    '53': [295, 492],
    '54': [295, 589],
    '41': [393, 492],

    '6': [687, 589],
    '5': [687, 492],
    '4': [687, 393],
    '17': [590, 492],
    '18': [590, 589],
    '19': [590, 688],
    '31': [492, 688],
    '30': [492, 589],
    '29': [492, 492],
    '43': [393, 688],
    '42': [393, 589],

    '66': [198, 589],
    '67': [198, 688],
    '80': [99, 786],

    '72': [99, 2],
    '49': [295, 100],

    '15': [590, 296],
    '28': [492, 393],
    '3': [687, 296],
    '16': [590, 393],

    '36': [393, 2],
    '24': [492, 2],

    '12': [590, 2],
    '85': [99, 100],
    '84': [2, 2],
    '90': [2, 589],
    '92': [2, 786],
    '0': [687, 2],
    '39': [393, 296],
    '27': [492, 296],
    '40': [393, 393],
}

# tracking lon & lat of ISS
def ISS_GroundTrack():
    global lat, lon
    # load the current status of the ISS in real-time
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    # Extract the ISS location
    location = result["iss_position"]
    lat = location['latitude']
    lon = location['longitude']

    # store final values as floats
    lat = float(lat)
    lon = float(lon)

#---------------------------------------------------------------------------
while True:
    #ISS_GroundTrack()
    # disable next manual Values to have real lon/lat:
    lon, lat = 21, 61
    print("\nLatitude: " + str(lat))
    print("\nLongitude: " + str(lon))
    Near_Oman = (lon > 0 and lon < 45) and (lat > 30 and lat < 90)
    # To set the conditions as True manually, just disable ISS_GroundTrack() inthe main loop, and
    # enable the following line:
    Near_Oman = True
    print("\nNear_Oman = ", Near_Oman)
    # if near Oman And it is day time, start capturing pictures
    # now the default is daytime, as we didn't read data from a light sensor yet:
    Day_time = True

    run_once = 0
    while Near_Oman and Day_time:
        # For manual Configuration, disable the following line, also set the if statement to not:
        # ISS_GroundTrack()

        print("\nLatitude: " + str(lat))
        print("\nLongitude: " + str(lon))
        if not((lon > 0 and lon < 45) and (lat > 30 and lat < 90)):
            Near_Oman = 0
            print("\nExitted operating zone.______________________")
            with open("Tile_description.bin", "a") as f:
                f.write("\n------------\nExitting Operating zone!\n------------\n")
            break

        if run_once == 0:
            region1 = '1'
            print("\nEntered operating zone!!*********\n")
            # Writing the bits in a text file with a compression method
            with open("Tile_description.bin", "w") as f:
                f.write("Entered Operating zone!\n============ \n")
            run_once = 1

        # labelling tiles:
        if (lon >= 0 and lon < 5) and (lat >= 30 and lat < 35):
            region = "0"
        elif (lon >= 0 and lon < 5) and (lat >= 35 and lat < 40):
            region = "1"
        elif (lon >= 0 and lon < 5) and (lat >= 40 and lat < 45):
            region = "2"
        elif (lon >= 0 and lon < 5) and (lat >= 45 and lat < 50):
            region = "3"
        elif (lon >= 0 and lon < 5) and (lat >= 50 and lat < 55):
            region = "4"
        elif (lon >= 0 and lon < 5) and (lat >= 55 and lat < 60):
            region = "5"
        elif (lon >= 0 and lon < 5) and (lat >= 60 and lat < 65):
            region = "6"
        elif (lon >= 0 and lon < 5) and (lat >= 65 and lat < 70):
            region = "7"
        elif (lon >= 0 and lon < 5) and (lat >= 70 and lat < 75):
            region = "8"
        elif (lon >= 0 and lon < 5) and (lat >= 75 and lat < 80):
            region = "9"
        elif (lon >= 0 and lon < 5) and (lat >= 80 and lat < 85):
            region = "10"
        elif (lon >= 0 and lon < 5) and (lat >= 85 and lat < 90):
            region = "11"

        elif (lon >= 5 and lon < 10) and (lat >= 30 and lat < 35):
            region = "12"
        elif (lon >= 5 and lon < 10) and (lat >= 35 and lat < 40):
            region = "13"
        elif (lon >= 5 and lon < 10) and (lat >= 40 and lat < 45):
            region = "14"
        elif (lon >= 5 and lon < 10) and (lat >= 45 and lat < 50):
            region = "15"
        elif (lon >= 5 and lon < 10) and (lat >= 50 and lat < 55):
            region = "16"
        elif (lon >= 5 and lon < 10) and (lat >= 55 and lat < 60):
            region = "17"
        elif (lon >= 5 and lon < 10) and (lat >= 60 and lat < 65):
            region = "18"
        elif (lon >= 5 and lon < 10) and (lat >= 65 and lat < 70):
            region = "19"
        elif (lon >= 5 and lon < 10) and (lat >= 70 and lat < 75):
            region = "20"
        elif (lon >= 5 and lon < 10) and (lat >= 75 and lat < 80):
            region = "21"
        elif (lon >= 5 and lon < 10) and (lat >= 80 and lat < 85):
            region = "22"
        elif (lon >= 5 and lon < 10) and (lat >= 85 and lat < 90):
            region = "23"

        elif (lon >= 10 and lon < 15) and (lat >= 30 and lat < 35):
            region = "24"
        elif (lon >= 10 and lon < 15) and (lat >= 35 and lat < 40):
            region = "25"
        elif (lon >= 10 and lon < 15) and (lat >= 40 and lat < 45):
            region = "26"
        elif (lon >= 10 and lon < 15) and (lat >= 45 and lat < 50):
            region = "27"
        elif (lon >= 10 and lon < 15) and (lat >= 50 and lat < 55):
            region = "28"
        elif (lon >= 10 and lon < 15) and (lat >= 55 and lat < 60):
            region = "29"
        elif (lon >= 10 and lon < 15) and (lat >= 60 and lat < 65):
            region = "30"
        elif (lon >= 10 and lon < 15) and (lat >= 65 and lat < 70):
            region = "31"
        elif (lon >= 10 and lon < 15) and (lat >= 70 and lat < 75):
            region = "32"
        elif (lon >= 10 and lon < 15) and (lat >= 75 and lat < 80):
            region = "33"
        elif (lon >= 10 and lon < 15) and (lat >= 80 and lat < 85):
            region = "34"
        elif (lon >= 10 and lon < 15) and (lat >= 85 and lat < 90):
            region = "35"

        elif (lon >= 15 and lon < 20) and (lat >= 30 and lat < 35):
            region = "36"
        elif (lon >= 15 and lon < 20) and (lat >= 35 and lat < 40):
            region = "37"
        elif (lon >= 15 and lon < 20) and (lat >= 40 and lat < 45):
            region = "38"
        elif (lon >= 15 and lon < 20) and (lat >= 45 and lat < 50):
            region = "39"
        elif (lon >= 15 and lon < 20) and (lat >= 50 and lat < 55):
            region = "40"
        elif (lon >= 15 and lon < 20) and (lat >= 55 and lat < 60):
            region = "41"
        elif (lon >= 15 and lon < 20) and (lat >= 60 and lat < 65):
            region = "42"
        elif (lon >= 15 and lon < 20) and (lat >= 65 and lat < 70):
            region = "43"
        elif (lon >= 15 and lon < 20) and (lat >= 70 and lat < 75):
            region = "44"
        elif (lon >= 15 and lon < 20) and (lat >= 75 and lat < 80):
            region = "45"
        elif (lon >= 15 and lon < 20) and (lat >= 80 and lat < 85):
            region = "46"
        elif (lon >= 15 and lon < 20) and (lat >= 85 and lat < 90):
            region = "47"

        elif (lon >= 25 and lon < 30) and (lat >= 30 and lat < 35):
            region = "48"
        elif (lon >= 25 and lon < 30) and (lat >= 35 and lat < 40):
            region = "49"
        elif (lon >= 25 and lon < 30) and (lat >= 40 and lat < 45):
            region = "50"
        elif (lon >= 25 and lon < 30) and (lat >= 45 and lat < 50):
            region = "51"
        elif (lon >= 25 and lon < 30) and (lat >= 50 and lat < 55):
            region = "52"
        elif (lon >= 25 and lon < 30) and (lat >= 55 and lat < 60):
            region = "53"
        elif (lon >= 25 and lon < 30) and (lat >= 60 and lat < 65):
            region = "54"
        elif (lon >= 25 and lon < 30) and (lat >= 65 and lat < 70):
            region = "55"
        elif (lon >= 25 and lon < 30) and (lat >= 70 and lat < 75):
            region = "56"
        elif (lon >= 25 and lon < 30) and (lat >= 75 and lat < 80):
            region = "57"
        elif (lon >= 25 and lon < 30) and (lat >= 80 and lat < 85):
            region = "58"
        elif (lon >= 25 and lon < 30) and (lat >= 85 and lat < 90):
            region = "59"
            
        elif (lon >= 20 and lon < 25) and (lat >= 30 and lat < 35):
            region = "60"
        elif (lon >= 20 and lon < 25) and (lat >= 35 and lat < 40):
            region = "61"
        elif (lon >= 20 and lon < 25) and (lat >= 40 and lat < 45):
            region = "62"
        elif (lon >= 20 and lon < 25) and (lat >= 45 and lat < 50):
            region = "63"
        elif (lon >= 20 and lon < 25) and (lat >= 50 and lat < 55):
            region = "64"
        elif (lon >= 20 and lon < 25) and (lat >= 55 and lat < 60):
            region = "65"
        elif (lon >= 20 and lon < 25) and (lat >= 60 and lat < 65):
            region = "66"
        elif (lon >= 20 and lon < 25) and (lat >= 65 and lat < 70):
            region = "67"
        elif (lon >= 20 and lon < 25) and (lat >= 70 and lat < 75):
            region = "68"
        elif (lon >= 20 and lon < 25) and (lat >= 75 and lat < 80):
            region = "69"
        elif (lon >= 20 and lon < 25) and (lat >= 80 and lat < 85):
            region = "70"
        elif (lon >= 20 and lon < 25) and (lat >= 85 and lat < 90):
            region = "71"

        elif (lon >= 30 and lon < 35) and (lat >= 30 and lat < 35):
            region = "72"
        elif (lon >= 30 and lon < 35) and (lat >= 35 and lat < 40):
            region = "73"
        elif (lon >= 30 and lon < 35) and (lat >= 40 and lat < 45):
            region = "74"
        elif (lon >= 30 and lon < 35) and (lat >= 45 and lat < 50):
            region = "75"
        elif (lon >= 30 and lon < 35) and (lat >= 50 and lat < 55):
            region = "76"
        elif (lon >= 30 and lon < 35) and (lat >= 55 and lat < 60):
            region = "77"
        elif (lon >= 30 and lon < 35) and (lat >= 60 and lat < 65):
            region = "78"
        elif (lon >= 30 and lon < 35) and (lat >= 65 and lat < 70):
            region = "79"
        elif (lon >= 30 and lon < 35) and (lat >= 70 and lat < 75):
            region = "80"
        elif (lon >= 30 and lon < 35) and (lat >= 75 and lat < 80):
            region = "81"
        elif (lon >= 30 and lon < 35) and (lat >= 80 and lat < 85):
            region = "82"
        elif (lon >= 30 and lon < 35) and (lat >= 85 and lat < 90):
            region = "83"
            
        elif (lon >= 35 and lon < 40) and (lat >= 30 and lat < 35):
            region = "84"
        elif (lon >= 35 and lon < 40) and (lat >= 35 and lat < 40):
            region = "85"
        elif (lon >= 35 and lon < 40) and (lat >= 40 and lat < 45):
            region = "86"
        elif (lon >= 35 and lon < 40) and (lat >= 45 and lat < 50):
            region = "87"
        elif (lon >= 35 and lon < 40) and (lat >= 50 and lat < 55):
            region = "88"
        elif (lon >= 35 and lon < 40) and (lat >= 55 and lat < 60):
            region = "89"
        elif (lon >= 35 and lon < 40) and (lat >= 60 and lat < 65):
            region = "90"
        elif (lon >= 35 and lon < 40) and (lat >= 65 and lat < 70):
            region = "90"
        elif (lon >= 35 and lon < 40) and (lat >= 70 and lat < 75):
            region = "91"
        elif (lon >= 35 and lon < 40) and (lat >= 75 and lat < 80):
            region = "92"
        elif (lon >= 35 and lon < 40) and (lat >= 80 and lat < 85):
            region = "93"
        elif (lon >= 35 and lon < 40) and (lat >= 85 and lat < 90):
            region = "94"
        else:
            region = "Outside Operating zone---------------------"
            continue
        print("CubeSat above: ", region)
        # sleep/wait check if same region then wait until reaching another region
        if region == region1:
            time.sleep(5)
            continue

        region1 = region

        with open("Tile_description.bin", "a") as f:
            f.write(region + " \n")

        # Acquire a frame from the source
        (grabbed, frame) = CameraCapture.read()
        frame = cv2.resize(frame, (612, 393), interpolation=cv2.INTER_LINEAR)

        # Check if a frame was successfully acquired
        if not grabbed:
            print('Failed to capture frame!')
            continue # or break
        hf, wf, cf = frame.shape

        # Remove the noise from the frame
        #Blurred = cv2.GaussianBlur(frame, (3, 3), 0)
        # Convert BGR to HSL
        imgHLS = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        # define range of blue color in HSV
        lower = np.array([0, 190, 0])
        upper = np.array([255, 255, 255])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(imgHLS, lower, upper)
        # thresholded = cv2.bitwise_and(frame, frame, mask=mask)

        # Taking a matrix of size 3 as the kernel
        kernel = np.ones((3, 3), np.uint8)
        mask_Er = cv2.erode(mask, kernel, iterations=1)
        mask_Di = cv2.dilate(mask_Er, kernel, iterations=9)

        # Find contours
#         Contours = cv2.findContours(mask_Di.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         Contours = imutils.grab_contours(Contours)
# 
#         Total_contours = 0
#         for Contour in Contours:
#             (x, y, w, h) = cv2.boundingRect(Contour)
#             # Process contours that may represent a person
#             ContourArea = cv2.contourArea(Contour)
#             Total_contours += 1
# 
#             # Outline the contour and write the name of the shape. Orange color is used.
#             cv2.drawContours(frame, [Contour], -1, (0, 192, 255), 2)
#             # Note: These Limits are based on the Processed Frame size!
#             if ContourArea < 2000:
#                 label = 'Small'
#             elif ContourArea < 30000:
#                 label = 'Med'
#             elif ContourArea < 150000:
#                 label = 'Large'
#             elif ContourArea >= 150000:
#                 label = 'Typhoon'
#             if label == 'Typhoon':
#                 cv2.putText(frame, label, (x + (w // 2), y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
#             elif label == 'Large':
#                 cv2.putText(frame, label, (x + (w // 2), y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
#             elif label == 'Med':
#                 cv2.putText(frame, label, (x + (w // 2), y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 0, 200),
#                             2)
#             elif label == 'Small':
#                 cv2.putText(frame, label, (x + (w // 2), y + (h // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
#         print("Total Contours are: {}".format(Total_contours))

        # Clouds Ranks
        Rank_small, Rank_Medium, Rank_Large, Rank_Typhoon = 0, 0, 0, 0
        # 32x32 sub-tiles (on the virtual map)
        sub_num = 32
        #
        sub_lenh = hf//sub_num
        sub_lenw = wf//sub_num
        sub = 0
        # cv2.imshow('mask', mask)
        # print(len(mask))
        # cv2.waitKey(0)
        # exit()
        for i in range(sub_num):
            for ii in range(sub_num):
                subtm = mask[(sub_lenh * i):sub_lenh * (i + 1), (sub_lenw * ii):sub_lenw * (ii + 1)]

                # percentage of clouds
                cloud_pixels = np.sum(subtm == 255)
                total_pixels = np.sum(subtm == 0) + cloud_pixels
                cloud_percentage = cloud_pixels / total_pixels * 100

                # Note: These Limits are based on the Processed tile size!
                # clouds classification
                rank = ''
                if cloud_percentage < 20:
                    rank = '00'
                elif cloud_percentage < 40:
                    # Small clouds
                    Rank_small += 1
                    rank = '01'
                elif cloud_percentage < 65:
                    # Medium clouds
                    cloud_percentage += 1
                    rank = '10'
                else:
                    # Large clouds
                    cloud_percentage += 1
                    rank = '11'

                # ---------------------------------------------------------------------------
                # Writing the bits in a text file with a compression method
                with open("Tile_description.bin", "a") as f:
                    f.write("{} ".format(sub) + rank + ' \n')
                sub += 1

        # Done! ---------------------------------------------------------------------
        # mentioning FPS rate on top of window display
        cv2.imwrite('captured.jpeg', frame)
#         frame = FPSC.update(frame, pos=(wf - 200, 50), color=(0, 0, 255), scale=2, thickness=2)[
#         end = time.time()
#         print('time spent for 1 image: ')
#         print(end - start)
#         cv2.imshow("Processing", frame)
#         key = cv2.waitKey(1)

# clean up the camera and close any open windows
# CameraCapture.release()
# cv2.destroyAllWindows()
