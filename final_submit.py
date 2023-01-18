#!/usr/bin/env python
import PySimpleGUI as sg
import numpy as np
import pandas as pd
import os
import cv2
import ast
import json
import time
from opencv_draw_annotation import draw_bounding_box
from upload import converting_to_asset_format, generate, upload_confirmation

"""
LAYOUT DESIGN
"""


col11 = sg.Image( key='image')  # Coloumn 1 = Image view
Output = sg.Text()
Input = sg.Text()
Error = sg.Text()
Asset= sg.Text()
col12 = [[sg.Text('ENTER VIDEO PATH')],

         [sg.Text('Input video Path', size=(16, 1)), sg.InputText('', key='-IN-',size=(32, 1)), sg.FileBrowse()],
         [sg.Text('Verified json Path', size=(16, 1)), sg.InputText('', key='JSON',size=(32, 1)), sg.FileBrowse()],
         [sg.Button('Submit Video')],
         [sg.Button('START', size=(15, 1)), sg.Button('STOP', size=(15, 1))],
         [sg.Text('MODIFY MASTER')],

         [sg.Button('Replace Image', size=(15, 1))],
         [sg.Text('Current Asset: '), Asset],
         [sg.Text('Change Frames')],
         
         [sg.Button('Previous Frame', size=(15, 1)), sg.Button('Next Frame', size=(15, 1))],
         [sg.Text('Change Assets')],
         [sg.Button('Previous Asset', size=(15, 1)), sg.Button('Next Asset', size=(15, 1))],
         [sg.Button('EXIT', size=(15, 1)), sg.Text('Frame no: '), Input],
         [sg.Text(' '),Error]]

# Join two columns
# layout=col12
layout = [[ col11,sg.Frame(layout=col12, title='Details TO Enter')]]

def save_json(data, CSV):
    f=open(CSV,"w")
    f.write(str(data))
    f.close()





def load_json(CSV):
    f = open(CSV, "r")
    file = f.read()
    # print(file)
    data = eval(file)

    return data


if __name__ == "__main__":

    window = sg.Window('Data Verification Toolbox',
                       layout, resizable=True, finalize=True, return_keyboard_events=True, use_default_focus=False)
    window.finalize()
    stream = False
    index=0
    output_frame=0
    while True:
        event, values = window.read()
        # print(event, values)
        if event == 'EXIT' or event == sg.WIN_CLOSED:
            break
        try:
            if event == 'Submit Video':
                ip = values['-IN-']
                json = values['JSON']
                data = load_json(json)
                data["Assets"].sort(key=lambda val: val[2])
                total_assets=len(data["Assets"])
                current=data["Assets"][0]
                cap=cv2.VideoCapture(ip)
                stream=True
        except Exception as ex:
            Error.update(value=ex,text_color='red')
        if not stream:
            continue

        if event == "Next Asset":
            index=min(index+1,total_assets-1)
            current=data["Assets"][index]
            output_frame=current[2]
        if event == 'Previous Asset':
            index = max(0,index-1)
            current=data["Assets"][index]
            output_frame=current[2]
        if event == 'Previous Frame':
            output_frame=output_frame-2
        if event == "Next Frame":
            output_frame=output_frame+2

        

        cap.set(1,output_frame)

        ret,image=cap.read()
        if event == "Replace Image":
            cv2.namedWindow("select the area",cv2.WINDOW_NORMAL)
            r = cv2.selectROI("select the area", image)
            cv2.destroyWindow("select the area")
            data["Assets"][index]=[current[0], current[1], output_frame,[r[0], r[1]], [r[2] + r[0], r[3] + r[1]]]
            current=data["Assets"][index]
            # save_json(data, CSV)

        if current[2]==output_frame:
            draw_bounding_box(image, (current[3][0], current[3][1], current[4][0], current[4][1]), labels=[current[0]])
        Asset.update(value=current[0])
        Input.update(value=output_frame)
        image = cv2.resize(image, (1280, 720))
        imgbytes = cv2.imencode('.png', image)[1].tobytes()  # ditto
        window['image'].update(data=imgbytes)




