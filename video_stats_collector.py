"""
This module will fetch videos statistics from the videos using  video id's.
"""
# imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json
import pandas as pd
from tqdm import tqdm

class VideoStatsCollector(object):
    def __init__(self,path_to_api_key = None,path_to_video_ids = None):
        self.path_to_api_key = path_to_api_key
        self.path_to_video_ids = path_to_video_ids
        self.api_key = None
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'

    def read_key(self):
        """
        This method will read api key from local file system
        """
        with open(self.path_to_api_key) as F:
            key_file = json.load(F)
            self.api_key = key_file['key_2']

    def get_resource(self):
        self.read_key() #  read the api keys.
        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey = self.api_key,
                        cache_discovery=False)
        return youtube
    
    