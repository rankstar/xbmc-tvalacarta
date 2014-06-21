# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mail.ru
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mail.ru.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Descarga
    data = scrapertools.cache_page( page_url )
    logger.info("data="+data)
    url = scrapertools.get_match( data , 'videoSrc\s*\=\s*"([^"]+)"' )
    media_url = scrapertools.get_header_from_response(url,header_to_get="location")
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:] + " [mail.ru]",media_url ] )

    for video_url in video_urls:
        logger.info("[mail.ru] %s - %s" % (video_url[0],video_url[1]))

    return video_urls


    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://api.video.mail.ru/videos/embed/mail/cinemaxxmaxx/_myvideo/416.html
    patronvideos  = '(video.mail.ru/videos/embed/mail/[^/]+/[^/]+/\d+.html)'
    logger.info("[mail.ru.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mail.ru]"
        url = "http://api."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mailru' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
