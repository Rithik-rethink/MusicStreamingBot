from youtubesearchpython import SearchVideos
from youtubesearchpython import SearchPlaylists
import youtube_dl
import sys
import playsound
import os
import subprocess
import multiprocessing
import random
import time

songs_list = []
my_playlist = []
def findurl():
    song_ob = SearchVideos(user_query , offset = 1 , mode = 'json' , max_results = 5)
    return song_ob.links[0]
    
def converttomp3(url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = url , download = False
    )
    filename = video_info['title'] + ".mp3"
    options = {
        'format' : 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192'
        }] 
    }
    with youtube_dl.YoutubeDL(options) as ydl :
        ydl.download([video_info['webpage_url']])
    subprocess.call(['clear'])
    return(filename)

def playmusic(music,i):
    songs_list.append(music)
    print('Added to queue: {}'.format(music))
    print('Now Playing {}'.format(music))
    if i+1 < len(my_playlist):
        print('Next Up {}'.format(my_playlist[i+1]))
    playsound.playsound(music)
    os.remove(music)
    if len(my_playlist) == 0:
        print('No more songs in the queue')

if __name__ == "__main__":
    while(1):
        try:
            print('Booting up bot.. Please wait')
            user_query = input('Enter songs to add to queue, queue has {} track(s)..\t{}\n'.format(len(my_playlist),time.ctime()))
            my_playlist.append(user_query)
            i = len(my_playlist) - 1
            while i < len(my_playlist):
                try:
                    url = findurl()
                    music = converttomp3(url)
                    playmusic(music,i)
                except:
                    print('Check your internet and try again')
                    if len(my_playlist) > 0:
                        my_playlist.pop(len(my_playlist) - 1)
                    user_query = input('Enter track name again to add in queue:\n')
                    my_playlist.append(user_query)
                    i = len(my_playlist) - 1
                    continue
                user_query = input('1. Enter tracks to add in queue\n2. \'q\' or \'quit\' for quitting the queue,\n3. \'r\' or \'rem\' to remove the current track from playlist,\n4. \'s\' to shuffle the playlist ,\n5. \'rep\' to repeat the current track ,\n6. \'c\' to continue playing songs in the guild\n')
                if user_query == 'q' or user_query == 'quit':
                    break
                elif user_query == 'r' or user_query == 'rem':
                    print('Removed track {}'.format(my_playlist[i]))
                    my_playlist.pop(i)
                    if(len(my_playlist) == 0):
                        user_query = input('No more tracks in the queue. Bot going to sleep..(Enter song name to restart the Bot:) ')
                        my_playlist.append(user_query)
                        i = len(my_playlist) - 1
                        continue
                    
                    else:
                        for j in range(len(my_playlist)):
                            print(j+1 , end = ' ')
                            print(my_playlist[j])

                        i = input('Choose song to play or enter a new song name(eg. 1,2..)\n')
                        if i.isnumeric():
                            i = int(i)
                            i -= 1
                            user_query = my_playlist[i]
                            continue
                        user_query = i
                        my_playlist.append(user_query)
                        i = len(my_playlist) - 1
                        continue
                elif user_query == 'c':
                    i += 1
                    if i >= len(my_playlist):
                        print('Playing from start.. ')
                        i = 0
                        for i in range(len(my_playlist)):
                            user_query = my_playlist[i]
                            url = findurl()
                            music = converttomp3(url)
                            playmusic(music,i)
                        user_query = input('Enter new song, songs in guild are done playing: ')
                        my_playlist.append(user_query)
                        i = len(my_playlist) - 1
                        continue

                elif user_query == 'rep':
                    user_query = my_playlist[len(my_playlist) - 1]
                    continue
                elif user_query == 's':
                    if len(my_playlist) == 1:
                        user_query = input('Enter new song, can\'t shuffle , playlist contains only 1 song: ')
                        i = len(my_playlist) - 1
                        
                        continue
                    random.shuffle(my_playlist)
                    print(my_playlist)
                    i = 0
                    for i in range(len(my_playlist)):
                        user_query = my_playlist[i]
                        url = findurl()
                        music = converttomp3(url)
                        playmusic(music,i)
                    user_query = input('Enter new song, songs in guild are done playing: ')
                    my_playlist.append(user_query)
                    i = len(my_playlist) - 1
                    continue
                else:
                    my_playlist.append(user_query)
                
                i = len(my_playlist) - 1
        finally:
            if user_query == 'q' or user_query == 'quit':
                break
            else:
                if len(my_playlist) > 0:
                    my_playlist.pop(len(my_playlist)-1)
                user_query_res = input('Press any key to restart bot(This may be due to bad internet connectivity): ')
