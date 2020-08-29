import praw
import os
import spaw
import redvid
import re
from botsecrets2 import spawemail, spawpassword
from botsecrets2 import PUT_USER_NAME_HERE, PUT_PASSWORD_HERE, PUT_CLIENT_ID_HERE, PUT_CLIENT_SECRET_HERE, PUT_USER_AGENT_HERE
from botsecrets2 import mydirectory


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

            # Finds the downloaded video and returns the name without .mp4
            for file in os.listdir():
                if file.endswith('.mp4'):
                    shortenedfilename = file[:-4]

            reverse_video_and_save(shortenedfilename)

            post_video_to_streamable(f'{shortenedfilename}reversed.mp4')

            # Allows for later use of the Streamable link
            streamableurl = post_video_to_streamable(f'{shortenedfilename}reversed.mp4')

            comment.reply(f'[Here is your reversed video!]({streamableurl})\n\nThe video might take a few minutes to finish processing. If there are any problems, private message this account (It is used as a normal user and bot)')

            delete_videos()


def download_video(submissionurl):
    '''
    Saves video from the provided reddit url to directory
    and returns the path to the saved video
    '''

    # Finds the video from the submission link
    # max_q means maximum quality
    videofile = redvid.Downloader(url = submissionurl, max_q = True)
    videofile.download()


def reverse_video_and_save(normalvideo):
    '''
    Takes the old video file and uses ffmpeg with the command
    line to apply the reverse video code below
    '''

    # os.system() allows for usage of terminal commands
    os.system(f'ffmpeg -i {normalvideo}.mp4 -vf reverse -af areverse {normalvideo}reversed.mp4')


def post_video_to_streamable(reversedvideo):
    '''
    Uploads the reversed video to https://streamable.com
    and returns the video's custom url
    '''

    # Returns dictionary of video info
    uploaded = SPAW.videoUpload(f'{mydirectory}/{reversedvideo}')
    # Connects streamable url with the id of the posted video
    streamableurl = 'https://streamable.com/' + uploaded['shortcode']
    return streamableurl


def delete_videos():
    '''
    Permanently deletes all .mp4 files
    from personal directory before next use
    '''

    [os.remove(file) for file in os.listdir(mydirectory) if file.endswith('.mp4')]



if __name__ == '__main__':
    bot_run()


# deployment --> 'https://education.github.com/pack?sort=popularity&tag=Cloud'
