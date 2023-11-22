import time
import glob,os
import cv2
from send_mail_alert import send_mail
from threading import Thread


video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame_gau = None
status_list =[]
count = 0

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    if first_frame_gau is None:
        first_frame_gau = gray_frame_gau_blur

    delta_frame_gau = cv2.absdiff(first_frame_gau, gray_frame_gau_blur)

    thresh_frame=cv2.threshold(delta_frame_gau,70,255,cv2.THRESH_BINARY)[1]
    dil_frame= cv2.dilate(thresh_frame,None,iterations=2)

    contours,check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("My video", dil_frame)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x,y,w,h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if rectangle.any():
            status=1
            cv2.imwrite(f'images/frame{count}.png',frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images)/2)

    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] ==0:
        image_with_object = all_images[index]

        mail_thread = Thread(target=send_mail,args=(image_with_object,))
        mail_thread.daemon = True
        mail_thread.start()

        #clean_folder_thread= Thread(target= clean_folder)
        #clean_folder_thread.daemon =True
        #clean_folder_thread.start()



    cv2.imshow("processed video",frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break




video.release()
clean_folder()
