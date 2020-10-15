import pyautogui
import random
import time
import cv2
import mss
import numpy as np

def start_game():
    pyautogui.click(840,400,1,button='left')
    pyautogui.click(840, 400, 1, button='left')

def move(up,down):
    if(up == 1):
        pyautogui.keyDown('up')
    if (down == 1):
        pyautogui.keyDown('down')

#start_game()

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 250, "left": 535, "width": 620, "height": 220}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))

        print(img,img.shape,img.reshape(img.shape[2],img.shape[0],img.shape[1]).shape)
        #cv2.imshow("score",img[100:200,820:])
        #time.sleep(30)

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
