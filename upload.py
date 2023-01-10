
import cv2
from opencv_draw_annotation import draw_bounding_box
import json
def converting_to_asset_format(data_json,total_frames):
    data = {}
    for i in range(0,total_frames,2):
        i=str(i)
        if i not in data_json:
            continue

        for asset in data_json[i]:
            for index, v in enumerate(data_json[i][asset]):
                if asset not in data:
                    data[asset] = {}
                if int(v[0]) not in data[asset]:
                    data[asset][int(v[0])] = []
                data[asset][int(v[0])].append([i, v[1],v[2]])
    return data


def generate(cap,data,video_name):
    try:
        os.mkdir("Upload_Images")
    except:
        pass
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    final_json={"Assets":[]}
    for asset in data:
        nth_last=8
        if 'Light' in asset:
            nth_last=12

        for ids in data[asset]:
            val=data[asset][ids][-min(nth_last,len(data[asset][ids]))]
            if (val[1][0]+val[2][0])/2 > width/2:
                Asset="RIGHT_"+asset
            else:
                Asset="LEFT_"+asset
            final_json["Assets"].append([Asset,int(ids),int(val[0]),val[1],val[2]])
            cap.set(1,int(val[0]))
            ret,frame=cap.read()
            cv2.imwrite(f"Upload_Images/{video_name.replace('.MP4','')}_{str(val[0])}_{Asset}_{str(ids)}.jpeg")
    with open(f"{video_name.replace('.MP4','')}_final.json") as f:
        f.write(json.dumps(final_json))













    # try:
    #     os.mkdir("Upload_files")
    # except:
    #     pass

    # normalised={"Position":[],"Start_Frame":[],"End_Frame":[],"Speed":[]}
    # pos=set()
    # for x in range(len(position_df)):
    #     if position_df["Position"][x]=="N0.00000E0.00000":
    #         continue
    #     if position_df["Position"][x] not in pos:
    #         pos.add(position_df["Position"][x])
    #         normalised["Position"].append(position_df["Position"][x])
    #         normalised["Speed"].append(position_df["Speed"][x])
    #         normalised["Start_Frame"].append(position_df["Frame"][x])
    #         normalised["End_Frame"].append(position_df["Frame"][x])
    #         if len(normalised["End_Frame"])>2:
    #             normalised["End_Frame"][-1]=position_df["Frame"][x-1]
    # normalised["End_Frame"][-1]=position_df["Frame"][-1]
    # normalised=pd.DataFrame(normalised)
    # for asset in data:
    #     normalised["LEFT_"+asset]=pd.Series([[] for x in range(len(normalised))])
    #     normalised["RIGHT_"+asset]=pd.Series([[] for x in range(len(normalised))])
    # normalised=normalised.set_index("Position")
    # for asset in data:
    #     nth_last=8
    #     if 
    #     if 'Light' in asset:
    #         nth_last=12

    #     for ids in data[asset]:
    #         val=data[asset][ids][-min(nth_last,len(data[asset][ids]))]
    #         cap.set(1,int(val))
    #         ret,img=cap.read()
    #         if (val[1][0]+val[2][0])/2 >

    #         cv2.imwrite(video_name+"/"+)

            







# def converting_to_img_normalisedsheet_json(json_file,csv_file,video_file):



#         v = re.split("/|.csv",csv_file)

#         vname = v[-2]


#         data = pd.read_csv(csv_file)

#         l = len(data)

#         Position = []

#         start_frame = []

#         end_frame = []

#         speed = []

#         Pos = []

#         # data['Position'] contains Position values,datatype-str

#         for index, i in enumerate(data['Position']):

#             # Pos contains position values,datatype-str

#             Pos.append(i)

#         #s conatins unique positions,datatype-str

#         s = set(Pos)

#         s = list(s)

#         s.sort()

#         # for i in s:

#         #     print(i)

#         #for getting all the first Positions

#         grouped_df = data.groupby("Position").first()

# ​

#         # Reset indices to match format

#         #first_values contains dataframe with all the start frame

#         first_values = grouped_df.reset_index()

# ​

#         # print(first_values)

#         # for getting all the last positions

#         grouped_df = data.groupby("Position").last()

# ​

#         # Reset indices to match format

#         # last_values contains dataframe with all the end-frame

#         last_values = grouped_df.reset_index()

# ​

#         # print(type(last_values))

#         #Position contains all the positions,start_frame contains all the start_frames,speed contains all the speed,datatype-list of str values

#         for index, item in enumerate(first_values['Position']):

#             Position.append(item)

#             start_frame.append(first_values['Frame'][index])

#             speed.append(first_values['Speed'][index])

#         p = len(Position)

#         for i in range(p):

#             end_frame.append(0)

#         # print(len(end_frame))

