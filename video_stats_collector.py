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
pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

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
    
    def get_all_video_files(self):
        """
        This method will read all video_files name and return it
        """
        if os.path.isdir('./data/'): 
            video_files =  list(filter(lambda x:'all_videos.json' in x ,os.listdir('./data/')))
            return video_files
        else:
            raise Exception('data folder do not exists!!')
    def parse_video_files(self,video_list = None):
        """
         This function will parse the video files and extract information required to pull video stats   
        """
        columns_for_dataFrame_metadata = ['publishedAt','channelId','title','description','channelTitle',\
            'videoId']
        channels_dataFrames = []

        if video_list is not None:
            all_files_data = list() # will store channel video file names
            for f in video_list:
                with open(f'./data/{f}','r') as F:
                    all_files_data.append(json.load(F))
            
            # every data file has 1 dict, and in that dict there is one value encopassing all videos
            for data_file in all_files_data:
                df = pd.DataFrame(columns=columns_for_dataFrame_metadata) # dataFrame to store current channel video data
                channel_data_dict = list(data_file.values())[0] # this dict will contain all the video files of the channel
                # now we have to parse it and prepare a meta_data for that channel
                print('reading the channel data from json and storing in dataFrame .....\n')
                for video_file in tqdm(channel_data_dict):
                    d = video_file['snippet']
                    # print(d['publishedAt'])
                    # print(d['channelId'])
                    # print(d['title'])
                    # print(d['description'])
                    # print(d['channelTitle'])
                    # print(d['resourceId']['videoId'])
                    # print('*'*100)  # for debug
                    
                    # now we will store all the above information in the data Frame

                    df = df.append({
                        'publishedAt':d['publishedAt'],
                        'channelId':d['channelId'],
                        'title':d['title'],
                        'description':d['description'],
                        'channelTitle':d['channelTitle'],
                        'videoId':d['resourceId']['videoId']
                    },ignore_index=True)
                channels_dataFrames.append(df)
            return channels_dataFrames

        else:
            raise Exception('Empty or None videos list passed !!')


if __name__ == '__main__':
    sc = VideoStatsCollector()

    video_files_list = sc.get_all_video_files()
    ch_dfs = sc.parse_video_files(video_files_list)

    if os.path.isdir('./meta_data_for_channels') == False:
        os.mkdir('./meta_data_for_channels')
    
    for df in ch_dfs:
        df_name = df['channelTitle'].unique()[0]
        file_name = f'./meta_data_for_channels/meta_data_for_{df_name}'
        df.to_csv(file_name,index = False)
        

    
    
    


    