import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture(0)
color = (214, 116, 51)
color2 = (230, 116, 51)
zoom = False
maxZoom = False
faceZoom = False

while (cap.isOpened()):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    ret, frame = cap.read()
    #frame = pyautogui.screenshot()
    #frame = np.array(frame)
    #frame = frame[:, :, ::-1].copy()

    frame = cv2.resize(frame, (1280, 720))


    width, height = 1280, 720

    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)



    keyPressed = cv2.waitKey(1)
    if keyPressed == ord('k') and zoom != True:
        zoom = True
        maxZoom = False
        faceZoom = False
        print("True")
    elif keyPressed == ord('l') and (zoom == True or maxZoom == True or faceZoom):
        zoom = False
        maxZoom = False
        faceZoom = False
        print("False")
    elif keyPressed == ord('j') and maxZoom != True:
        zoom = False
        maxZoom = True
        faceZoom = False
        print("Maximum Zoom")
    elif keyPressed == ord('h') and faceZoom == False:
            faceZoom = True

    if zoom is True:
        pts1 = np.float32([[300, 169], [300, height - 169], [width - 300, height - 169], [width - 300, 169]])
        pts2 = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        frame = cv2.warpPerspective(frame, matrix, (width, height))
    if maxZoom == True:
        pts1 = np.float32([[400, 400/16 * 9], [400, height - 400/16 * 9], [width - 400, height - 400/16 * 9], [width  - 400,400/16 * 9]])
        pts2 = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        frame = cv2.warpPerspective(frame, matrix, (width, height))

    poly_fill_image = frame.copy()

    for (x, y, w, h) in faces:
        if faceZoom == True:
            pts1 = np.float32([[x-w/2, y], [x-w/2, y+(w*2/16*9)], [x+3*w/2, y+(w*2/16*9)],[x+3*w/2, y]])
            pts2 = np.float32([[0, 0], [0, height], [width, height], [width, 0]])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            frame = cv2.warpPerspective(frame, matrix, (width, height))
            poly_fill_image = cv2.warpPerspective(poly_fill_image, matrix, (width, height))
        else:
            cv2.circle(poly_fill_image, (int(x + w/2), int(y + h/2)), int(w/2), color2, 5)
            cv2.circle(poly_fill_image, (int(x + w/2), int(y + h/2)), 2, color2, 5)
            cv2.line(poly_fill_image, (int(1280 / 2), int(720 / 2)), (int(x + w/2), int(y + h/2)), color2, 1)

            xDegreesDiff = int((int(x + w/2)-640)/14.22)
            yDegreesDiff = -int((int(y + h/2)-360)/16)

            print(xDegreesDiff,yDegreesDiff)
            cv2.circle(poly_fill_image, (int(((x + w/2)+640)/2),int(((y + h/2)+360)/2)), 3, color2, 5)
            cv2.putText(poly_fill_image, str(xDegreesDiff) +", " + str(yDegreesDiff) , (int(((x + w/2)+640)/2) + 10, int(((y + h/2)+320)/2)+ 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color2, 2)



    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("Fps: "+ str(fps))
    pts = np.array([[0, 50], [0, 120], [450, 120], [400, 50]])
    cv2.fillPoly(poly_fill_image, [pts], color)

    pts = np.array([[1280, 50], [1280, 120], [1280 - 450, 120], [1280 - 400, 50]])
    cv2.fillPoly(poly_fill_image, [pts], color)

    if faceZoom == False:
        cv2.circle(poly_fill_image, (int(1280 / 2), int(720 / 2)), 30, color, thickness=5)
        cv2.circle(poly_fill_image, (int(1280 / 2), int(720 / 2)), 2, color, thickness=5)

    image_new = cv2.addWeighted(poly_fill_image, 0.2, frame, 0.8, 0)

    cv2.imshow("Display", image_new)

    if keyPressed == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
