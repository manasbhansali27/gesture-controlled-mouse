import cv2
import numpy as np
import HandTracking as htm
import pyautogui
import time


wCam, hCam = 640, 480
frameR = 100  
smoothening = 7
clickThreshold = 100  
scrollSpeed = 2  
scrollSensitivity = 20  


pyautogui.FAILSAFE = False

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
lastClickTime = time.time()


last_thumb_y = None
scrolling_direction = 0  

cap = cv2.VideoCapture(0)  
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)

while True:
    
    success, img = cap.read()
    

    img = cv2.flip(img, 1)
    
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    
    if len(lmList) != 0:
        
        x1, y1 = lmList[8][1:]  
        x2, y2 = lmList[12][1:]  
        x_thumb, y_thumb = lmList[4][1:]  

        
        fingers = detector.fingersUp()

        
        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, pyautogui.size().width))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, pyautogui.size().height))


            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            
            pyautogui.moveTo(clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        
        if fingers[1] == 1 and fingers[2] == 1:
            
            length, img, lineInfo = detector.findDistance(8, 12, img)

            
            if length < clickThreshold and time.time() - lastClickTime > 0.5:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                lastClickTime = time.time()

        
        if fingers[4] == 1 and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:

            pyautogui.scroll(-scrollSpeed * scrollSensitivity)
            cv2.putText(img, "Open Hand (Scroll Down)", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        elif fingers[1] == 1 and fingers[4] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0:

            pyautogui.scroll(scrollSpeed * scrollSensitivity)
            cv2.putText(img, "Thumb Up (Scroll Up)", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
