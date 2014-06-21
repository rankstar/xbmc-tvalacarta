# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para goear
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "goear"
__category__ = "M"
__type__ = "xbmc"
__title__ = "goear"
__language__ = "ES"

DEBUG = config.get_setting("debug")

IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'goear' )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[goear.py] mainlist")

	
	
########################################## GENERA EL MENU PRINCIPAL################################

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar Canciones"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por número de reproducciones'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por calidad'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar y ordenar por fecha'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
 
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar PlayList"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
   
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar PlayList y ordenar por número de reproducciones'     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))
    
    itemlist.append( Item(channel=__channel__, action="search"     , title='Buscar PlayList y ordenar por fecha'     
    ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))

    
    itemlist.append( Item(channel=__channel__, action="search"     , title="Mostrar los PlayList de un Usuario"     ,     thumbnail=os.path.join(IMAGES_PATH, 'user100x100.png'), fanart=os.path.join(IMAGES_PATH, 'poster.png')))

    return itemlist
    
########################################################################################################################

def search(item,texto):
    logger.info("[goear.py] search")
   
    try:
        
    
        if item.title=="Buscar Canciones": 
            item.url = "http://www.goear.com/apps/android/search_songs_json.php?q=%s" % texto + "&p=0&order=default"
            
        if item.title=='Buscar y ordenar por número de reproducciones':
            item.url = "http://www.goear.com/apps/android/search_songs_json.php?q=%s" % texto + "&p=0&order=played"
            
        if item.title=='Buscar y ordenar por calidad':
            item.url = "http://www.goear.com/apps/android/search_songs_json.php?q=%s" % texto + "&p=0&order=quality"
                        
        if item.title=='Buscar y ordenar por fecha':
            item.url = "http://www.goear.com/apps/android/search_songs_json.php?q=%s" % texto + "&p=0&order=recent"
        #---------------------------------------------------------------------------------------------#    
            
        if item.title=="Buscar PlayList":
            item.url = "http://www.goear.com/apps/android/search_playlist_json.php?q=%s" % texto + "&p=0&order=default"
            
        if item.title=='Buscar PlayList y ordenar por número de reproducciones':
            item.url = "http://www.goear.com/apps/android/search_playlist_json.php?q=%s" % texto + "&p=0&order=played"
            
        #if item.title=='Buscar PlayList y ordenar por número de canciones':
        #    item.url = "http://www.goear.com/apps/android/search_playlist_json.php?q=%s" % texto + "&p=0&order=sounds"
            
        if item.title=='Buscar PlayList y ordenar por fecha':
            item.url = "http://www.goear.com/apps/android/search_playlist_json.php?q=%s" % texto + "&p=0&order=recent"
           
        if item.title=='Mostrar los PlayList de un Usuario':
            item.url = "http://www.goear.com/%s" % texto + "/playlist/0"
            
            
        if item.title=="Buscar Canciones":
            return search_results(item)
            
        if item.title=='Buscar y ordenar por número de reproducciones':
            return search_results(item)
            
        if item.title=='Buscar y ordenar por calidad':
            return search_results(item)
                        
        if item.title=='Buscar y ordenar por fecha':
            return search_results(item)
            
   

        if item.title=="Buscar PlayList":
            return search_playlist_results(item)
        
        if item.title=='Buscar PlayList y ordenar por número de reproducciones':
            return search_playlist_results(item)
            
        if item.title=='Buscar PlayList y ordenar por número de canciones':
            return search_playlist_results(item)
            
        if item.title=='Buscar PlayList y ordenar por fecha':
            return search_playlist_results(item)
            
        if item.title=='Mostrar los PlayList de un Usuario':
            return list_my_playlist(item)
        
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
        
        
        
################################################################################################################
#                          BUSCA y REPRODUCE RESULTADOS PARA CANCIONES SUELTAS                                 #
################################################################################################################

def search_results(item):
    
    logger.info("[goear.py] search_results")
    data = scrapertools.cachePage(item.url)
    patron = '"id":"[^"]+","title":"(.*?),"mp3path":"([^"]+)","imgpath".*?songtime":"([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedtitle, scrapedurl, scrapedtime in matches:
    
        scrapedurl = scrapedurl.replace("\\","")
        scrapedtitle = scrapedtitle.replace('","artist":"',' - ')
        scrapedtitle = scrapedtitle.replace('"',' ')
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedtitle = scrapedtitle + " / Duración: " + scrapedtime
        scrapedplot =  ""
    
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server="directo", folder=False))
    
    
    if 'playlist_songs_json' in item.url:
        url_pag_sig=""
    else:    
        #EXTRAE EL NUMERO DE PAGINA ACTUAL Y LO LIMPIA
        pag_actual = item.url[-17:-13]
        pag_actual = pag_actual.replace("p","")
        pag_actual = pag_actual.replace("&","")
        pag_actual = pag_actual.replace("=","")
    
        # INCREMENTA EN UNO EL NUMERO DE PAGINA
        pag_sig = int(pag_actual)+1
    
        # FABRICA EL LINK DE LA SIGUIENTE PAGINA DE RESULTADOS    
        url_pag_sig = item.url
        url_pag_sig = url_pag_sig.replace(pag_actual,repr(pag_sig))
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="search_results" , title=">> Pagina Siguiente", url=url_pag_sig, plot=item.plot))
    
    
    return itemlist
    


