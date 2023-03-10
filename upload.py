import cv2
import PySimpleGUI as sg
import json
import os
from opencv_draw_annotation import draw_bounding_box


def converting_to_asset_format(data_json, total_frames):
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
        nth_last = 8
        print(asset)
        if 'Light' in asset:
            nth_last = 12

        for ids in data[asset]:
            val = data[asset][ids][-min(nth_last, len(data[asset][ids]))]
            if (val[1][0] + val[2][0]) / 2 > width / 2:
                Asset = "RIGHT_" + asset
            else:
                Asset = "LEFT_" + asset
            # print(ids)
            final_json["Assets"].append([Asset, int(ids), int(val[0]), val[1], val[2],['','']])
            cap.set(1, int(val[0]))
            ret, frame = cap.read()
            draw_bounding_box(frame, (val[1][0], val[1][1], val[2][0], val[2][1]), labels=[asset], color='green')
            cv2.imwrite(f"Upload_Images/{video_name}/{video_name}_{str(val[0])}_{Asset}_{str(ids)}.jpeg", frame)
    print("images Done!!!")
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
