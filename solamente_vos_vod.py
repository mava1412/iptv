from urllib import request
from bs4 import BeautifulSoup
import time
import random
import itertools

from pyvirtualdisplay import Display

from selenium import webdriver


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
capitulos = '/solamente-vos/capitulos-completos?page='

page_soup = make_soup('https://www.eltrecetv.com.ar/solamente-vos')

pages = []

last_page = page_soup.find('li', class_= 'pager__item pager__item--last').find('a')
last_page_url = last_page['href']
last_page_num = last_page_url.split('=')[-1]
page_no = int(last_page_num)
print(page_no)

l = []

def find_links_base_page():
    visited = []
    page = 'https://www.eltrecetv.com.ar/solamente-vos'
    soup = make_soup(page)
    for a in soup.find_all('a'):
        try:
            if '/programas/solamente-vos/capitulos-completos/capitulo' in a['href'] and a['href'] not in visited:
              l.append(base + a['href'])
              visited.append(a['href'])
        except:
            pass
    return(l)


def find_links():
  visited = []
  for link in range(page_no):
    soup = make_soup(base+capitulos+str(link+1))
    for a in soup.find_all('a'):
      try:
        if '/programas/solamente-vos/capitulos-completos/capitulo' in a['href'] and a['href'] not in visited:
          l.append(base + a['href'])
          visited.append(a['href'])
      except:
        pass
  return(l)


def trim_list(lst):
        final_lst = []
        for line in lst:
            if line not in final_lst and '#comments' not in line:
                final_lst.append(line)
        return(final_lst)


if __name__ == '__main__':

    display = Display(visible=0, size=(1920, 1080)).start()

    driver = webdriver.Firefox()
    
    lst_1 = find_links()
    lst_2 = find_links_base_page()
    
    final_list = itertools.chain(lst_1, lst_2)

    full_url_list = trim_list(final_list)
    print(len(full_url_list))
#    
#    with open('final_list.txt', 'w') as f:
#        for row in full_url_list:
#            f.write(row+ '\n')

    visited = []
    for row in full_url_list:
        if row not in visited:
            visited.append(row)
            page_source = make_soup(row)
            episode_number = page_source.find('h1', class_ = 'heading').get_text()
            #episode_name = page_source.find('h3', class_ = 'head-line').get_text()
            vodgc = ([i['src'] for i in page_source.find_all('iframe')])
            link = vodgc[1]
            driver.get(link)
            time.sleep(random.randint(2, 5))
            driver_source = driver.page_source
            vod_final = BeautifulSoup(driver_source, 'html.parser')          
            m3u8 = ([i['data-value'] for i in vod_final.find_all('li', class_ = 'quality activeQuality')])
            kodi_link = ''.join(m3u8).strip()
            id_link = kodi_link.split('/')[4]
            mp4_link = id_link.replace('.m3u8', '_480P.mp4')
            pre_link = 'https://vod.vodgc.net/gid1/vod/Artear/Eltrece/6/'
            print("#EXTINF:-1,{}\n{}{}".format(episode_number,pre_link,mp4_link))