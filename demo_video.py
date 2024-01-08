import cv2
import numpy as np
from opencv_draw_annotation import draw_bounding_box
import json
import glob
import os

assets_dic={}
videos=list(glob.glob("/*.MP4"))
videos.sort()
print(videos)
counter={}
cap=cv2.VideoCapture(videos[0])
dirname = os.path.basename(videos[0])
COLORS =[
    '#700409',  # Dark Red
    '#007010',  # Dark Green
    '#100090',  # Dark Blue
    '#907000',  # Olive
    '#600060',  # Dark Purple
    '#0A4050',  # Teal
    '#B04000',  # Sienna
    '#80B040',  # Dark Salmon
    '#603330',  # Dark Brown
    '#54A050'   # Dim Gray
]
assets_color={}
w, h =  int(cap.get(3)), int(cap.get(4))
cap.release()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter("out.MP4", fourcc, 30, (w, h))

def addBBox(im, frameNo,data):
    if str(frameNo) not in data:
        data[str(frameNo)]={}
    for ass in data[str(frameNo)]:
        for items in data[str(frameNo)][ass]:
            if ass not in assets_dic:
                assets_dic[ass]={}
                if ass not in counter:
                    counter[ass]=1
            if items[0] not in assets_dic[ass]:
                assets_dic[ass][items[0]]=counter[ass]
                counter[ass]+=1
            if ass not in assets_color:
                assets_color[ass]=COLORS[len(assets_dic.keys())%len(COLORS)]  
            draw_bounding_box(im, (items[1][0],items[1][1],items[2][0],items[2][1]), labels=[str(assets_dic[ass][items[0]]), ass.replace("_"," ")], font_scale = 0.8,color=assets_color[ass]) 
    return im

for x in videos:
    cap=cv2.VideoCapture(x)
    f = open(x.replace(".MP4","_annotation.json"), "r")
    file = f.read()
    data = json.loads(file)
    frame_no=2
    while True:

        cap.read()
        ret,frame=cap.read()
        # print(frame.shape)
        # break
        if not ret or cv2.waitKey(1) & 0xff==27:
            break

        frame=addBBox(frame, frame_no, data)
        frame_no+=2
        cv2.imshow("out_",frame[::2,::2])
        writer.write(frame)
    assets_dic={}
writer.release()





