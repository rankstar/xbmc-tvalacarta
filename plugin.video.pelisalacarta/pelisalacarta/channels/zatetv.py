# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para zate.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__channel__ = "zatetv"
__title__ = "Zate.tv"
__language__ = "ES"

def isGeneric():
    return True

def mainlist(item):
    logger.info("channels.zatetv mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="menupeliculas" , title="Películas"           , url="http://zate.tv/peliculas/" ))
    #itemlist.append( Item(channel=__channel__, action="menuseries"    , title="Series"              , url="http://zate.tv/series/" ))
  
    return itemlist

def menupeliculas(item):
    logger.info("channels.zatetv menupeliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Todas"             , url="http://zate.tv/pelis/todasScroll/todos" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Últimas Agregadas" , url="http://zate.tv/pelis/ultAgregadas" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Estrenos"          , url="http://zate.tv/pelis/scrollEstrenos" ))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Destacadas"        , url="http://zate.tv/pelis/scrollDestacadas" ))
  
    return itemlist

def menuseries(item):
    logger.info("channels.zatetv menuseries")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="letras"  , title="Por orden alfabético" , url="http://animeflv.net/animes/?orden=nombre&mostrar=series" ))
    itemlist.append( Item(channel=__channel__, action="generos" , title="Por géneros"          , url="http://animeflv.net/animes/?orden=nombre&mostrar=series" ))
    itemlist.append( Item(channel=__channel__, action="series"  , title="En emisión"           , url="http://animeflv.net/animes/en-emision/?orden=nombre&mostrar=series" ))
  
    return itemlist

def generos(item):
    logger.info("channels.zatetv generos")

    itemlist = []

    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)
    data = scrapertools.get_match(data,'<div class="generos_box"(.*?)</div>')
    patron = '<a href="([^"]+)[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.entityunescape(scrapedtitle)
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=title , url=url, thumbnail=thumbnail, plot=plot))
    return itemlist

def search(item,texto):
    logger.info("channels.zatetv search")
    if item.url=="":
        item.url="http://animeflv.net/animes/?buscar="
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("channels.zatetv peliculas")

    # Descarga la pagina

    '''
    POST /pelis/todasScroll/todos HTTP/1.1
    Host: zate.tv
    Connection: keep-alive
    Content-Length: 42
    Cache-Control: max-age=0
    Accept: */*
    Origin: http://zate.tv
    X-Requested-With: XMLHttpRequest
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Referer: http://zate.tv/peliculas
    Accept-Encoding: gzip,deflate,sdch
    Accept-Language: es-ES,es;q=0.8
    Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
    Cookie: typefilter=todo; HstCfa2572748=1393007855506; HstCmu2572748=1393007855506; hide_beta=yes; HstCla2572748=1393008737204; HstPn2572748=9; HstPt2572748=9; HstCnv2572748=1; HstCns2572748=2; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%223332507da7d34fef7c30607178801121%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A12%3A%2280.26.231.69%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A119%3A%22Mozilla%2F5.0+%28Macintosh%3B+Intel+Mac+OS+X+10_8_5%29+AppleWebKit%2F537.17+%28KHTML%2C+like+Gecko%29+Chrome%2F24.0.1312.52+Safari%2F537.17%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1393009222%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dd5cfc8a834b586ac5f4da9626add165c; filtropelis=todos
    '''
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17"])
    headers.append(["Origin","http://zate.tv"])
    headers.append(["X-Requested-With","XMLHttpRequest"])
    headers.append(["Content-Type","application/x-www-form-urlencoded; charset=UTF-8"])
    headers.append(["Referer","http://zate.tv/peliculas"])

    if item.extra=="":
        item.extra = "action=scrollpagination&number=25&offset=0"
    
    post = item.extra
    #post = "action=scrollpagination&number=25&offset=25"
    data = scrapertools.cache_page(item.url,post=post,headers=headers)

    # Extrae las entradas (carpetas)  
    '''
    <div class="col-lg-2" id="post" style="width:150px;" >
    <a href="/peliculas/1"><img src="http://img.zate.tv/peliculas/imagen_32790.jpg" class="hover" width="150px" height="200px" />
    <div class="info">
    <p class="titulo">1</p>  
    <hr style="margin-bottom:0px;margin-top:0px;"/>
    <p class="desc">Centrado en la 'edad dorada' del Grand Prix Racing, sigue la historia una generación de carismáticos corredores y de los límites que alcanzaron durante su época en la Fórmula 1, arriesgando su vidas para cambiar el deporte para siempre. </p>
    </div>
    </a>
    </div>
    '''
    patron  = '<div class="col-lg[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^<]+'
    patron += '<div class="info"[^<]+'
    patron += '<p class="titulo">([^<]+)</p[^<]+'  
    patron += '<hr[^<]+'
    patron += '<p class="desc">(.*?)</p'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:

        title = scrapedtitle
        fulltitle = scrapedtitle
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapedplot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, viewmode="movie_with_plot"))

    valor = int(scrapertools.find_single_match(item.extra,'offset=(\d+)'))
    itemlist.append( Item(channel=__channel__, action="peliculas" , title=">> Página siguiente" , url=item.url, extra="action=scrollpagination&number=25&offset="+str(valor+25)))

    return itemlist

