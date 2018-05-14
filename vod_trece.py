from urllib import request
from bs4 import BeautifulSoup
import requests

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

display = Display(visible=0, size=(1920, 1080)).start()

driver = webdriver.Firefox()
    

def make_soup(url):
  hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
  
  req = request.Request(url, headers=hdr)
  page = request.urlopen(req).read()
  soup = BeautifulSoup(page,'html.parser')
  return(soup)

base = "https://www.eltrecetv.com.ar"
capitulos = '/simona/capitulos-completos?page='

page_soup = make_soup('https://www.eltrecetv.com.ar/simona/capitulos-completos')

pages = []

last_page = page_soup.find('li', class_= 'pager__item pager__item--last').find('a')
last_page_url = last_page['href']
last_page_num = int(last_page_url[-1])
 
def find_links():
  l = []
  visited = []
  #d = {}
  for link in range(last_page_num):
    soup = make_soup(base+capitulos+str(link+1))
    for a in soup.find_all('a'):
      try:
        if '/programas/simona/capitulos-completos/capitulo' in a['href']:#and a['href'] not in visited:       
          l.append(base + a['href'])
          visited.append(a['href'])
          #d["Dato"] = base + a['href'].strip('#comments')
      except:
        pass
  return(l)

def pull_m3u8(soup):
  for i in soup.find_all('li', {"class": ["quality", "activeQuality"]}):
    print(i['data-value'])

  
if __name__ == '__main__':
    
    #https://api.vodgc.net/player/conf/playerId/PRZ9KU1515679151/contentId/557774
    #https://vod.vodgc.net/gid1/vod/Artear/Eltrece/47/SIMO899C9A803069DF3C3DA03E7C912DB023208_1080P.mp4
    #https://vod.vodgc.net/manifest/SIMO899C9A803069DF3C3DA03E7C912DB023208.m3u8
    
    lst = find_links()
#    url = 'https://www.eltrecetv.com.ar/programas/simona/capitulos-completos/capitulo-73-de-simona_101489'
#    
#    codigo = make_soup(url)
#  
#    with open("output1.html", "w") as file:
#        file.write(str(codigo))
    
    l = []
    for row in lst:
        if row not in l:
            page_source = make_soup(row)
            episode_number = page_source.find('h1', class_ = 'heading').get_text()
            episode_name = page_source.find('h3', class_ = 'head-line').get_text()
            vodgc = ([i['src'] for i in page_source.find_all('iframe')])
            link = vodgc[1]
            driver.get(link)
            driver_source = driver.page_source
            vod_final = BeautifulSoup(driver_source, 'html.parser')          
            m3u8 = ([i['data-value'] for i in vod_final.find_all('li', class_ = 'quality activeQuality')])
            kodi_link = ''.join(m3u8)
            id = kodi_link.split('/')[4]
            mp4_link = id.replace('.m3u8', '_1080P.mp4')
            pre_link = 'https://vod.vodgc.net/gid1/vod/Artear/Eltrece/47/'
            print("#EXTINF:-1,{} - {}\n{}{}".format(episode_number,episode_name,pre_link,mp4_link))
    
    