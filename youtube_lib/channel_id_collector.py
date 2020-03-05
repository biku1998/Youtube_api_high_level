"""
This module will be used to fetch channel id's that make videos on certain topics
"""

# imports
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json



class ChannelFetcher(object):
    def __init__(self,path_to_api_key,query_topic,max_results=50,regionCode="IN"):
        """
        query_topic : topic for channel fetching e.g 'machine learning'
        max_results : maximum results to fetch
        path_to_api : api key json file
        regionCode : 'IN' for india location , 'US' for united states etc
        """
        self.query_topic = query_topic
        self.path_to_api_key = path_to_api_key
        self.max_results = max_results
        self.api_key = None
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.regionCode = regionCode
    
    def read_key(self):
        """
        This method will read api key from local file system
        """
        with open(self.path_to_api_key) as F:
            key_file = json.load(F)
            self.api_key = key_file['key_2']
        # print(self.api_key) # for debug
    
    def fetch(self):
        """
        This method will fetch data using youtube api
        """
        self.read_key() # read the key
        start_num = 50 
        channel_id = list() # will store all the channel objects
        next_page_token =  None
        youtube = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        developerKey = self.api_key,
                        cache_discovery=False)

        while True:
            search_response  = youtube.search().list(
            q = self.query_topic,
            part = 'id,snippet',
            maxResults = self.max_results,
            regionCode = self.regionCode,
            pageToken = next_page_token).execute()
            
            channel_id += search_response['items']

            next_page_token = search_response.get('nextPageToken')

            start_num += 50

            if next_page_token is None:
                break

            if start_num >= 200: # so that we don't finish our daily quota. LOL
                break
            
            

        return channel_id
 
    def parse_response(self,response_obj):
        """
        This method will parse the search_response returned by the youtube api.
        parameters:
        response_obj : youtube api response object
        """
        channel_id_name_dict = dict() # to store key value pairs of channel_id and name
        for item in response_obj:
            channel_id_name_dict[item['snippet']['channelId']] = item['snippet']['channelTitle']
        return channel_id_name_dict

    def read_search_response(self,raw_response_obj = True):
        """
        This method will be called by the user to fetch the final results.
        If the user wants raw output or processed json output depends on the raw_response_obj parameter
        parameter :
        raw_response_obj : if False then the function will return raw output. No other modules will work.
        """
        search_response = self.fetch()

        if raw_response_obj == False:
            return search_response
        else:
            dict_channel = self.parse_response(search_response)
    
            # let's dump the result into json file
            if os.path.isdir('./data/') == False:
                os.mkdir('./data')
            file_name = f'./data/{self.query_topic}_channel_id_name.json'
            with open(file_name,'w') as F:
                json.dump(dict_channel,F)
            print('Channel Id fetching completed !!\n')

    
        


            


