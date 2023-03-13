import cv2
import numpy as np
from opencv_draw_annotation import draw_bounding_box
import json
import glob
import os

assets_dic={}
videos=list(glob.glob("/run/user/1000/gvfs/afp-volume:host=Anton.local,user=ml_support,volume=MachineLearning/POC/Jubail Royal Commission/takeleap_jubail-royal-commission_2023-02-05_1225/Jubail Royal Commission/jub/*.MP4"))
videos.sort()
print(videos)
counter={}
cap=cv2.VideoCapture(videos[0])
dirname = os.path.basename(videos[0])

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
            # print()
            draw_bounding_box(im, (items[1][0],items[1][1],items[2][0],items[2][1]), labels=[str(assets_dic[ass][items[0]]), ass], color='green') 
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





