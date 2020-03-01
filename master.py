"""
This is master file that will run all the modules
"""

from youtube_lib.channel_id_collector import ChannelFetcher
from youtube_lib.channel_video_collector import ChannelVideoCollector
from youtube_lib.video_stats_collector import VideoStatsCollector

if __name__ == '__main__':
    print('hello world')

