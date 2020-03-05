# Youtube_api_high_level
A small project that contains some high level libraries for fetching data from youtube data api v3.

## What this api can do ?

* given a query topic, the api will collect video statistics for every channel for visualization and data analysis

## How the api will do that ?

1. Given a **query** topic it will fire a search on youtube e.g say deep learning.
2. Then it will collect all the channel id's that makes video related to the above topic.
3. We have to pass another parameter i.e how many channels to consider ? - suppose we passed 10
4. The program will select top 10 channels from the list of may be 100 channels fetched in stage 2
5. Then we will collect the upload Id of all the channels, why upload id's ? As all the videos published by any channel is present in **upload folder**.
6. After we have all the upload Id's we will extract all the video Id's from the upload folder for every channel.
7. One we have all the video Id's of all the videos of all the channel's, We will start collecting video stats attributes from them i.e viewCount, likeCount, commentCount, dislikeCount,title,description etc.
8. All the data will we collected in JSON format as YouTube returns everything in JSON, we will convert all the data in a cleaned csv file and put all the files for all the channels in a seperate folder named **final_channel_data** (will be created during the process automatically)

## Once we have all the data we can make plots, or even a dashboard using dash that will automatically be created and launched(in progress).

## packages required to use the api
* pip install numpy
* pip install pandas
* pip install json
* pip install tqdm
* pip install --upgrade google-api-python-client
* pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

## Also you need to create your own YouTube Data v3 api key(It's free, just don't fetch more than 20 channels data at a time)

## Steps to create api key
1. go to https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwiHpfyd0YLoAhXRfX0KHTkWAvIQFjAAegQICBAC&url=https%3A%2F%2Fconsole.developers.google.com%2F&usg=AOvVaw39ieEDI7pzBj4NtuzqS57M
2. agree to the terms 
 ![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_1_.jpg)
3.  Create a new project
![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_2_.jpg)
4. give a unique name to the project
![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_3_.jpg)
5. search for youtube data api v3
![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_4_.jpg)
6. Enable the api
![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_5.jpg)
7. Creata credentials
![Image description](https://github.com/biku1998/Youtube_api_high_level/blob/master/steps_screenshots/step_6.jpg)

### Once you have the api key, store it somewhere locally in a json format
like {'key_1':your_api_key}

### after that put the path of the json file in the master.py file in the variable API_KEY_PATH

### Run the master.py file

## Working sample : https://drive.google.com/open?id=1jGKlcLj9jOwZMs_fEt2KpCr1qLIjFuXr