#         for index, item in enumerate(last_values['Position']):

#             for index_list, i in enumerate(Position):

#                 if item == i:

#                     #end_frame contains all the end_frames,datatype-list of str values

#                     end_frame[index_list] = last_values['Frame'][index]

#         # Position.sort()

#         # start_frame.sort()

#         # end_frame.sort()

#         #d is a dictionary which contains position,start_frame,end_frame,speed

#         d = {"Position": Position, "Start_frame": start_frame, "End_frame": end_frame, "Speed": speed}

#         #new_data is dataframe of d

#         new_data = pd.DataFrame(d)

#         # sorting the dataframe by start_frame,new_data contains sorted dataframe

#         new_data = new_data.sort_values(by=['Start_frame'])

#         #ndata is dataframe which contains sorted dataframe

#         ndata = new_data


#         c = {}

#         # data_json contains json_file {asset:id:[frame,position]} format

#         data_json = converting_to_asset_format(json_file)

#         # print("aaaaaaaaa",data_json)

#         # print(len(data_json))

#         d = {}

#         d1 = {}

#         #i is asset_name

#         for i in data_json:

#             d[i] = {}

#             d1[i] = {}

#             # print(d1)

#         #i is asset_names

#         for i in data_json:

#             # print(data_json)

#             # print("a", data_json[i])

#             # k is id and value contains frame,position,datatype-str

#             for k, v in enumerate(data_json[i]):

#                 # print("b", v)

#                 d[i][v] = []

#                 d1[i][v] = []

#                 # print(data_json[i][v])

#                 # # print(len(data_json[i][v]))

#                 # print((data_json[i][v]))

# ​

#                 for j in range(len(data_json[i][v])):

#                     # print("c",j)

#                     # print(data_json[i][v][j])

#                     # print("d", data_json[i][v][j][0])

#                     if j < len(data_json[i][v]):

#                         d[i][v].append(data_json[i][v][j])

#         # print("aaaaaaaaaaaaaaaaaa")

#         # print(d)

#         # print(d1)

#         #d is dictionary which contains asset,id,frame,position

#         #i is asset

#         for i in d:

#             print(i)

#             #if i is street_light_slanding then if length of frames are greater than 14 then we are taking every 15 frame else we are taking 1 frame

#             if i == "Street_Light_Slanding":

#                 for j in d[i]:

#                     # print("@@@@@@@@@@")

#                     # print(len(d[i][j]))

#                     if len(d[i][j]) > 14:

#                         # print(d[i][j][-3])

#                         d1[i][j].append(d[i][j][-15])

#                     elif (len(d[i][j]) <= 14):

#                         # print("3 or less than 3")

#                         # print(d[i][j][0])

#                         d1[i][j].append(d[i][j][0])

#             # else if length of frames is greater than 11 then we are taking 12 frame else we are taking 1 frame

#             else:

#                 for j in d[i]:

#                     if len(d[i][j]) > 11:

#                         # print(d[i][j][-3])

#                         d1[i][j].append(d[i][j][-12])

#                     elif (len(d[i][j]) <= 11):

#                         # print("3 or less than 3")

#                         # print(d[i][j][0])

#                         d1[i][j].append(d[i][j][0])

#         print("d1", d1)

#         #d1 contains all the 15frame or 12 frame or 1 frame of assets,datatype-dictionary

#         with open(f"{vname}.json", "w") as outfile:

#             json.dump(d1, outfile)

#         #sorting d1  by frame number,datatype-dictionary

#         for i in d1:

#             for j in d1[i]:

#                 print(d1[i][j])

#                 for k in range(len(d1[i][j])):

#                     print(d1[i][j][k][0])

#                     d1[i][j].sort(key=lambda x: int(x[0]))

#         d2 = {}

#         for i in d1:

#             d2[i] = []

#             for j in d1[i]:

#                 if d2[i] == []:

#                     print(d1[i][j][0])

#                     d2[i] = [d1[i][j][0]]

#                 else:

#                     print(d1[i][j][0])

#                     d2[i].append(d1[i][j][0])

#         # print(d2)

#         # sorting d1  by frame number,datatype-dictionary

#         for i in d2:

#             # print(i)

#             for j in d2[i]:

#                 print(j[0])

#             d2[i].sort(key=lambda x: int(x[0]))

#         # print(d2)

#         # print(len(d2))

#         d3 = {}

#         # adding all the assets present in d2 to d3,datatype-dictionary

#         for i in d2:

#             d3[i] = []

#             for k in d2[i]:

#                 if d3[i] == []:

#                     d3[i] = [k]

#                 else:

#                     d3[i].append(k)

#         print(d3)

#         # fetching left,top,height and width,frame for drawing a bounding box

#         for i in d3:

#             # print("qqqqqq",i)

