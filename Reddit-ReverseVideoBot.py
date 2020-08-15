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

SPAW = spaw.SPAW()
SPAW.auth(spawemail,spawpassword)

def bot_run():
    '''
    Looks for mentions of the bot and then downloads
    the submission video, reverses the video, posts it to
    Streamable, and replies to the comment with the link
    '''

    while True:
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
            videofilename = download_video()
            # This removes the .mp4 at the end
            shortenedfilename = os.path.basename(videofilename)[:-4]

            reverse_video_and_save(shortenedfilename)

            post_video_to_streamable(f'{shortenedfilename}reversed.mp4')

            # Allows for later use of Streamable link
            streamableurl = post_video_to_streamable()

            comment.reply(f'[Here is your reversed video!]({streamableurl})')

            delete_videos()


def download_video(submissionurl):
    '''
    Saves video from the provided reddit url to directory
    and returns the path to the saved video
    '''

    # Finds the video from the submission link
    # max_q means maximum quality
    videofile = redvid.Downloader(url = submissionurl, max_q = True)
    videofilename = videofile.download()
    return videofilename


def reverse_video_and_save(normalvideo):
    '''
    Takes the old video file and uses ffmpeg with the command
    line to apply the reverse video code below
    '''

    # os.system allows for usage of terminal commands
    os.system(f'ffmpeg -i {normalvideo}.mp4 -vf reverse {normalvideo}reversed.mp4')


def post_video_to_streamable(reversedvideo):
    '''
    Uploads the reversed video to https://streamable.com
    and returns the video's custom url
    '''

    # Returns dictionary of video info
    uploaded = SPAW.videoUpload(reversedvideo)
    # Connects streamable url with the id of the posted video
    streamableurl = 'https://streamable.com/' + uploaded['shortcode']
    return streamableurl


def delete_videos():
    '''
    Permanently deletes all .mp4 files from directory
    before next use
    '''

    [os.remove(file) for file in os.listdir(mydirectory) if file.endswith('.mp4')]



if __name__ == '__main__':
    bot_run()
