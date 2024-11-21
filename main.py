from tkinter import *
from PIL import ImageTk, Image
import requests
import math
from tkinter import ttk
from ultralytics import YOLO
import cv2
import cvzone
import numpy as np
import shutil
import os

def left_button_click(arr1,arr2):
    label_tree_count['text']=""
    for i in range(0,3,+1):
            for j in range(0,3,+1):
                arr1[i][j]=arr1[i][j]-1
    ParseImage(arr1,arr2)
    PrintImage()

def right_button_click(arr1,arr2):
    label_tree_count['text']=""
    for i in range(0,3,+1):
            for j in range(0,3,+1):
                arr1[i][j]=arr1[i][j]+1
    ParseImage(arr1,arr2)
    PrintImage()

def top_button_click(arr1,arr2):
    label_tree_count['text']=""
    for i in range(0,3,+1):
         arr2[i]=arr2[i]-1
    ParseImage(arr1,arr2)
    PrintImage()

def bottom_button_click(arr1,arr2):
    label_tree_count['text']=""
    for i in range(0,3,+1):
         arr2[i]=arr2[i]+1
    ParseImage(arr1,arr2)
    PrintImage()

def PrintImage():
    for label in labels:
        label.destroy()
    labels.clear()
    for row in range(3):
        for col in range(3):
            image_index = (row * 3) + col
            if image_index < len(image_files):
                image_path = image_files[image_index]
                image = Image.open(image_path)
                image = ImageTk.PhotoImage(image)
                label = ttk.Label(row_frames[row], image=image)
                label.image = image
                label.pack(side="left")
                labels.append(label)

def ParseImage(arr1, arr2):
    num=1
    for i in range(0,3,+1):
        y=arr2[i]
        for j in range(0,3,+1):
            x=arr1[i][j]
            z = 19
            url1= "https://tile.googleapis.com/v1/2dtiles/"+str(z)+"/"+str(x)+"/"+str(y)+"?session="+session_data_info+"&key=AIzaSyBsns8WDhLDdo-SyRaFSEeOTirv-sbMIfc"
            response1=requests.get(url1)
            output_file=f'parsed_images/{num}.png'
            num=num+1
            if response1.status_code == 200:
                with open(output_file, "wb") as file:
                    file.write(response1.content)

def PredictImages():
    predict_path="C:\\Trees_project\\annotated_images\\predict"
    if os.path.isdir(predict_path):
        shutil.rmtree(predict_path)
    model = YOLO("runs\\detect\\train3\\weights\\best.pt")
    results = model.predict(image_files,save=True, project="annotated_images",conf=0.6)
    count=0
    for result in results:
        for ss in result:
            count+=1
    # label_tree_count['text']=f"Количетсво деревьев: {count}"
    predicted_image_files = [
        "annotated_images/predict/1.png",
        "annotated_images/predict/2.png",
        "annotated_images/predict/3.png",
        "annotated_images/predict/4.png",
        "annotated_images/predict/5.png",
        "annotated_images/predict/6.png",
        "annotated_images/predict/7.png",
        "annotated_images/predict/8.png",
        "annotated_images/predict/9.png",
    ]
    for label in labels:
        label.destroy()
    labels.clear()
    for row in range(3):
        for col in range(3):
            image_index = (row * 3) + col
            if image_index < len(predicted_image_files):
                image_path = predicted_image_files[image_index]
                image = Image.open(image_path)
                image = ImageTk.PhotoImage(image)
                label = ttk.Label(row_frames[row], image=image)
                label.image = image
                label.pack(side="left")
                labels.append(label)

image_files = [
    "parsed_images/1.png",
    "parsed_images/2.png",
    "parsed_images/3.png",
    "parsed_images/4.png",
    "parsed_images/5.png",
    "parsed_images/6.png",
    "parsed_images/7.png",
    "parsed_images/8.png",
    "parsed_images/9.png",
]
row_frames = []
labels = []
root = Tk()
frame = ttk.Frame(root)
frame.pack(fill="both")
click_count = 0
w, h = 3, 3
arr1 = [[0 for x in range(w)] for y in range(h)]
arr2 = [0 for x in range(w)]
left_arr1=[[0 for x in range(w)] for y in range(h)]
left_arr2 = [0 for x in range(w)]
#startX,startY=183078,87579
lat, lng = 51.102960, 71.436242
z = 19
n = 2 ** z
startX = int((lng + 180.0) / 360.0 * n)
lat_rad = math.radians(lat)
startY = int((1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
url = "https://tile.googleapis.com/v1/createSession?key=AIzaSyBsns8WDhLDdo-SyRaFSEeOTirv-sbMIfc"
data = {
    "mapType": "satellite",
    "language": "en-US",
    "region": "US"
}
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    session_data = response.json()
    session_data_info=session_data.get('session')
for i in range(-1,2,+1):
        arr2[i+1]=startY+i
        for j in range(-1,2,+1):
            arr1[i+1][j+1]=startX+j
ParseImage(arr1,arr2)
label_tree_count = ttk.Label(text="")
label_tree_count.pack(side="top")
right_button = ttk.Button(frame, text="Right", command=lambda: right_button_click(arr1,arr2))
right_button.pack(side="right")
left_button = ttk.Button(frame, text="Left", command=lambda: left_button_click(arr1,arr2))
left_button.pack(side="left")
top_button = ttk.Button(frame, text="Top", command=lambda: top_button_click(arr1,arr2))
top_button.pack(side="top")
bottom_button = ttk.Button(frame, text="Bottom", command=lambda: bottom_button_click(arr1,arr2))
bottom_button.pack(side="bottom")
predict_button = ttk.Button(frame, text="Predict", command=lambda: PredictImages())
predict_button.pack(side="top")
for row in range(3):
    row_frame = ttk.Frame(root)
    row_frame.pack(side="top")
    row_frames.append(row_frame)
    for col in range(3):
        image_index = (row * 3) + col
        if image_index < len(image_files):
            image_path = image_files[image_index]
            image = Image.open(image_path)
            image = ImageTk.PhotoImage(image)
            label = ttk.Label(row_frame, image=image)
            label.image = image
            label.pack(side="left")
            labels.append(label)
root.mainloop()