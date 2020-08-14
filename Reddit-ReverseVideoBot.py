import praw
from botsecrets2 import *
import os
import urllib


os.chdir('/users/tabinda/documents/python/reddit-reversevideobot')

reddit = praw.Reddit(username=PUT_USER_NAME_HERE,
                     password=PUT_PASSWORD_HERE,
                     client_id=PUT_CLIENT_ID_HERE,
                     client_secret=PUT_CLIENT_SECRET_HERE,
                     user_agent=PUT_USER_AGENT_HERE)

def bot_run():
    pass

def find_link_and_download(redditsubmission):
    pass

def reverse_video_and_save(videofile):
    pass

def post_video(videolink/download???):
    pass





#TODO Checklist
'''
multiple functions
refactor
multiline comments
comments throughout code
commit often - committing this change will...
inspiration --> https://sandiegofreepress.org/2017/11/one-veterans-dream-kurt-vonneguts-war-in-reverse-video-worth-watching/#.XzbBwS2z2Dc
'''
