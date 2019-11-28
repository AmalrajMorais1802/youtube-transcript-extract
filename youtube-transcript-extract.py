#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install apiclient
#!pip install freeze
#!pip install oauth2client
#!pip install google-cloud
#!pip install google
#!pip install google-cloud-language
#!pip install youtube-data-api
#!pip install google-api-python-client
#!pip install youtube_transcript_api
#!pip install youtube-python
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as matplot


# In[2]:


DEVELOPER_KEY = "<Insert your API Key>"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
#from youtube_data import youtube_search
from youtube_transcript_api import YouTubeTranscriptApi
#YouTubeTranscriptApi.get_transcript('')


# In[3]:


def youtube_search(q, max_results=49,order="relevance", token=None, location=None, location_radius=None):

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want 
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []
    channelSub = []
    
    for search_result in search_response.get("items", []):
  
  
        if ((search_result["id"]["kind"] == "youtube#video") or (search_result["id"]["kind"] == "youtube#channel")):

            title.append(search_result['snippet']['title']) 

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(part='statistics, snippet',id=search_result['id']['videoId']).execute()
            #response1 = youtube.channels().list(part='statistics', id=search_result['id']['videoId']).execute()
            #channelSub.append(response1['items'][0]['statistics']['subscriberCount'])

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
            #likeCount.append(response['items'][0]['statistics']['likeCount'])
            #dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
 
        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        else:
            commentCount.append([])
  
        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])
        
        if 'likeCount' in response['items'][0]['snippet'].keys():
            likeCount.append(response['items'][0]['snippet']['likeCount'])
        else:
            likeCount.append([])
        
        if 'dislikeCount' in response['items'][0]['snippet'].keys():
            dislikeCount.append(response['items'][0]['snippet']['dislikeCount'])
        else:
            dislikeCount.append([])
            
    for i in channelId:
        search_response2 = youtube.channels().list(part="snippet,statistics", id=i).execute()
        for search_result in search_response2.get("items", []):
            channelSub.append(search_response2['items'][0]['statistics']['subscriberCount'])
            

    youtube_dict = {'videoId':videoId,'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount,'channelSubCount':channelSub}

    return youtube_dict


# In[4]:


df=pd.DataFrame(youtube_search("Redmi Note 8 pro", max_results=49))
import os
os.chdir("<Mention your preferred Directory>/Youtube Automation Blog")


# In[5]:


df.to_csv("redmi_note_8_pro.csv", sep=',', encoding='utf-8')


# In[6]:


df1 = df[['title','videoId','viewCount','channelTitle','channelSubCount','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']]
df1.columns = ['Title','videoId','viewCount','channelTitle','Channel_SubCount','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']


# In[ ]:




