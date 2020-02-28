"""
This module will fetch videos from the channel using channel id.
"""
# imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json
import pandas as pd
from tqdm import tqdm

class ChannelVideoCollector(object):
    def __init__(self,channel_id_json_path = None,path_to_api_key = None,regionCode = "IN"):
        self.api_key = None
        self.channel_id_list = None
        self.channel_id_json_path = channel_id_json_path
        self.path_to_api_key = path_to_api_key
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.regionCode = regionCode
        self.channels_upload_id_json_path = None

    def read_key(self):
        """
        This method will read api key from local file system
        """
        with open(self.path_to_api_key) as F:
            key_file = json.load(F)
            self.api_key = key_file['key_2']
    
    def read_channel_id(self):
        """
        This method will read all the channel id's from the given json path.
        """
        if os.path.isfile(self.channel_id_json_path):
            channel_id_list = []
            with open(self.channel_id_json_path,'r') as F:
                channel_ids = json.load(F)
                for ch in channel_ids:
                    channel_id_list.append(ch)
            self.channel_id_list = channel_id_list

        else:
            raise Exception('channel id Json path incorrect Or\
         File does not exist, run channel_id_collector.py before running this module')



    def fetch_upload_id(self):
        """
        This method will fetch all the upload id's for all the channels using channel id
        """
        self.read_key() #  read the api keys.
        self.read_channel_id() # read channel id's 
        channel_list = list() # will store all the channel objects
        next_page_token =  None
        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey = self.api_key,
                        cache_discovery=False)
        if self.channel_id_list is not None:
            for ch in tqdm(self.channel_id_list):
                channel = youtube.channels().list(id = self.channel_id_list[0],part = 'contentDetails').execute()
                # channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                channel_list.append(channel['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
            if os.path.isdir('./data/'):
                file_name_prepare = self.channel_id_json_path.split('/')[2].strip().split('.')[0]
                file_path = f'./data/content_upload_id_list_for_channels_related_to_{file_name_prepare}.json'
                self.channels_upload_id_json_path = file_path
                with open(file_path,'w') as F:
                    json.dump(channel_list,F)
        else:
            raise Exception('channel id list is not fetched yet. Please run the channel_id_collector module first')

    def fetch_videos_info(self):
        if self.channels_upload_id_json_path is not None:
            pass
        else:
            raise Exception('please run the fetch_upload_id method before running this module as \
                channel upload id json file is not fetched yet')   

    def parse_response(self):
        pass

    def read_search_response(self):
        pass

if __name__ == "__main__":
    cvc = ChannelVideoCollector(channel_id_json_path='./data/machine learning_channel_id_name.json',
            path_to_api_key='E:/google_api_key.json')
    cvc.fetch_upload_id()

