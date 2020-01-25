#!/usr/bin/env python
# coding: utf-8

# In[66]:


#Step 1 :

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
#!pip install mtranslate
#!pip install langdetect
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
import mtranslate
import langdetect
import re


# In[67]:


#Step 2 :

DEVELOPER_KEY = "AIzaSyBiTLl0Pis4g7RJCAEwjPobBaqrWW9rHdI"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
from youtube_transcript_api import YouTubeTranscriptApi


# In[68]:


#Step 3 :

def youtube_search(q, max_results=49,order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", 
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
            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
            viewCount.append(response['items'][0]['statistics']['viewCount'])
 
        try:
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        except:
            commentCount.append(0)
                
        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])
        
        try:
                likeCount.append(response['items'][0]['statistics']['likeCount'])
        except:
                likeCount.append(0)
        try:
                dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
        except:
                dislikeCount.append(0)
            
    for i in channelId:
        search_response2 = youtube.channels().list(part="snippet,statistics", id=i).execute()
        for search_result in search_response2.get("items", []):
            channelSub.append(search_response2['items'][0]['statistics']['subscriberCount'])
            
    youtube_dict = {'videoId':videoId,'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount,'channelSubCount':channelSub}

    return youtube_dict


# In[108]:


#Step 4:

import os
os.chdir("C:/Users/antony.morais/Desktop/Amalraj/Youtube Automation Blog")
df=pd.DataFrame(youtube_search("Samsung Galaxy M30 S", max_results=49))
df1 = df[['title','videoId','viewCount','channelTitle','channelSubCount','commentCount','likeCount','dislikeCount','tags','favoriteCount','channelId','categoryId']]
df1.columns = ['Title','VideoId','ViewCount','ChannelTitle','ChannelSubCount','CommentCount','likeCount','dislikeCount','tags','favoriteCount','channelId','categoryId']


# In[109]:


# df1.loc[:,'title_translated']=df1['Title']
# df1.loc[:,'title_translated']=df1.apply(lambda row: mtranslate.translate(row.Title,"en","auto"), axis=1)


# In[110]:


# df1.shape


# In[111]:


# import urllib.request, json 
# with urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCOhHO2ICt0ti9KAh-QHvttQ&key=AIzaSyBiTLl0Pis4g7RJCAEwjPobBaqrWW9rHdI") as url:
#     data = json.loads(url.read().decode())
#     print(data)


# In[112]:


# from pandas.io.json import json_normalize
# json_normalize(data['kind'])


# In[113]:


#Step 5:

#Remove Tutorial Videos
df1=df1[[not i for i in df1.Title.str.contains("how to|tutorial|getting started")]]
#Retain only one video per channel (channelID column) based on highest value of Views, Likes and Comments.
#This is to overcome redundant information.
df1.sort_values(['ViewCount','likeCount','CommentCount'], ascending=[False,False,False],inplace=True)
df1.reset_index(drop=True,inplace=True)
# df1_dup=pd.DataFrame(df1.duplicated(subset='channelId', keep='first'))
# df1_dup.columns=["Dup"]
# df_red=df1[df1_dup['Dup']==False]
# df_red.reset_index(drop=True,inplace=True)
# df_red.shape
df_red=df1


# In[114]:


df_red.shape


# In[115]:


#Step 6:

df_red.loc[:,"emv_video"] = df_red.apply(lambda row: int(row.ViewCount)*0.14+int(row.CommentCount)*8.20+int(row.likeCount)*0.72, axis=1)
#df1.loc[:,"emv_subscriber"] = df1.apply(lambda row:int(row.ChannelSubCount)*16.54 , axis=1)


# In[116]:


videoid = list(df_red['VideoId'])
x = YouTubeTranscriptApi.get_transcripts(videoid, continue_after_error=True)
vids_with_sub = x[0]
vids_without_sub = x[1]
df_trans = pd.DataFrame(list(vids_with_sub.keys()), columns=['VideoId'])


# In[117]:


result2= []
for i in range(0,len(vids_with_sub)):
    print(i)
    result1 = []
    list_con = list(vids_with_sub.values())[i]
    for j in list_con:
        text_proc=j['text']
        if(re.findall('[a-zA-Z]',text_proc)==[]) :
            text_proc_fin=text_proc
            #print(text_proc_fin)
        else :
            txt_lan=langdetect.detect(text_proc)
            if(txt_lan!='en'):
                try :
                    #print("Translating !!!!!!!!!")
                    text_proc_fin=mtranslate.translate(text_proc,"en","auto")
                except :
                    text_proc_fin=text_proc
                #print(text_proc_fin)
            else :
                text_proc_fin=text_proc
                #print(text_proc_fin)
        result1.append(text_proc_fin)
    result2.append(' '.join(result1))


# In[118]:


df_trans['Transcripts'] = result2


# In[119]:


fin_df = pd.merge(df_red, df_trans, how='left', left_on='VideoId', right_on='VideoId')
fin_df=fin_df.drop(['categoryId','channelId','ChannelTitle','VideoId','Title','VideoId','tags','favoriteCount'], axis = 1) 
fin_df.reset_index(drop=True).to_csv("Samsung_Galaxy_M30S.csv", sep=',', encoding='utf-8',index=False)
