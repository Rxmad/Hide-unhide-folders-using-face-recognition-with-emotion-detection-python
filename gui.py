import tkinter as tk
import tkinter.font as font 
from pathlib import Path
import time

def isPython(versionNumber): 
    import platform
    return platform.python_version().startswith(str(versionNumber))

 

def consoleWriteLine(message):  
    import os, sys
    sys.stdout.write(str(message) + os.linesep)
import numpy as np
import cv2
import pickle
from platform import system
def Verify():
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")
    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}
    cap = cv2.VideoCapture(0)
    name=False
    for i in range(50): 
        ret, frame = cap.read()
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            id_, conf = recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                smile=smile_cascade.detectMultiScale(roi_gray,2,12)
                print(id_)
                for (sx,sy,sw,sh) in smile:
                    cv2.rectangle(roi_color,(sx,sy),(sx+sw,sy+sh),(0,0,0))
                    cv2.putText(frame,'smile',(x+sx,y+sy),font,1,(12,255,255),2,cv2.LINE_AA)
            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    if name:
        cap.release()
        cv2.destroyAllWindows()
        return True
    else:
        cap.release()
        cv2.destroyAllWindows()
        return False
    
def check():
    ans=Verify()
    if ans==True:
        TakeImages()
        lbl = tk.Label(window, text = "Done Hide/Unhide",width = 50, height = 2, fg ="green",bg = "white", font = ('times', 15, ' bold ') )
        lbl.place(x = 450, y = 480) 
    else:
        lbl = tk.Label(window, text = "Its Not YOu",width = 50, height = 2, fg ="green",bg = "white", font = ('times', 15, ' bold ') )
        lbl.place(x = 450, y = 480) 
def TakeImages():
    status=txt2.get()
    operatingSystem = system()
    if operatingSystem == "Windows" or operatingSystem == "Darwin":
        folderPath = txt.get()
        command = txt2.get()
        command=command.upper()
        from subprocess import call
        if command == "HIDE":
            if operatingSystem == "Windows":
                call(["attrib", "+H", folderPath])
            elif operatingSystem == "Darwin":
                call(["chflags", "hidden", folderPath])
        elif command == "UNHIDE":
            if operatingSystem == "Windows":
                call(["attrib", "-H", folderPath])
            elif operatingSystem == "Darwin":
                call(["chflags", "nohidden", folderPath])
        else:
            consoleWriteLine("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        consoleWriteLine("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

window = tk.Tk()  
window.title("Face_Recogniser") 
window.configure(background ='white') 
window.grid_rowconfigure(0, weight = 1) 
window.grid_columnconfigure(0, weight = 1) 
message = tk.Label( 
    window, text ="Hide by Face",  
    bg ="green", fg = "white", width = 50,  
    height = 3, font = ('times', 30, 'bold'))  
      
message.place(x = 200, y = 20) 
  
lbl = tk.Label(window, text = "Path of folder you want to hide or unhide",  
width = 50, height = 2, fg ="green",  
bg = "white", font = ('times', 15, ' bold ') )  
lbl.place(x = 180, y = 200) 
  
txt = tk.Entry(window,  
width = 20, bg ="white",  
fg ="green", font = ('times', 15, ' bold ')) 
txt.place(x = 700, y = 215) 
  
lbl2 = tk.Label(window, text ="Type hide or unhide",  
width = 20, fg ="green", bg ="white",  
height = 2, font =('times', 15, ' bold '))  
lbl2.place(x = 400, y = 300) 
  
txt2 = tk.Entry(window, width = 20,  
bg ="white", fg ="green",  
font = ('times', 15, ' bold ')  ) 
txt2.place(x = 700, y = 315)


takeImg = tk.Button(window, text ="Verify-is that You",  
command = check, fg ="white", bg ="green",  
width = 20, height = 3, activebackground = "Red",  
font =('times', 15, ' bold ')) 
takeImg.place(x = 650, y = 500) 
