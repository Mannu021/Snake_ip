import cv2
import mediapipe as mp
import time
import math
import numpy as np
import pyautogui
cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mp_drawing = mp.solutions.drawing_utils
pTime=0
cTime=0
count=0
x=[0]*4
y=[0]*4

with mpHands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands: 
    while cap.isOpened():
        sucess,img=cap.read()
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        imgHeight,imgWidth,_ = imgRGB.shape
        imgpro=hands.process(imgRGB)

        if imgpro.multi_hand_landmarks:
            for hand in imgpro.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(0, 0, 250), thickness=2, circle_radius=2),)
        
        if imgpro.multi_hand_landmarks!=None:
            for handlm in imgpro.multi_hand_landmarks:
                for point in mpHands.HandLandmark:
    
        
                    normalizedLandmark = handlm.landmark[point]
                    pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imgWidth, imgHeight)
        
                    point=str(point)
                    if point=='HandLandmark.INDEX_FINGER_TIP':
                        try:
                            x[count]=pixelCoordinatesLandmark[0]
                            y[count]=pixelCoordinatesLandmark[1]
                            count+=1
                            if count==6:
                                if abs(x[3]-x[0])>=15 or abs(y[3]-y[0])>=15:
                                    deltaX = x[3]-x[0]
                                    deltaY = y[3]-y[0]
                                    degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
                                    print(degrees_temp)
                                    if -45>=degrees_temp>=-135:
                                        print("left")
                                        pyautogui.press('left')
                                    elif 45<=degrees_temp<135:
                                        print("right")
                                        pyautogui.press('right')
                                    elif 135<=degrees_temp<=180 or -135>=degrees_temp>=-180:
                                        print("up")
                                        pyautogui.press('up')
                                    else:
                                        print("down")
                                        pyautogui.press('down')
                                count=0
                                x=[0]*4
                                y=[0]*4
                        except:
                            pass





        cTime=time.time()    
        fps=1/(cTime-pTime)
        pTime=cTime
        fpss=str(int(fps))
        cv2.putText(img,fpss,(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)




        cv2.imshow("Image",img)
        if cv2.waitKey(10) & 0xFF == 27:
            cv2.destroyWindow()
    cap.release()
