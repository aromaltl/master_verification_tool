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
from upload import converting_to_asset_format, generate, confirmation
from final_submit import final_verify

"""
LAYOUT DESIGN
"""

# assets_list = ['LEFT_Signboard_Caution_Board', 'RIGHT_Signboard_Caution_Board', 'LEFT_Signboard_Chevron_Board', 'RIGHT_Signboard_Chevron_Board', 'LEFT_Signboard_Gantry_Board', 'RIGHT_Signboard_Gantry_Board', 'LEFT_Signboard_Hazard_board', 'RIGHT_Signboard_Hazard_board', 'LEFT_Signboard_Information_Board', 'RIGHT_Signboard_Information_Board', 'LEFT_Signboard_Mandatory_Board', 'RIGHT_Signboard_Mandatory_Board', 'LEFT_VMS_Gantry', 'RIGHT_VMS_Gantry', 'LEFT_Delineator', 'RIGHT_Delineator', 'LEFT_ECB_(SOS)', 'RIGHT_ECB_(SOS)', 'LEFT_Encroachment', 'RIGHT_Encroachment', 'LEFT_Hectometer_stone', 'RIGHT_Hectometer_stone', 'LEFT_Kilometer_Stone', 'RIGHT_Kilometer_Stone', 'LEFT_Solar_blinker', 'RIGHT_Solar_blinker', 'LEFT_Double_Arm_Street_Light', 'RIGHT_Double_Arm_Street_Light', 'LEFT_Pot_Holes', 'RIGHT_Pot_Holes', 'LEFT_Street_Light_Slanding', 'RIGHT_Street_Light_Slanding', 'LEFT_Single_Arm_Light_Slanting', 'RIGHT_Single_Arm_Light_Slanting', 'LEFT_High_Mast_Light', 'RIGHT_High_Mast_Light', 'Chainage']
global CSV

CSV = None
PLAY = True
column = ''

col11 = sg.Image(filename='bg2.png', key='image')  # Coloumn 1 = Image view
Output = sg.Text()
Input = sg.Text()
Error = sg.Text()
col12 = [[sg.Text('ENTER VIDEO PATH')],
         # [sg.Slider(range=(0, 1000), default_value=0, size=(50, 10), orientation="h",enable_events=True, key="slider")],
         [sg.Text('Input video Path', size=(18, 1)), sg.InputText('', key='-IN-', size=(38, 1)), sg.FileBrowse()],
         [sg.Text('Normalized CSV File ', size=(18, 1)), sg.InputText('', key='CSV', size=(38, 1)), sg.FileBrowse()],
         [sg.Button('Submit Videos')],
         [sg.Text('VIDEO PLAY')],
         [sg.Button('PLAY', size=(18, 1))],
         [sg.Text('ENTER FRAME NUMBER TO JUMP IN')],
         [sg.Text('Take Me To:', size=(18, 1)), sg.InputText('', key='skip', size=(38, 1))],
         [sg.Button('Go', size=(18, 1))],
         [sg.Text('MODIFY MASTER')],
         # [sg.Button('Add Data', size=(15, 1)), sg.InputCombo([], size=(40,4), key='Coloumn'), sg.Button('Select1')],
         [sg.Button('Add Data', size=(15, 1))],
         [sg.Button('Delete Data', size=(15, 1)), sg.InputCombo([], size=(40, 4), key='Delete_drop'),
          sg.Button('Select')],
         [sg.Text('NAVIGATE')],
         [sg.Button('START', size=(15, 1)), sg.Button('STOP', size=(15, 1))],

         [sg.Button('PREVIOUS', size=(15, 1)), sg.Button('NEXT', size=(15, 1))],
         [sg.Text('Click to generate final json and images : ', size=(35, 1)), sg.Button('Generate')],
         [sg.Button('SAVE FRAME', size=(15, 1)), sg.Button('EXIT', size=(15, 1)), sg.Text('', key='text'), Output,
          sg.Text('Frame no: '), Input]]


# Join two columns
def asset_select_window(keys, cols):
    layout = []
    # print(keys)
    d = len(keys)
    r = d % cols
    keys = keys + [""] * (cols - r)
    n = len(keys) // cols
    for hh in range(n):
        layout.append([sg.Button(keys[x + hh * cols], size=(24, 1), pad=(0, 0)) for x in range(cols)])

    layout.append([sg.InputText('', key='New_Asset', size=(58, 1)), sg.Button('ADD_NEW_ASSET', size=(18, 1))])  # ,
    win = sg.Window("Select Asset", layout, resizable=True, finalize=True, enable_close_attempted_event=True,
                    element_justification='c')
    win.hide()
    return win


def save_json(data, CSV):
    with open(CSV, "w") as outfile:
        json.dump(data, outfile)


#
tab1 = [[col11, sg.Frame(layout=col12, title='Details TO Enter')],
        [sg.Slider(range=(0, 1000), default_value=0, size=(200, 5), tick_interval=500, orientation="h",
                   enable_events=True, key="slider")]]


