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
    def __init__(self,path_to_api_key = None):
        self.path_to_api_key = path_to_api_key
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
        print("\nReading all video id's !!\n")
        """
        This method will read all video_files name and return it
        """
        if os.path.isdir('./data/'): 
            video_files =  list(filter(lambda x:'all_videos.json' in x ,os.listdir('./data/')))
            return video_files
        else:
            raise Exception('data folder do not exists!!')

    def parse_video_files(self,video_list = None):
        print("\nParsing all the video files to extract video id's and other information !!\n")
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
    
    def read_csv_meta_files(self):

        print("\nReading meta-data from csv's !!\n")
        if os.path.isdir('./meta_data_for_channels'):
            all_meta_data_csv_files = list(filter(lambda x:'.csv' in x ,os.listdir('./meta_data_for_channels')))
            return all_meta_data_csv_files
        else:
            raise Exception('No meta_data folder found')
    
    def collect_video_stats(self,channel_video_id_list):
        print("\nFetching and building video statistics files !!\n")
        if len(channel_video_id_list) != 0:
            # we will loop through all the csv's
            for f in channel_video_id_list:
                make_path = f'./meta_data_for_channels/{f}'
                # print(make_path)
                df = pd.read_csv(make_path)
                youtube  = self.get_resource()
                ch_name = df['channelTitle'].unique()[0]
                print(f'\ncollecting statistics of {ch_name} channel')
                stats = [] #  to store stats of videos of that channel

                for i in range(0,df['videoId'].shape[0],50):
                    res = youtube.videos().list(
                        id = ','.join(df['videoId'].tolist()[i:i+50]),
                        part = 'statistics'
                    ).execute()
                    stats += res['items']

                # now we will call a function and pass the fn the dataFrame and stats asscociated with it

                self.join_dataFrame_stats(df,stats)

                # also we will save the stats in meta_data folder , just be in safe side
                
                file_name = f'./meta_data_for_channels/{ch_name}_stats_meta_data.json'
                
                if os.path.isdir('./meta_data_for_channels/') == False:
                    os.mkdir('./meta_data_for_channels/')
                with open(file_name,'w') as F:
                    json.dump(stats,F)
                

        else:
            raise Exception('Empty channel videos Id list passed')
    
    def join_dataFrame_stats(self,df,stats_list):

        if df is not None and stats_list is not None:
            # print(len(stats_list))
            # print(df.shape)
            ch_name = df['channelTitle'].unique()[0]
            print(f'\n Merging data for channel {ch_name}')
            # let's make new columns in our dataFrames
            df['viewCount'] = 0
            df['likeCount'] = 0
            df['dislikeCount'] = 0
            df['favoriteCount'] = 0
            df['commentCount'] = 0

            viewCount = []
            likeCount = []
            dislikeCount = []
            favoriteCount = []
            commentCount = []

            # temp 
            # with open('./meta_data_for_channels/Simplilearn.json','r') as F

            # first_let's collect all the columns from the json dict and then we will just append them to the dataFrame
            print('\nCombining Statistics json data in  dataFrame') 
            for el in tqdm(stats_list):
                # print('\n',el['statistics']['likeCount'])
                
                if 'viewCount' in el['statistics'].keys():
                    viewCount.append(el['statistics']['viewCount'])
                else:
                    viewCount.append(0)

                if 'likeCount' in el['statistics'].keys():
                    likeCount.append(el['statistics']['likeCount'])
                else:
                    likeCount.append(0)

                if 'dislikeCount' in el['statistics'].keys():
                    dislikeCount.append(el['statistics']['dislikeCount'])
                else:
                    dislikeCount.append(0)

                if 'favoriteCount' in el['statistics'].keys():
                    favoriteCount.append(el['statistics']['favoriteCount'])
                else:
                    favoriteCount.append(0)
                
                if 'commentCount' in el['statistics'].keys():
                    commentCount.append(el['statistics']['commentCount'])
                else:
                    commentCount.append(0)


                
                # likeCount.append(el['statistics']['likeCount'])
                # dislikeCount.append(el['statistics']['dislikeCount'])
                # favoriteCount.append(el['statistics']['favoriteCount'])
                # commentCount.append(el['statistics']['commentCount'])

            df['viewCount'] = viewCount
            df['likeCount'] = likeCount
            df['dislikeCount'] = dislikeCount
            df['favoriteCount'] = favoriteCount
            df['commentCount'] = commentCount

            if os.path.isdir('./final_channel_data/') == False:
                os.mkdir('./final_channel_data/')
            
            file_name = f'./final_channel_data/{ch_name}_complete_data.csv'

            df.to_csv(file_name,index = False)    
                
                
        else:
            raise Exception('None type dataFrame or Stats list passed !!') 

if __name__ == '__main__':
    sc = VideoStatsCollector(path_to_api_key='E:/google_api_key.json')

    # video_files_list = sc.get_all_video_files()
    # ch_dfs = sc.parse_video_files(video_files_list)

    # if os.path.isdir('./meta_data_for_channels') == False:
    #     os.mkdir('./meta_data_for_channels')
    
    # for df in ch_dfs:
    #     df_name = df['channelTitle'].unique()[0]
    #     file_name = f'./meta_data_for_channels/meta_data_for_{df_name}.csv'
    #     df.to_csv(file_name,index = False)

    ch_video_id_list  = sc.read_csv_meta_files()
    sc.collect_video_stats(ch_video_id_list)


        

    
    
    


    