#             for j in d3[i]:

#                 # print(len(j))

#                 # print(j)

#                 # print(j[1])

#                 # print(j[2])

#                 # print("aaaa", j[0])

#                 f = int(j[0])

#                 # print(f)

#                 # print("###########@@@@@@@@@@2")

#                 # print(j)

#                 left = abs(int(j[1][0]))

#                 print("lll", left)

#                 top = abs(int(j[1][1]))

#                 width = abs(int(j[2][0]))

#                 print("width", width)

#                 height = abs(int(j[2][1]))

#                 #c contains assets

#                 #creating count to store the number of times assets come in a video

#                 if i not in c.keys():

#                     c[i] = 1

#                 else:

#                     c[i] = c[i] + 1

#                 #label1 contains frame_no,used for labeling while creating image

#                 label1 = i

#                 #label2 contains count of the asset ocurred, used for labeling while creating image

#                 label2 = c[i]

#                 # print(type(label1))

#                 #image0utputPath is the output image path,output

#                 image0utputPath = vname + "_" + i + "_" + str(j[0]) + "_" + str(c[i]) + '.jpeg'

#                 print(image0utputPath)

#                 #imgpath is the output image path

#                 imgpath = vname + "_" + i + "_" + str(j[0]) + "_" + str(c[i]) + '.jpeg'

#                 # checking the asset comes on left or right,if >960 is right

#                 if (left + width) / 2 > 960:

#                     print("Right")

#                     # start_f,end_f and position are start_frame,end_frame,position from ndata,datatype-str

#                     for index in range(len(ndata["Start_frame"])):

#                         start_f, end_f, position = ndata["Start_frame"][index], ndata["End_frame"][index], \

#                         ndata["Position"][index]

#                         #a is for checking f(frame) is between start_f and end_f

#                         a = int(f) in range(int(start_f), int(end_f))

#                         # print(a)

#                         # print(start_f, end_f, f, i)

#                         #adding output image path and position ndata dataframe

#                         if int(start_f) <= int(f) <= int(end_f):

#                             # print("########")

#                             a1 = f"RIGHT_{i}"

#                             if ndata.columns.isin([a1]).any():

#                                 # print("aaa")

#                                 # print(type(ndata[a1][index]))

#                                 n = (imgpath, position)

#                                 ndata[a1][index].append(n)

#                             else:

#                                 ndata[a1] = pd.Series([[] for i in range(len(ndata["Position"]))])

#                                 n = (imgpath, position)

#                                 ndata[a1][index].append(n)

# ​

#                 # asset is in the left

#                 else:

#                     print("Left")

#                     for index in range(len(ndata["Start_frame"])):

#                         start_f, end_f, position = ndata["Start_frame"][index], ndata["End_frame"][index], \

#                         ndata["Position"][index]

#                         a = int(f) in range(int(start_f), int(end_f))

#                         print(a)

#                         if int(start_f) <= int(f) <= int(end_f):

#                             print("########")

#                             a1 = f"LEFT_{i}"

#                             if ndata.columns.isin([a1]).any():

#                                 print("aaa")

#                                 # print(type(ndata[a1][index]))

#                                 n = (imgpath, position)

#                                 ndata[a1][index].append(n)

#                             else:

#                                 ndata[a1] = pd.Series([[] for i in range(len(ndata["Position"]))])

#                                 n = (imgpath, position)

#                                 ndata[a1][index].append(n)

#                 #video_file is the video file,input,datatype-str

#                 cap = cv2.VideoCapture(video_file)

#                 while (cap.isOpened()):

#                     # ret, frame = cap.read()

#                     # if ret == False:

#                     #     break

#                     # Works as expected

#                     # _, frame = cap.read()

#                     # cv2.imwrite('0_read.jpg', frame)

#                     # Returns a posterior frame

#                     ret = cap.set(cv2.CAP_PROP_POS_FRAMES, f)

#                     _, frame = cap.read()

#                     # print(_)

#                     # input_img = '/home/maxi/27-dec/' + str(j[0]) + '.jpg'

#                     # cv2.imwrite('/home/maxi/27-dec/' + str(j[0]) + '.jpg', frame)

#                     cap.release()

#                     cv2.destroyAllWindows()

#                     # img = image = cv2.imread(frame)

#                     box = (left, top, width, height)  # xmin,ymin,xmax,ymax

#                     #drawing bounding box on the image(frame)

#                     draw_bounding_box(frame, box, labels=[str(label1)], color='green')

#                     #output image

#                     cv2.imwrite(image0utputPath, frame)

#         #saving normalised file as csv file

#         ndata.to_csv(f"{vname}.csv")

# ​

#     # with open(f"/home/maxi/27-dec/8/1.json", "w") as outfile:

#     #     json.dump(data, outfile)