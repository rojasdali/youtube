from __future__ import unicode_literals
import youtube_dl
import urllib
import urllib2
from bs4 import BeautifulSoup


__author__ = 'Dali'
def getTextToSearch():
    isValid = False
    while not isValid:
        q = (raw_input('Please enter your search query: \n'))
        try:
             a = str(q)
             isValid = True
        except ValueError:
             print "Incorrect format"
    return a

def checkAnswer():
    isValid = False
    while not isValid:
        answer = (raw_input('Is this the video/song you want to download? (y or n) \n'))
        try:
            if answer in "y" or answer in "n":
                if answer in "n":
                    answer = False
                    isValid = True
                else:
                    answer = True
                    isValid = True
        except ValueError:
             print "Incorrect value"
    return answer

# download metadata
ydl = youtube_dl.YoutubeDL()
#r = None

#list of keywords in search query that bring up unwanted videos
listUnwanted = ['google','user', 'list', 'channel']

textToSearch = getTextToSearch()
query = urllib.quote(textToSearch)
url = "https://www.youtube.com/results?search_query=" + query
response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html, "lxml")
#listLinks=[]

listTitles=[] #empty list
for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}, limit = 10):
    if not any(x in vid['href'] for x in listUnwanted):
        #print 'https://www.youtube.com' + vid['href']
        listTitles.append(vid['title'])
        listTitles.append(['https://www.youtube.com' + vid['href']])
        #print vid['title']
        #print listTitles[-1]
        #print 'Please run program again and revise your search for more accurate results'
        #print " \n".join(str(x) for x in listTitles)
        #print " \n".join(str(x) for x in listLinks)
for i, title in enumerate(listTitles):
   if i % 2 == 0:
       ytUrl = "".join(str(x) for x in listTitles[i+1])
       print title
      # with ydl:
       # r = ydl.extract_info(ytUrl, download=False)  # don't download, much faster
       #print "views-%d  duration-%.02f" % (r['view_count'], r['duration']/60)
       if checkAnswer() is True:
           options = {
                'format': 'bestaudio/best',
                'extractaudio' : True,      # only keep the audio
                'audioformat' : "mp3",      # convert to mp3
                'outtmpl': '%(title)s.%(ext)s',        # name the file the ID of the video
                'noplaylist' : True,
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
    }],
}

           print 'downloading file........'
           with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([ytUrl])
           break
       else:
           continue









