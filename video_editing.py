from moviepy.editor import VideoFileClip, concatenate_videoclips
import json


video_file = "recording_2024-05-16_15-48-28.avi"

with open('gesture_log.json', 'r') as f:
    gesture_log = json.load(f)

original_clip = VideoFileClip(video_file)
clips = []
i = 0
while i < len(gesture_log) - 1:  
    start_gesture = gesture_log[i]
    end_gesture = gesture_log[i+1]
    
    if start_gesture["gesture"] == "thumbs_up" and end_gesture["gesture"] == "thumbs_down":
        start_time = start_gesture["timestamp"]
        end_time = end_gesture["timestamp"]
        
        start_time = max(0, start_time)
        end_time = min(end_time, original_clip.duration)
        
        if start_time < end_time:
            clip = original_clip.subclip(start_time, end_time)
            clips.append(clip)
        
        i += 2  
    else:
        i += 1  

if clips:
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("edited_video.mp4")
else:
    print("No valid clips found based on gestures.")
