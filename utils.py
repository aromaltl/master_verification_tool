import cv2
import numpy as np
import yaml
import os

import json




def extract_for_annotations(cap,frame,vname):
    # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    data={"Frames":set()}
    if os.path.exists(f"DeletedImages/{vname}_deleted.json"):
        with open(f"DeletedImages/{vname}_deleted.json",'r') as f:
            data = json.load(f)
        data["Frames"]=set(data["Frames"])

    for x in range(max(0,frame-6*3),frame+6*3,6):
        # cap.set(1,x)
        # ret,fra = cap.read()
        # if not ret:
        #     break 
        # cv2.imwrite(f"DeletedImages/{vname}_{x}.jpeg",fra)
        data["Frames"].add(x)
    data["Frames"] = list( data["Frames"])
    with open(f"DeletedImages/{vname}_deleted.json", 'w') as f:
        json.dump(data, f)





class mouse_call:
    def __init__(self) :
        self.ast = None
        self.input =None
        self.changed=False
        # self.cap=cap
        # self.vname = vname

    def highlight(self,img):
        if self.ast is not None:
            items,_=self.ast
            img[int(items[1][1]): int(items[2][1]),int(items[1][0]): int(items[2][0]),2]=255
        return img

    def mclbk(self,event, x, y, flags,param):
        if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
            self.input=event,x,y
            self.changed = True


    def update(self,data,framno,total_frames,cap,vname):
        if self.input is None:
            return
        event,x,y= self.input
        self.input=None
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.ast is None:
                for xx in data[str(framno)]:
                    for id, yy in enumerate(data[str(framno)][xx]):
                        # print(x,y,yy)
                        if  int(yy[1][0]) <= x <= int(yy[2][0]) and int(yy[1][1]) <= y <= int(yy[2][1]):
                            self.ast = yy,xx
                            self.changed =True
                            break
            else:
                self.ast=None



        output_frame=framno

        if (event == cv2.EVENT_MBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN) and self.ast is not None:
            delete_val = self.ast
            found = 25
            extract_for_annotations(cap,output_frame,vname)
            if event == cv2.EVENT_RBUTTONDOWN:
                RANGE=range(output_frame+1, total_frames)
            else:
                RANGE=range(output_frame, total_frames)
            
            for x in RANGE:
                if x % 2 == 1:
                    continue
                x = str(x)
                if x not in data:
                    data[x] = {}

                if delete_val[1] in data[x].keys():

                    for yy in range(len(data[x][delete_val[1]])):

                        if delete_val[0][0] == data[x][delete_val[1]][yy][0]:
                            data[x][delete_val[1]].pop(yy)
                            found = 25
                            self.changed=True
                            break
                found -= 1
                if found == 0:
                    break
            found = 25
            for x in range(output_frame - 1, -1, -1):
                if x % 2 == 1:
                    continue
                x = str(x)
                if x not in data:
                    data[x] = {}
                if delete_val[1] in data[x].keys():

                    for yy in range(len(data[x][delete_val[1]])):
                        if delete_val[0][0] == data[x][delete_val[1]][yy][0]:
                            data[x][delete_val[1]].pop(yy)
                            found = 25
                            self.changed = True
                            break
                found -= 1
                if found == 0:
                    break
            self.ast=None












