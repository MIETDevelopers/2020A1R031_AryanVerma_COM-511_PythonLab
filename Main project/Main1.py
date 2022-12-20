from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from tkinter import filedialog,messagebox
import tkinter as tk
from datetime import datetime
from numpy import*
win = Tk()
win.geometry("821x621")
win.resizable(0,0)
win.title("My CAM")
bgimg=tk.PhotoImage(file="C:\\Users\\LENOVO\\Desktop\\Environement\\Venv\\CameraApp\\Background.png")
items = "Modes", "Web Cam", "Phone Cam","Browse Image"
label = Label(win,i=bgimg)
label.pack(fill='both',expand=True)
destPath=StringVar()
#win.cap=cv2.VideoCapture()
#creating a label to display the camera frame in the tkinter window and determining the size of the the camera frame
def imageFrame(img,label,x,y,w,h):
    #rezing the frame 
    img = cv2.resize(img, (w, h))
    #fliping the frame
    img =cv2.flip(img,1)
    #we have to convert the image from the array using numpy library
    image = Image.fromarray(img)
    
    pic = ImageTk.PhotoImage(image)
    label.configure(image=pic)
    label.image = pic
    label.place(x=x, y=y)

def choose():
    bt3=Button(win,text="Capture",bg="Green",fg="white",command=capture,font=("Times New Roman",20),padx=10,pady=10)
    bt3.place(x=350, y=530, width=125)  
    global cap,cap2,image
    if com3.get()=="Web Cam":
        cap =cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture()

    elif com3.get()=="Phone Cam":
        url="http://192.168.1.5:8080/video" 
        cap2 = cv2.VideoCapture(url)
        cap = cv2.VideoCapture()

    elif com3.get()=="Browse Image":
        path = filedialog.askopenfilename( title="Select file", filetypes=(('JPG','*.jpg'),('PNG', '*.png')))
        image = cv2.imread(path)
        cap = cv2.VideoCapture()
        cap2 = cv2.VideoCapture()
    show()
#function for browsing the files        
def destBrowse():
    destDirectory=filedialog.askdirectory(initialdir="V:\python Programs\python project")
    destPath.set(destDirectory)

#function for image browsing
def imageBrowse():
    opendirectory=filedialog.askopenfilename(initialdir="V:\python Programs\python project")
    imagePath.set(opendirectory)
    imageView=Image.open(opendirectory)
    imageResize=imageView.resize((821,621),Image.ANTIALIAS)
    imageDisplay=ImageTk.PhotoImage(imageResize)
    win.label.config(image=imageDisplay)
    win.label.photo=imageDisplay
    
#function for capturing the image
def capture():
    image_name=datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    if destPath.get() !='':
        image_Path=destPath.get()
    else:
        messagebox.showerror("Error","No Directory selected to store image!!")
             
    #imageSave=filedialog.askopenfile(initialdir="V:\python Programs\python project")
    #image_path=imageSave    
    imgName=image_Path+'/'+image_name+".jpg"
    if com3.get()=="Web Cam":
        _,frame=cap.read()
    else:
        _,frame=cap2.read()    
    #cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    success=cv2.imwrite(imgName,frame)
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED"+imgName)

# BUTTONS            
com3 = ttk.Combobox(win,values=items,font=("Times New Roman",25))
com3.current(0)
com3.place(x=35, y=10, width=210)
button3 =Button(win,text='Switch',command=choose,padx=10,pady=2.5,font=("Times New Roman",20))
button3.place(x=80,y=60, width=100)
browsebtn=Button(win,text="BROWSE",command=destBrowse)
browsebtn.place(x=10,y=580,width=100)
imgs = "Filters", "rgb", "gray"
switch = ttk.Combobox(win,values=imgs,font=("Times New Roman",20))
switch.place(x=675, y=10, width=100)
switch.current(0)
#show function for display the output and appling the filters
def show():
    if com3.get()=="Web Cam":
        _, frame = cap.read()
    if com3.get() == "Phone Cam":
        _, frame = cap2.read()
    if com3.get() == "Browse Image":
        frame = image
    
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    
    if switch.get()=="rgb":
        imageFrame(rgb,label,5,2,820,620)
    if switch.get()=="gray":
        imageFrame(gray,label,5,2,820,620)
    label.after(5,show)
imagePath=StringVar()
win.mainloop()