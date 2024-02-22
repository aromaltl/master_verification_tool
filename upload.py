import cv2
import PySimpleGUI as sg
import json
import os
from opencv_draw_annotation import draw_bounding_box
from config import config


def converting_to_asset_format(data_json, total_frames):
    # try:
    #     print("converting_to_asset_format cpp started...")
    #     import convert 
    #     data = convert.convert_format(json.dumps(data_json),total_frames)
    #     data = json.loads(data)
    #     # print(data)
    #     print("converting_to_asset_format cpp ended!!")
    #     return data
    # except Exception as ex:
    #     print(f"Error in cpp convert convert:{ex}")

    data = {}
    print("converting_to_asset_format started...")
    for i in range(0, total_frames, 2):
        i = str(i)
        # print(i)
        if i not in data_json:
            continue

        for asset in data_json[i]:
            for index, v in enumerate(data_json[i][asset]):
                if asset not in data:
                    data[asset] = {}
                if int(v[0]) not in data[asset]:
                    data[asset][int(v[0])] = []
                data[asset][int(v[0])].append([i, v[1], v[2]])
    print("converting_to_asset_format ended!!")
    return data


def generate(cap, data, video_name):
    video_name = os.path.basename(video_name).replace('.MP4', '')
    print("genearting images !!")
    os.makedirs(f"Upload_Images/{video_name}", exist_ok=True)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    final_json = {"Assets": []}
    for asset in data:
        nth_last = config["det_loc"]["default"]
        print(asset)
        if 'Light' in asset:
            nth_last = config["det_loc"]['light_nth_last']
        if asset in config["det_loc"]:
            nth_last= config["det_loc"][asset]

        for ids in data[asset]:
            val = data[asset][ids][-min(nth_last, len(data[asset][ids]))]
            if (val[1][0] + val[2][0]) / 2 > width / 2:
                Asset = "RIGHT_" + asset
            else:
                Asset = "LEFT_" + asset
            # print(ids)
            final_json["Assets"].append([Asset, int(ids), int(val[0]), val[1], val[2], ['', '']])
            cap.set(1, int(val[0]))
            ret, frame = cap.read()
            draw_bounding_box(frame, (val[1][0], val[1][1], val[2][0], val[2][1]), labels=[asset], color='green')
            cv2.imwrite(f"Upload_Images/{video_name}/{video_name}_{str(val[0])}_{Asset}_{str(ids)}.jpeg", frame)
    print("images Done!!!")

    if os.path.exists(f"Upload_Images/{video_name}/{video_name}_final.json"):
        f1 = eval(open(f"Upload_Images/{video_name}/{video_name}_final.json", "r").read())
        for i, asset1 in enumerate(final_json["Assets"]):
            for asset2 in f1["Assets"]:
                # print(asset1,asset2)
                if asset1[:2] == asset2[:2]:
                    final_json["Assets"][i] = asset2
                    break

    final_json["Assets"].sort(key=lambda yy: int(yy[2]))
    f = open(f"Upload_Images/{video_name}/{video_name}_final.json", "w")
    f.write(json.dumps(final_json))
    f.close()
    print("finished")


def confirmation(CONFIRMATION):
    Input = sg.Text(font=("Arial", 20), justification='center')
    layout = [[sg.Button("Confirm", size=(12, 2), pad=(50, 40), font=("Arial", 20)),
               sg.Button("Cancel", size=(12, 2), pad=(50, 40), font=("Arial", 20))], [Input]]
    # layout=sg.Column(layout, scrollable=True,  vertical_scroll_only=True)
    win = sg.Window(CONFIRMATION, layout, finalize=True, enable_close_attempted_event=True,
                    element_justification='c')
    event = win.read()[0]
    Input.update(value=f"{CONFIRMATION}ing Please Wait !!!!")
    win["Confirm"].update(disabled=True)
    win["Cancel"].update(disabled=True)
    win.read(timeout=0.1)
    # import time
    # time.sleep(4)
    if event == "Confirm":

        return True, win
    else:
        return False, win

# print(upload_confirmation())
