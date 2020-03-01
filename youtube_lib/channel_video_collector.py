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

    def get_resource(self):
        self.read_key() #  read the api keys.
        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey = self.api_key,
                        cache_discovery=False)
        return youtube
    
    def read_channel_id(self):
        """
        This method will read all the channel id's from the given json path.
        """
        print("\n Reading channel Id's ......\n")
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
        print("\nFetching upload id's of every channel !!\n")
        self.read_channel_id() # read channel id's 
        channel_list = list() # will store all the channel objects
        youtube  = self.get_resource() # create the resource
        
        if self.channel_id_list is not None:
            # print(self.channel_id_list)
            for ch in tqdm(self.channel_id_list):
                channel = youtube.channels().list(id = ch,part = 'contentDetails').execute()
                # channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                # print((channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']))
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
        print("\nFetching every video information present in each channel channel !!\n")
        if self.channels_upload_id_json_path is not None:

            youtube = self.get_resource()
            temp_upload_id = None
            channel_id_list = []

            # read the upload_id's in a list
            channels_upload_id = list()
            video_resource = None
            with open(self.channels_upload_id_json_path) as F:
                file_data = json.load(F) # list of all the channel id's
                channel_id_list += file_data

            for ch_id in tqdm(channel_id_list[:2]):
                video_resource = self.fetch_all_video_with_channel_upload_id(ch_id)
                # now we have to save the above data into a json object
                channel_video_dict = dict()
                channel_video_dict[ch_id] = video_resource
                
                if os.path.isdir('./data/')== False:
                    os.mkdir('./data')
                file_name = f'./data/channel_upload_id_{ch_id}_all_videos.json'
                with open(file_name,'w') as F:
                    json.dump(channel_video_dict,F)
                    print(f'\nvideo data file dumped for {ch_id}!')
            
            print('Data collection completed for all channels.Please check the data folder in the current dir')
            
                
        else:
            raise Exception("""please run the fetch_upload_id method before running this module as
                channel upload id json file is not fetched yet""")   

    def fetch_all_video_with_channel_upload_id(self,channel_upload_id):
        """
        This method will fetch all the videos for a particular channel given the channel Id
        """
        videos_raw = []
        nextPageToken = None
        if len(channel_upload_id) != 0:
            youtube = self.get_resource()
            
            while True:
                results = youtube.playlistItems().list(
                    playlistId = channel_upload_id,
                    part = 'snippet',
                    maxResults = 50,
                    pageToken = nextPageToken
                ).execute()

                videos_raw += results['items']
                nextPageToken = results.get('nextPageToken')

                if nextPageToken is None:
                    break

            return videos_raw                

        else:
            raise Exception('Empty channel type encountered !!!')