####################################################################################################################
####################################################################################################################
####################################################################################################################
#                                        BLOQUEPLAYLIST                                                            #
####################################################################################################################

def search_playlist_results(item):
    logger.info("[goear.py] search_playlist_results")
    data = scrapertools.cachePage(item.url)
    
    patron = '"id":"([^"]+)","title":"([^"]+)","plsongs":"([^"]+)","imgpath.*?songtime":"([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedid, scrapedtitle, scrapednumberofsongs, scrapedtime in matches:
    
        # fabrica el link tipo http://www.goear.com/apps/android/playlist_songs_json.php?v=999c96d
        scrapedurl =  "http://www.goear.com/apps/android/playlist_songs_json.php?v="+scrapedid
        scrapedplot = ""
        #scrapedtitle = scrapedtitle.replace("</span>","")
        #scrapedtitle = scrapedtitle.replace("</a>","")
        #scrapedtitle = scrapedtitle.replace('<p class="comment">'," - ")
        if scrapednumberofsongs == "1":
                scrapedtitle = scrapedtitle+ " - " + scrapednumberofsongs+" cancion "+ "- duracion: " + scrapedtime
        else:
                scrapedtitle = scrapedtitle+ " - " + scrapednumberofsongs+" canciones "+ "- duracion: " + scrapedtime
                
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="search_results" , title=scrapedtitle, url=scrapedurl, plot=scrapedplot))
    
    
    #EXTRAE EL NUMERO DE PAGINA ACTUAL Y LO LIMPIA
    pag_actual = item.url[-17:-13]
    pag_actual = pag_actual.replace("p","")
    pag_actual = pag_actual.replace("&","")
    pag_actual = pag_actual.replace("=","")
    
    # INCREMENTA EN UNO EL NUMERO DE PAGINA
    pag_sig = int(pag_actual)+1
    
    # FABRICA EL LINK DE LA SIGUIENTE PAGINA DE RESULTADOS    
    url_pag_sig = item.url
    url_pag_sig = url_pag_sig.replace(pag_actual,repr(pag_sig))
        
    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
    itemlist.append( Item(channel=__channel__, action="search_playlist_results" , title=">> Pagina Siguiente", url=url_pag_sig, plot=item.plot))
        
   
    return itemlist



##################################################################################################################
#                           LISTA los PLAYLIST DE un USUARIO     (UTILIZA API)                                   #
##################################################################################################################

def list_my_playlist(item):
    logger.info("[goear.py] list_my_playlist")
    data = scrapertools.cachePage(item.url)
    patron = '<a href="http://www.goear.com/playlist/([^/]+)/[^"]+"><span class="playlist">([^<]+)</span></a>.*?<li class="description">([^<]+)</li>'
                              
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedurl,scrapedtitle, scrapedplot in matches:
        # fabrica el link tipo http://www.goear.com/apps/android/playlist_songs_json.php?v=fdc5e49
        scrapedurl = "http://www.goear.com/apps/android/playlist_songs_json.php?v="+scrapedurl
        scrapedtitle = scrapedtitle + " - Playlist con " +scrapedplot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="playlist_play" , title=scrapedtitle , url=scrapedurl, plot=scrapedplot))
   
   
   
   #EXTRAE EL NUMERO DE PAGINA ACTUAL Y LO LIMPIA
    pag_actual = item.url[-3:]
    pag_actual = pag_actual.replace("t","")
    pag_actual = pag_actual.replace("/","")
    
    
    # INCREMENTA EN UNO EL NUMERO DE PAGINA
    pag_sig = int(pag_actual)+1
    
    # FABRICA EL LINK DE LA SIGUIENTE PAGINA DE RESULTADOS    
    url_pag_sig = item.url
    url_pag_sig = url_pag_sig.replace(pag_actual,repr(pag_sig))
    
    
        
    if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
    itemlist.append( Item(channel=__channel__, action="list_my_playlist" , title=">> Pagina Siguiente", url=url_pag_sig, plot=item.plot))
   
    return itemlist


#################################################################################################################
#                                EXTRAE EL LINK DEL PLAYLIST Y LO REPRODUCE                                     #
#################################################################################################################


def playlist_play(item):
    logger.info("[goear.py] playlist_play")
    data = scrapertools.cachePage(item.url)
    patron = '"id":"[^"]+","title":"(.*?),"mp3path":"([^"]+)","imgpath"'
  
    #{"id":"053eee9","title":"DINASTIA","artist":"series tv","mp3path":"http:\/\/live3.goear.com\/listen\/ea2cc54efa02be506cf891c6890799a1\/51460ec2\/sst\/mp3files\/06082006\/78313386a704d28e8ac0c6a0bf1e7848.mp3","imgpath":"http:\/\/userserve-ak.last.fm\/serve\/_\/11714861\/Series+TV+mejoresseriesempire1.jpg","songtime":"1:17"},
            
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for scrapedtitle, scrapedurl in matches:
    
        scrapedurl = scrapedurl.replace("\\","")
        scrapedtitle = scrapedtitle.replace('","artist":"',' - ')
        scrapedtitle = scrapedtitle.replace('"',' ')
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedtitle = scrapedtitle
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+""+"]")
        itemlist.append( Item(channel=__channel__, action="play" , server="directo", title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, folder=False))
    return itemlist
    
        
# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false
    
    # Comprueba si alguno de los vídeos de "Novedades" devuelve mirrors
    episodios_items = novedades(mainlist_items[0])
    
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien