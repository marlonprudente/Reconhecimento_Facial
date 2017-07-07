import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
DESATIVAR=15
COM_RASP=14
SERVO = 4
camera=0
semface=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(COM_RASP, GPIO.OUT)
GPIO.setup(DESATIVAR, GPIO.OUT)
p = GPIO.PWM(SERVO, 50)
p.start(2.5)
def abrir():
    global p
    p.ChangeDutyCycle(7.5)
    time.sleep(7)
    p.ChangeDutyCycle(2.5)
    time.sleep(0.5)
faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0)
rec=cv2.createLBPHFaceRecognizer(1,8,8,8,60.0)
rec.load("/home/pi/Desktop/reconhecimento facial/recognizer/trainningData.yml")
id=0
cam.set(3,320)
cam.set(4,240)
font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_COMPLEX_SMALL,5,1,0,4)
start = time.time()
GPIO.output(COM_RASP, GPIO.LOW)
validacao=1
while True:   
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    print 'q' 
    if semface==0:
	semface=1
	noface=faceDetect.detectMultiScale(gray,1.3,5)
	print noface
	print 'aaaaa'
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    print faces
    if faces!=noface and camera==1:
	camera=0
        while faces!=noface:
	  ret,img=cam.read();
	  gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          faces=faceDetect.detectMultiScale(gray,1.3,5)
	  print faces
    faces=faceDetect.detectMultiScale(gray,1.3,5)

    print faces
    for(x,y,w,h) in faces:
         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
         if (validacao==1):
             start = time.time()
             validacao=0
         id,conf=rec.predict(gray[y:y+h,x:x+w])
         print time.time() - start
         if (id==1 or id==2 or id==3):
             print id
             GPIO.output(DESATIVAR, GPIO.HIGH)
             abrir()
             GPIO.output(DESATIVAR, GPIO.LOW)
	     time.sleep(6)
             validacao=1
	     camera=1
	     # GPIO.cleanup()
	     break
         elif ((time.time() - start)>=8):
             GPIO.output(COM_RASP, GPIO.HIGH)
             time.sleep(0.2)
             GPIO.output(COM_RASP, GPIO.LOW)
             validacao=1
        #cv2.cv.PutText(cv2.cv.fromarray(img),str(id),(x,y+h),font,255
cam.release()
cv2.destroyAllWindows()