def load_json(CSV):
    f = open(CSV, "r")
    file = f.read()
    data = json.loads(file)
    return data


def addBBox(im, frameNo, data):
    if str(frameNo) not in data:
        data[str(frameNo)] = {}
    for ass in data[str(frameNo)]:
        for items in data[str(frameNo)][ass]:
            draw_bounding_box(im, (items[1][0], items[1][1], items[2][0], items[2][1]), labels=[items[0], ass],
                              color='green')
    return im


def drop_down_list(frame, data):
    if str(frame) not in data:
        data[str(frame)] = {}

    i = []
    a = data[str(frame)]
    for x in a.keys():
        for c in a[x]:
            i.append([c[0], x])
    return i


def addtoJSON(frameNo, asset, bbox, data, id_):
    c = str(id_)
    try:
        data[str(frameNo)][asset].append([c, bbox[0], bbox[1]])

    except:
        data[str(frameNo)][asset] = [[c, bbox[0], bbox[1]]]


def verify():
    # Select Color Theme
    try:
        os.mkdir("SavedImages")
    except:
        pass
    df = pd.read_csv("https://tlviz.s3.ap-south-1.amazonaws.com/SeekRight/MASTER_VERIFICATION_FILES/assets_sheet.csv")
    # df
    sg.theme('DarkGrey5')
    layout = [[sg.TabGroup([[sg.Tab('Data Verification', tab1, tooltip='tip')]])]]
    # Frame windows
    window = sg.Window('Data Verification Toolbox',
                       layout, resizable=True, finalize=True, return_keyboard_events=True, use_default_focus=False)

    window.finalize()
    stream = False
    output_frame = 0
    Shift = False

    ip = ''
    PREV_SELECTED_ASSET = ''
    delete_val=''

    while True:
        letter = None
        event, values = window.read()

        print((event, values))
        # print()
        if event == 'slider':
            output_frame = int(int(values['slider']) // 2) * 2
            window['Delete_drop'].Update(values=drop_down_list(output_frame, data))

        text_elem = window['text']

        if len(event) == 1:
            print(ord(event))

            if ord(event) == 97 or ord(event) == 100 or ord(event) == 115:
                # print(ord(event))
                letter = ord(event)

        # if event is not None:
        # text_el em.update(event)

        if event == 'EXIT' or event == sg.WIN_CLOSED:
            return
        if event == 'Go':
            if int(values['skip']) % 2 == 0:
                output_frame = int(values['skip'])
                if str(output_frame) not in data:
                    data[str(output_frame)] = {}

        if event == 'Submit Videos':
            ip = values['-IN-']
            CSV = values['CSV']
            data = load_json(CSV)

        if event == 'START':
            if len(ip) > 0 and len(CSV) > 0:
                print('START')
                cap = cv2.VideoCapture(str(ip))
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                window["slider"].update(range=(0, total_frames-1))

                if str(output_frame) not in data:
                    data[str(output_frame)] = {}
                assets = []
                for x in data:
                    try:
                        x = int(x)
                    except:
                        assets.append(x)
                assets.sort(key=lambda strings: len(strings), reverse=True)
                asset_window = asset_select_window(assets, 6)
                window['Delete_drop'].Update(values=drop_down_list(output_frame, data))

                stream = True

        if event == 'STOP':
            stream = False
            output_frame = 0

            ip = ''
            img = cv2.imread('bg2.png')
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        if stream:

            if event == 'Add Data' or 'q:' in event:
                if event == 'Add Data':
                    asset_window.UnHide()
                    while True:
                        column, val = asset_window.read()
                        print("###", column, val)
                        if column == "ADD_NEW_ASSET":
                            data[val["New_Asset"]] = 0
                            asset_window.close()
                            assets.append(val["New_Asset"])
                            assets.sort(key=lambda strings: len(strings), reverse=True)
                            asset_window = asset_select_window(assets, 6)
                            asset_window.UnHide()

                        else:
                            if column != "-WINDOW CLOSE ATTEMPTED-":
                                PREV_SELECTED_ASSET = column
                            break
                    asset_window.hide()
                    if column == "-WINDOW CLOSE ATTEMPTED-":
                        continue
                if len(PREV_SELECTED_ASSET) == 0:
                    continue
                cap.set(cv2.CAP_PROP_POS_FRAMES, output_frame)
                cv2.namedWindow("select the area", cv2.WINDOW_NORMAL)
                ret, frame = cap.read()
                r = cv2.selectROI("select the area", frame)
                cv2.destroyWindow("select the area")
                if sum(r) == 0:
                    continue
                if type(delete_val) is str and len(delete_val):
                    addtoJSON(output_frame, PREV_SELECTED_ASSET, [(r[0], r[1]), (r[2] + r[0], r[3] + r[1])], data,
                              delete_val)
                else:
                    data[PREV_SELECTED_ASSET] += 1
                    addtoJSON(output_frame, PREV_SELECTED_ASSET, [(r[0], r[1]), (r[2] + r[0], r[3] + r[1])], data,
                              data[PREV_SELECTED_ASSET])
                frame = addBBox(frame, output_frame, data)
                save_json(data, CSV)

            if event == 'SAVE FRAME' or letter == 83:
                ret = cap.set(cv2.CAP_PROP_POS_FRAMES, output_frame)
                ret, frame = cap.read()
                frame = addBBox(frame, output_frame, data)
                cv2.imwrite("SavedImages/" + os.path.basename(ip) + '_' + str(output_frame) + '.jpeg', frame)

            if event == 'Select' or "Return" in event or event == "\r":
                delete_val = values['Delete_drop']

            if event == 'NEXT' or 'd:' in event:  # event == 'Right:114' or event == "Right:39":
                if Shift:
                    output_frame = int(output_frame) + 14
                    cap.set(1, output_frame)
                else:
                    output_frame = int(output_frame) + 2
                    cap.read()

                if str(output_frame) not in data:
                    data[str(output_frame)] = {}
                delete_val=''
                window['Delete_drop'].Update(values=drop_down_list(output_frame, data))

            if event == 'PREVIOUS' or 'a:' in event:

                output_frame = max(0, int(output_frame) - 14) if Shift else max(0, int(output_frame) - 2)
                if str(output_frame) not in data:
                    data[str(output_frame)] = {}
                delete_val = ''
                window['Delete_drop'].Update(values=drop_down_list(output_frame, data))
            if "Shift" in event:
                Shift = not Shift

            if event == "Generate":
                CONFIRM, wait = confirmation("Generate")
                if CONFIRM:
                    asset_format = converting_to_asset_format(data, total_frames)
                    generate(cap, asset_format, ip)
                    window.close()
                    wait.close()
                    return ip
                wait.close()

            # if (event == "Delete Data" or event == "Delete:119" or event == "\x7f" ) and len(delete_val):
            if ("delete" in event.lower() or event == "\x7f") and len(delete_val):
                found = 25
                for x in range(output_frame, total_frames - 1):
                    if x % 2 == 1:
                        continue
                    x = str(x)
                    if x not in data:
                        data[x] = {}

                    if delete_val[1] in data[x].keys():

                        for yy in range(len(data[x][delete_val[1]])):
                            if delete_val[0] == data[x][delete_val[1]][yy][0]:
                                data[x][delete_val[1]].pop(yy)
                                found = 25
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
                            if delete_val[0] == data[x][delete_val[1]][yy][0]:
                                data[x][delete_val[1]].pop(yy)
                                found = 25
                                break
                    found -= 1
                    if found == 0:
                        break
                save_json(data, CSV)
                delete_val = ""

            if event == 'PLAY' or 'space:' in event:
                ret = True
                PAUSE = True
                asset_seen = set()
                cv2.namedWindow("OUT", cv2.WINDOW_NORMAL)
                while True:
                    new_asset = False
                    if not PAUSE:
                        output_frame += 2
                        ret, frame = cap.read()
                        ret, frame = cap.read()
                        if not ret:
                            break
                        if str(output_frame) not in data:
                            data[str(output_frame)] = {}

                        frame = addBBox(frame, output_frame, data)

                        for ass in data[str(output_frame)]:
                            for items in data[str(output_frame)][ass]:
                                if str(items[0]) + ass not in asset_seen:
                                    asset_seen.add(str(items[0]) + ass)
                                    new_asset = True
                                    draw_bounding_box(frame, (items[1][0], items[1][1], items[2][0], items[2][1]),
                                                      labels=[items[0], ass],
                                                      color='purple', border_thickness=3, )

                        frame = cv2.resize(frame, (1280, 720))
                    cv2.imshow("OUT", frame)
                    time.sleep(.008)

                    key_press = cv2.waitKey(1)

                    if key_press & 0xff == ord(' ') or new_asset:
                        PAUSE = not PAUSE

                    if not ret or key_press & 0xff == 27:
                        break
                window['Delete_drop'].Update(values=drop_down_list(output_frame, data))
                cv2.destroyWindow("OUT")
            # output_frame = int(output_frame // 2) * 2
            if output_frame > total_frames - 1:
                cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)
                output_frame = total_frames - 1
                output_frame = int(output_frame // 2) * 2
                window['Delete_drop'].Update(values=drop_down_list(output_frame, data))

            if event != 'NEXT' and 'd:' not in event:
                ret = cap.set(cv2.CAP_PROP_POS_FRAMES, output_frame)
            ret, frame = cap.read()


            window["slider"].update(value=output_frame)
            Input.update(value=output_frame)
            frame = addBBox(frame, output_frame, data)

            frame = cv2.resize(frame, (1280, 720))
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)


if __name__ == "__main__":
    ip = verify()
    if ip is not None:
        v_name = os.path.basename(ip).replace(".MP4", "")
        final_json = f"Upload_Images/{v_name}/{v_name}_final.json"
        final_verify(ip, final_json)
