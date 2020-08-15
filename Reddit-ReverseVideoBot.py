import praw
import os
import spaw
import redvid
import re
from botsecrets2 import *

os.chdir(mydirectory)

reddit = praw.Reddit(username=PUT_USER_NAME_HERE,
                     password=PUT_PASSWORD_HERE,
                     client_id=PUT_CLIENT_ID_HERE,
                     client_secret=PUT_CLIENT_SECRET_HERE,
                     user_agent=PUT_USER_AGENT_HERE)

def bot_run():
    '''
    Looks for mentions of the bot and then downloads
    the submission video, reverses the video, posts it to
    Streamable, and replies to the comment with the link
    '''

    # Checks every new comment posted to reddit and skips ones
    # made before the bot ran
    for comment in reddit.subreddit('all').stream.comments(skip_existing=True):
        try:
            botcall = re.compile(r'!ReverseVideo',re.I).search(comment.body).group()
        except AttributeError:
            # continues if botcall can not be found
            continue

        try:
            download_video(comment.submission.url)
        except BaseException:
            # continues if there is no video in the reddit submission
            continue

        # Allows for later use of video file name
        LATER_ASSIGNED_VARS = download_video()

        reverse_video_and_save('os.path.basename')

        post_video_to_streamable('os.path.basename[:-4] + reversed.mp4')

        # Allows for later use of Streamable link
        LATER_ASSIGNED_VARS = post_video_to_streamable()

        comment_reply('streamablelink')

        delete_videos()


def download_video(submissionurl):
    pass
    # Return statement

def reverse_video_and_save(normalvideo):
    pass

def post_video_to_streamable(reversedvideo):
    pass
    # Return statement

def comment_reply(streamablelink):
    pass

def delete_videos():
    pass


#TODO Checklist
'''
refactor
multiline comments
comments throughout code
commit often - committing this change will...
inspiration --> https://sandiegofreepress.org/2017/11/one-veterans-dream-kurt-vonneguts-war-in-reverse-video-worth-watching/#.XzbBwS2z2Dc
'''
