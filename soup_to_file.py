    url = 'https://www.eltrecetv.com.ar/programas/simona/capitulos-completos/capitulo-73-de-simona_101489'
    
    codigo = make_soup(url)
  
    with open("output1.html", "w") as file:
        file.write(str(codigo))
        
        
    
    #https://api.vodgc.net/player/conf/playerId/PRZ9KU1515679151/contentId/557774
    #https://vod.vodgc.net/gid1/vod/Artear/Eltrece/47/SIMO899C9A803069DF3C3DA03E7C912DB023208_1080P.mp4
    #https://vod.vodgc.net/manifest/SIMO899C9A803069DF3C3DA03E7C912DB023208.m3u8