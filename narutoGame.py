import cv2
import numpy as np
import pyautogui as pag
import time


from PIL import ImageGrab as ig
def grab_it(bbox=None):
    ssc = ig.grab(bbox)
    ssc = np.array(ssc)
    ssc = cv2.cvtColor(ssc, cv2.COLOR_RGB2BGR)
    return ssc


class Naruto_Game:
    def __init__(self, path):
        image = cv2.imread(path)
        self.image = image
        self.height = image.shape[0]
        self.width = image.shape[1]
        self.location = None

    def match(self, screen_img):
        result = cv2.matchTemplate(screen_img, self.image, cv2.TM_CCOEFF_NORMED)
        min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        bottom_right = (max_loc[0] + self.width, max_loc[1] + self.height)
        if max_value > 0.80:
            self.location = (top_left, bottom_right)
            return True
        else:
            self.location = None
            return False

Naruto = Naruto_Game("Naruto3''.png")

Obstacle = [Naruto_Game("Fire'.png"), Naruto_Game("Kakashi'.png"), Naruto_Game("Kakashi''.png"),Naruto_Game("Katsuyu''.png"), Naruto_Game("Sasuke+Trash'.png"),
           Naruto_Game("Shuriken1'.png"), Naruto_Game("Gaara'.png"), Naruto_Game("Orochimaru'.png")]

speed = 3.0

acceleration = 0.32

distanceThreshold = 100

while True:
    screen = grab_it()
    if Naruto.match(screen):
        if Naruto.location != None:
            topleft_x = 100
            topleft_y = 420
            bottomRight_x = 971
            bottomRight_y = 601
            TopLeft = (topleft_x, topleft_y)
            BottomRight = (bottomRight_x, bottomRight_y)
            break

pag.press('space')

startTime = time.time()

prevTime = time.time()

while True:
    main_panel = grab_it(bbox=(TopLeft[0], TopLeft[1], BottomRight[0], BottomRight[1]))

    if time.time() - startTime > 12 and Naruto.location:
        speed += speed * acceleration
        distanceThreshold += speed
        startTime = prevTime
        prevTime = time.time()

    if Naruto.match(main_panel):
        if Naruto.location:
            cv2.rectangle(main_panel, Naruto.location[0], Naruto.location[1], (255, 0, 0), 2)

    for enemy in Obstacle:
        if enemy.match(main_panel):
            cv2.rectangle(main_panel, enemy.location[0], enemy.location[1], (0, 0, 255), 2)
            if Naruto.location:
                horizontalDistance = enemy.location[0][0] - Naruto.location[1][0]
                verticalDistance = Naruto.location[0][1] - enemy.location[1][1]

                if horizontalDistance <= distanceThreshold and horizontalDistance >= 0:
                    if verticalDistance <= 0:
                        pag.press('space')
                        break

    cv2.imshow("Naruto Game", main_panel)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break