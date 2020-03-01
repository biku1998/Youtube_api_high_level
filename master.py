"""
This is master file that will run all the modules
"""

from youtube_lib.channel_id_collector import ChannelFetcher
from youtube_lib.channel_video_collector import ChannelVideoCollector
from youtube_lib.video_stats_collector import VideoStatsCollector

import os 

def main():

    if os.path.isdir('./data/') == False:
        os.mkdir('./data')

    if os.path.isdir('./meta_data_for_channels/') == False:
        os.mkdir('./meta_data_for_channels/')

    if os.path.isdir('./final_channel_data/') == False:
        os.mkdir('./final_channel_data/')

    query_topic = input('Enter query topic --- ')

    cf  = ChannelFetcher(path_to_api_key = "E:/google_api_key.json",query_topic=query_topic)
    
    cf.read_search_response() # will dump channel_id name mapping json

    cvc = ChannelVideoCollector(channel_id_json_path=f'./data/{query_topic}_channel_id_name.json',
            path_to_api_key='E:/google_api_key.json')

    # cvc.read_channel_id()
    cvc.fetch_upload_id()
    cvc.fetch_videos_info(max_n_channels=30)

    sc = VideoStatsCollector(path_to_api_key='E:/google_api_key.json')

    
    video_files_list = sc.get_all_video_files()

    ch_dfs = sc.parse_video_files(video_files_list)

    for df in ch_dfs:
        df_name = df['channelTitle'].unique()[0]
        file_name = f'./meta_data_for_channels/meta_data_for_{df_name}.csv'
        df.to_csv(file_name,index = False)

    ch_video_id_list  = sc.read_csv_meta_files()
    sc.collect_video_stats(ch_video_id_list)







if __name__ == '__main__':
    main()

