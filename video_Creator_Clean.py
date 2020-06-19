import subprocess
import os
import pandas as pd
import csv
import math
import numpy as np
import statistics as st
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def create_Scene_list(videoname):
    command = F"scenedetect -i {videoname}.mp4 -s {videoname}.stats.csv   list-scenes detect-content"
    var = os.popen(command)



def parse_csvFiles(videoname):
    df_scenes = pd.read_csv(F"{videoname}-Scenes.csv")
    timestamps = list(df_scenes)

    del timestamps[0]

    time_codes_scenes = []
    for i in timestamps:
        time_codes_scenes.append(i)
        
    with open(F"{videoname}.stats.csv") as fp:
        reader = csv.reader(fp, delimiter=",")
        data_read = [row for row in reader]
    
    del data_read[0]

    time_codes_stats = []
    content_vals = []

    
    for i in range(1,len(data_read)-1):
        time_codes_stats.append(data_read[i][1])
        content_vals.append(float(data_read[i][2]))

    wanted_scenes_end_time = []
    wanted_scenes_start_time = []
    previous_scene = 0
    for scene in timestamps:
        content_avg = []
        for i in range(previous_scene, time_codes_stats.index(scene)+1):
            content_avg.append(content_vals[i])
            if scene == time_codes_stats[i]:
                previous_scene = i
                if st.mean(content_avg) <= 3 and timestamps.index(scene)-1 >= 0:
                    wanted_scenes_start_time.append(timestamps[timestamps.index(scene)-1])
                    wanted_scenes_end_time.append(scene)
                break
            
    return wanted_scenes_start_time, wanted_scenes_end_time


def create_videos(videoname, wanted_scenes_start_time,wanted_scenes_end_time):
    path = os.path.abspath(F"{videoname}.mp4")
    clip_concat = []

    for i in range(len(wanted_scenes_end_time)):
        clip = VideoFileClip(path).subclip(wanted_scenes_start_time[i] , wanted_scenes_end_time[i])
        clip.write_videofile(F"{videoname}_point_{i}.mp4")
        path1 = os.path.abspath(F"{videoname}_point_{i}.mp4")
        clip_concat.append(VideoFileClip(path1))
    

def just_concat_videos(videoname):

    clip_concat = []
    
    for i in range(10000):
        if os.path.exists(F"{videoname}_point_{i}.mp4"):
            path = os.path.abspath(F"{videoname}_point_{i}.mp4")
            clip = VideoFileClip(path)
            clip_concat.append(clip)
            print(i)
            
    
    final_clip = concatenate_videoclips([element for element in clip_concat])
    final_clip.write_videofile(F"{videoname}_combined_points.mp4")