def series(item):
    logger.info("channels.zatetv series")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)

    # Extrae las entradas 
    '''
    <div class="aboxy_lista">
    <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA"><img class="lazy portada" src="/img/blank.gif" data-original="http://cdn.animeflv.net/img/portada/1026.jpg" alt="Nurarihyon no Mago OVA"/></a>
    <span style="float: right; margin-top: 0px;" class="tipo_1"></span>
    <a href="/ova/nurarihyon-no-mago-ova.html" title="Nurarihyon no Mago OVA" class="titulo">Nurarihyon no Mago OVA</a>
    <div class="generos_links"><b>Generos:</b> <a href="/animes/genero/accion/">Acci&oacute;n</a>, <a href="/animes/genero/shonen/">Shonen</a>, <a href="/animes/genero/sobrenatural/">Sobrenatural</a></div>
    <div class="sinopsis">La historia empieza en alrededor de 100 a&ntilde;os despu&eacute;s de la desaparici&oacute;n de Yamabuki Otome, la primera esposa Rihan Nura. Rihan por fin recobr&oacute; la compostura y la vida vuelve a la normalidad. A medida que la cabeza del Clan Nura, est&aacute; ocupado trabajando en la construcci&oacute;n de un mundo armonioso para los seres humanos y youkai. Un d&iacute;a, &eacute;l ve a Setsura molesta por lo que decide animarla tomando el clan para ir a disfrutar de las aguas termales &hellip;</div>
    </div>
    '''

    patron  = '<div class="aboxy_lista"[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img class="[^"]+" src="[^"]+" data-original="([^"]+)"[^<]+</a[^<]+'
    patron += '<span[^<]+</span[^<]+'
    patron += '<a[^>]+>([^<]+)</a.*?'
    patron += '<div class="sinopsis">(.*?)</div'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle
        fulltitle = title
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        show = title
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail , plot=plot , show=show, fulltitle=fulltitle, fanart=thumbnail, viewmode="movies_with_plot", folder=True) )

    patron = '<a href="([^"]+)">\&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            scrapedurl = urlparse.urljoin(item.url,match)
            scrapedtitle = ">> Pagina Siguiente"
            scrapedthumbnail = ""
            scrapedplot = ""

            itemlist.append( Item(channel=__channel__, action="series", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def episodios(item):
    logger.info("channels.zatetv episodios")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url, headers = ANIMEFLV_REQUEST_HEADERS)

    '''
    <div class="tit">Listado de episodios <span class="fecha_pr">Fecha Pr&oacute;ximo: 2013-06-11</span></div>
    <ul class="anime_episodios" id="listado_epis"><li><a href="/ver/aiura-9.html">Aiura 9</a></li><li><a href="/ver/aiura-8.html">Aiura 8</a></li><li><a href="/ver/aiura-7.html">Aiura 7</a></li><li><a href="/ver/aiura-6.html">Aiura 6</a></li><li><a href="/ver/aiura-5.html">Aiura 5</a></li><li><a href="/ver/aiura-4.html">Aiura 4</a></li><li><a href="/ver/aiura-3.html">Aiura 3</a></li><li><a href="/ver/aiura-2.html">Aiura 2</a></li><li><a href="/ver/aiura-1.html">Aiura 1</a></li></ul>
    '''

    # Saca enlaces a los episodios
    data = scrapertools.get_match(data,'<div class="tit">Listado de episodios.*?</div>(.*?)</ul>')
    patron = '<li><a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        try:
            episodio = scrapertools.get_match(scrapedtitle,item.show+"\s+(\d+)")
            if len(episodio)==1:
                title = "1x0"+episodio
            else:
                title = "1x"+episodio
        except:
            pass
        
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = item.thumbnail
        plot = item.plot
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , show=item.show, fulltitle=item.show+" "+title, fanart=thumbnail, viewmode="movies_with_plot", folder=True) )

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )
        itemlist.append( Item(channel=item.channel, title="Descargar todos los episodios de la serie", url=item.url, action="download_all_episodes", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("channels.zatetv findvideos")

    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<p id="zate_dir"[^>]+>([^<]+)</p>')
    logger.info("data="+data)

    '''
    ?mirror_vidbux=g3xsjixme9if&
    mirror_billionuploads=o41yimeb6ezt&
    mirror_180upload=ivawxzu5hfwz&
    mirror_videoshare=f0nk2pn55imm&
    mirror_uptobox=rc3tknpbnua9&
    movie_zombieuploadurl=http://www.zombieupload.com/files/mkyzKJU1391790063.html&
    langids=ES&
    videoid=32589&
    type=pelicula&fulldir=http://zate.tv/peliculas/the-secret-life-of-walter-mitty
    '''
    '''
    ?mirror_180upload=90hpwe6y7459&mirror_billionuploads=qov2b6hpmaa3&mirror_hugefiles=jtov2oj7fe5c&mirror_bayfiles=&
    mirror_videoshare=4bm2tq8eepo6&mirror_uptobox=ib45mflhpyic&mirror_vidbux=vvadis5mvi1w&movie_zombieuploadurl=http://www.zombieupload.com/files/92Sias1392914055.html&langids=ES&videoid=32790&type=pelicula&fulldir=http://zate.tv/peliculas/1</p>
    '''
    data = data.replace("mirror_vidbux="," http://www.vidbux.com/")
    data = data.replace("mirror_billionuploads="," ")
    data = data.replace("mirror_180upload="," http://180upload.com/")
    data = data.replace("mirror_videoshare="," ")
    data = data.replace("mirror_uptobox="," http://uptobox.com/")
    data = data.replace("mirror_hugefiles="," http://www.hugefiles.net/")
    data = data.replace("mirror_bayfiles="," http://bayfiles.net/file/")

    itemlist=[]
    logger.info("data="+data)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

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
        mirrors = findvideos(episodio_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien
