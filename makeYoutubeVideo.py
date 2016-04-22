#!/usr/bin/python
# Import everything needed to edit video clips
import sys
from moviepy.editor import *

import sys, getopt

def help():
    print 'makeYoutubeVideo.py -m <machineName> -t <thinginr> -i <timelapsevideo>'
    sys.exit()

def main(argv):
    thingiverseNr = ""
    machineType=""
    videoName =""
    introImageTime = 5 # time the intro image is shown in seconds
    try:
        opts, args = getopt.getopt(argv,"hi:t:m:")
    except getopt.GetoptError:
        help()

    for opt, arg in opts:
      if opt == '-h':
          help()
      elif opt in ("-i", "--ifile"):
          videoName = arg
      elif opt in ("-t"):
          thingiverseNr = arg
      elif opt in ("-m"):
          machineType = arg

    if videoName == "":
        help()
        sys.exit()
    # Reduce the audio volume (volume x 0.8)
    clip = VideoFileClip(videoName)
    clip = clip.volumex(0)
    clip = vfx.freeze(clip, 0, introImageTime)
    intro = vfx.blackwhite(clip)
    intro = vfx.freeze(intro, 0, introImageTime)
    intro = intro.set_duration(introImageTime)
    intro = vfx.colorx(intro, 0.2)

    # print infos
    w,h = clip.size
    duration = clip.duration
    print "Input Video stats:"
    print "Video size W: " + str(w) + ", H " + str(h)
    print "Duration " + str(duration) + "s"



    if machineType != "":
        machineTypeTxt = TextClip("Machine:\n"+str(machineType),font="AvantGarde-BookOblique",fontsize=40,color='red', stroke_color="gray")
    else:
        machineTypeTxt = TextClip(" ",font="AvantGarde-BookOblique",fontsize=20,color='red', stroke_color="white")


    # prepare thingiverse hint in video
    if (thingiverseNr != ""):
        thingiverseTxt= TextClip("Printing thingiverse thing:\n"+str(thingiverseNr),font="AvantGarde-BookOblique",fontsize=40,color='blue', stroke_color="gray")
        thingiverseTxt = thingiverseTxt.set_pos("top")
        thingiverseTxt = thingiverseTxt.set_duration(introImageTime)
    else:
        thingiverseTxt= TextClip(" ",font="DejaVu-Serif",fontsize=25,color='blue', stroke_color="white")
        thingiverseTxt = thingiverseTxt.set_pos("top")
        thingiverseTxt = thingiverseTxt.set_duration(introImageTime)
        

    machinetypeTxt = machineTypeTxt.set_pos('center').set_duration(introImageTime)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([intro, machinetypeTxt, thingiverseTxt ])
    # Freeze the last frames and crop the video a little
    video = vfx.freeze(video, video.duration - 0.1, introImageTime)
    video.set_duration(video.duration - 0.2,True)
    # fade out.. 
    video = vfx.fadeout(video, introImageTime)
    # print infos
    w,h = video.size
    duration = video.duration
    print "####"
    print "Output Video stats:"
    print "Video size W: " + str(w) + ", H " + str(h)
    print "Duration " + str(duration) + "s"
    # Write the result to a file (many options available !)
    video.write_videofile(videoName.replace(".","") + "_edited.mp4")

if __name__ == "__main__":
    main(sys.argv[1:])
