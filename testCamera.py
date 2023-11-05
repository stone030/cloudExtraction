# from picamera import PiCamera
# from time import sleep
# 
# camera = PiCamera()
# 
# camera.start_preview()
# sleep(50000)
import cv2 # OpenCV
import cvzone # to show FPS and draw augmented reality, and display multiple outputs

# Create an object that displays the FPS
FPSC = cvzone.FPS()

CameraCapture = cv2.VideoCapture(0)#"Live ISS stream record short.mp4") # or import a video like '/dataset/All-Way Pedestrian Crossing.mp4'
# Acquire a frame from the source
while True:
    (grabbed, frame) = CameraCapture.read()
    hf, wf, cf = frame.shape
    frame = cv2.resize(frame, (612, 393), interpolation=cv2.INTER_LINEAR)
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
#     frame = FPSC.update(frame, pos=(wf - 50, 50), color=(0, 0, 255), scale=2, thickness=2)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
