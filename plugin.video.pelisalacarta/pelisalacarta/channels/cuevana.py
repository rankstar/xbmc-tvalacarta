# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cuevana"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Cuevana"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cuevana.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"  , action="peliculas", url="http://www.cuevana.tv/web/peliculas?&todas"))
    itemlist.append( Item(channel=__channel__, title="Series"     , action="seriesMenu", url="http://www.cuevana.tv/web/series?&todas"))
    itemlist.append( Item(channel=__channel__, title="Buscar"     , action="search") )
    
    return itemlist
    
def seriesMenu(item):
    logger.info("[cuevana.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=__channel__, title="Lista Completa"  , action="series", url="http://www.cuevana.tv/web/series?&todas"))
    #itemlist.append( Item(channel=__channel__, title="Populares"  , action="series", url="http://www.cuevana.tv/web/series?&populares"))
    #itemlist.append( Item(channel=__channel__, title="Ranking"  , action="series", url="http://www.cuevana.tv/web/series?&ranking"))

    return itemlist
    

def peliculas(item):
    logger.info("[cuevana.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=__channel__, title="Lista Completa"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&todas"))
    itemlist.append( Item(channel=__channel__, title="Recientes"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&recientes"))
    itemlist.append( Item(channel=__channel__, title="Estrenos"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&estrenos"))
    itemlist.append( Item(channel=__channel__, title="Populares"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&populares"))
    itemlist.append( Item(channel=__channel__, title="Ranking"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&ranking"))
    itemlist.append( Item(channel=__channel__, title="HD"  , action="novedades", url="http://www.cuevana.tv/web/peliculas?&hd"))
#    itemlist.append( Item(channel=__channel__, title="Por Género"     , action="porGenero",    url="http://www.cuevana.tv/peliculas/genero/"))
#    itemlist.append( Item(channel=__channel__, title="Listado Alfabético"     , action="listadoAlfabetico",    url="http://www.cuevana.tv/peliculas/lista/"))	

    return itemlist

def porGenero(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Acción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=5"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Animación",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=7"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Aventura",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=14"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Bélica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=19"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Ciencia Ficción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=6"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Cine Negro",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=23"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=2"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia Dramática",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=27"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=15"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia Negra",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=26"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia Romántica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=16"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Comedia Stand Up",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=24"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Crimen",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=18"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Deporte",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=20"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Documental",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=10"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Dogma",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=22"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Drama",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=1"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Fantasía",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=13"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Humor",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=12"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Infantil",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=8"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Intriga",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=25"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=11"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Romance",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=9"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Suspenso",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=3"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Terror",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=4"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Thriller",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=17"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Western",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=21"))

    return itemlist	

def listadoAlfabetico(item):
    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="0-9",url="http://www.cuevana.tv/peliculas/lista/letra=num"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="A",url="http://www.cuevana.tv/peliculas/lista/letra=a"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="B",url="http://www.cuevana.tv/peliculas/lista/letra=b"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="C",url="http://www.cuevana.tv/peliculas/lista/letra=c"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="D",url="http://www.cuevana.tv/peliculas/lista/letra=d"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="E",url="http://www.cuevana.tv/peliculas/lista/letra=e"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="F",url="http://www.cuevana.tv/peliculas/lista/letra=f"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="G",url="http://www.cuevana.tv/peliculas/lista/letra=g"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="H",url="http://www.cuevana.tv/peliculas/lista/letra=h"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="I",url="http://www.cuevana.tv/peliculas/lista/letra=i"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="J",url="http://www.cuevana.tv/peliculas/lista/letra=j"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="K",url="http://www.cuevana.tv/peliculas/lista/letra=k"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="L",url="http://www.cuevana.tv/peliculas/lista/letra=l"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="M",url="http://www.cuevana.tv/peliculas/lista/letra=m"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="N",url="http://www.cuevana.tv/peliculas/lista/letra=n"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="O",url="http://www.cuevana.tv/peliculas/lista/letra=o"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="P",url="http://www.cuevana.tv/peliculas/lista/letra=p"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Q",url="http://www.cuevana.tv/peliculas/lista/letra=q"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="R",url="http://www.cuevana.tv/peliculas/lista/letra=r"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="S",url="http://www.cuevana.tv/peliculas/lista/letra=s"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="T",url="http://www.cuevana.tv/peliculas/lista/letra=t"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="U",url="http://www.cuevana.tv/peliculas/lista/letra=u"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="V",url="http://www.cuevana.tv/peliculas/lista/letra=v"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="W",url="http://www.cuevana.tv/peliculas/lista/letra=w"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="X",url="http://www.cuevana.tv/peliculas/lista/letra=x"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Y",url="http://www.cuevana.tv/peliculas/lista/letra=y"))
    itemlist.append( Item(channel=__channel__ , action="novedades" , title="Z",url="http://www.cuevana.tv/peliculas/lista/letra=z"))

    return itemlist

def novedades(item):
    logger.info("[cuevana.py] novedades")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas
    patron  = '<a href="([^"]+)">[^<]+'
    patron += '<div class="img"><img src="([^"]+)".*?'
    patron += '<div class="box">[^<]+'
    patron += '<div class="rate"><span[^<]+</span></div>[^<]+'
    patron += '<div class="tit">(.*?)</div>[^<]+'
    patron += '<div class="ano">([^<]+)</div>[^<]+'
    patron += '<div class="txt">(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,thumbnail,tit,anyo,plot in matches:
        scrapedtitle = scrapertools.htmlclean(tit).replace("Indexada","")
        scrapedplot = anyo+" "+plot        
        # url es "#!/peliculas/4437/mammuth"
        scrapedurl = re.compile('peliculas/([^/]+)',re.DOTALL).findall(url)[0]
        scrapedthumbnail = thumbnail
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, viewmode="movie_with_plot") )

    # Paginación
    # Enlace: <span class="actual">1</span><a href="page:2">
    # URL: http://www.cuevana.tv/#!/peliculas/page:2
    # Página 1: http://www.cuevana.tv/web/peliculas?&estrenos
    # Página 2: http://www.cuevana.tv/web/peliculas?&estrenos&page=2
    patron  = '<span class="actual">[^<]+</span><a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        parametro = matches[0].replace(":","=")
        if "page=" in item.url:
            baseurl = re.compile('(http\://.*?)\&page=',re.DOTALL).findall(item.url)[0]
        else:
            baseurl = item.url
        scrapedurl = baseurl + "&"+parametro
        logger.info("[cuevana.py] Página siguiente: "+scrapedurl)
        itemlist.append( Item(channel=__channel__, action="novedades", title="Página siguiente >>" , url=scrapedurl) )

    return itemlist

def series(item):
    logger.info("[cuevana.py] series")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    patron  = '<a href="([^"]+)">[^<]+'
    patron += '<div class="img"><img src="([^"]+)" /></div>[^<]+'
    patron += '<div class="box">[^<]+'
    patron += '<div class="rate"><span[^<]+</span></div>[^<]+'
    patron += '<div class="tit">([^>]+)</div>[^<]+'
    patron += '<div class="ano">([^<]+)</div>[^<]+'
    patron += '<div class="txt">(.*?)</div>[^<]+'
    patron += '<div class="in">(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,thumbnail,tit,anyo,plot,plot2 in matches:
        scrapedtitle = tit
        scrapedplot = anyo+" "+plot+" "+plot2
        scrapedurl = get_serie_url(url)
        scrapedthumbnail = thumbnail
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)

        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle, viewmode="movie_with_plot") )

    # Paginación
    # Enlace: <span class="actual">1</span><a href="page:2">
    # URL: http://www.cuevana.tv/web/series?&todas&page=2
    patron  = '<span class="actual">[^<]+</span><a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        parametro = matches[0].replace(":","=")
        scrapedurl = "http://www.cuevana.tv/web/series?&todas&"+parametro
        itemlist.append( Item(channel=__channel__, action="series", title="Página siguiente >>" , url=scrapedurl) )

    return itemlist

def get_serie_url(url):
    # url es "#!/series/3478/american-dad"
    # o "#!\\/series\\/4446\\/alcatraz"
    logger.info("get_serie_url(url=["+url+"]")
    scrapedurl = url.replace("\\","")
    logger.info("get_serie_url(url=["+scrapedurl+"]")
    scrapedurl = scrapedurl.replace("\\","")
    logger.info("get_serie_url(url=["+scrapedurl+"]")
    
    # el destino es "http://www.cuevana.tv/web/series?&3478&american-dad"
    
    #   #!/series/3478/american-dad
    scrapedurl = scrapedurl.replace("/","&")
    #   !&series&3478&american-dad

    scrapedurl = scrapedurl.replace("#!&series","http://www.cuevana.tv/web/series?")
    #   http://www.cuevana.tv/web/series?&3478&american-dad
    return scrapedurl

def episodios(item):
    logger.info("[cuevana.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae el argumento
    patron  = '<div class="txt">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = matches[0]

    data = data.replace("\\","")
    patron = "serieList\(\{l\:(.*?)\,e\:\$\('\#episodios'\)\}\)\;"
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    logger.info("data="+data)
    
    import simplejson as json
    seasons = json.loads(data)
    
    for season_id in seasons:
        print seasons[season_id]
        
        for episode in seasons[season_id]:
            num = episode["num"]
            if len(num)==1: num="0"+num
            scrapedtitle = "%sx%s %s" % (season_id,num,episode["tit"])
            if episode["hd"]=="1":
                scrapedtitle = scrapedtitle + " (HD)"
            scrapedplot = item.plot
            scrapedurl = episode["id"]
            scrapedthumbnail = item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+item.show)
    
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, fulltitle=item.fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.show , context="4", extra="serie") )

    itemlist = sorted(itemlist, key=lambda item: item.title)

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[cuevana.py] findvideos")

    id = item.url
    try:
        logger.info(item.extra)
        tipo=item.extra
    except:
        tipo=""
    
    if tipo=="":
        if item.category=="Series":
            tipo="serie"
        else:
            tipo="pelicula"

    if tipo=="pelicula":
        pathSubtitle="http://sc.cuevana.tv/files/sub/"
    else:
        pathSubtitle="http://sc.cuevana.tv/files/s/sub/"

    # Obtiene las fuentes compatibles
    '''
    var sources = {"720":{"2":["megaupload","glumbo","wupload"]},"360":{"2":["megaupload","glumbo","wupload"]}}, sel_source = 0;
    var label = {
        '360': 'SD (360p)',
        '480': 'SD (480p)',
        '720': 'HD (720p)',
        '1080': 'HD (1080p)'
    };
    
    var labeli = {"1":"Espa\u00f1ol","2":"Ingl\u00e9s","3":"Portugu\u00e9s","4":"Alem\u00e1n","5":"Franc\u00e9s","6":"Coreano","7":"Italiano","8":"Tailand\u00e9s","9":"Ruso","10":"Mongol","11":"Polaco","12":"Esloveno","13":"Sueco","14":"Griego","15":"Canton\u00e9s","16":"Japon\u00e9s","17":"Dan\u00e9s","18":"Neerland\u00e9s","19":"Hebreo","20":"Serbio","21":"\u00c1rabe","22":"Hindi","23":"Noruego","24":"Turco","26":"Mandar\u00edn","27":"Nepal\u00e9s","28":"Rumano","29":"Iran\u00ed","30":"Est\u00f3n","31":"Bosnio","32":"Checo","33":"Croata","34":"Fin\u00e9s","35":"H\u00fanagro"};
    var labelh = {
        'megaupload': 'Megaupload',
        'glumbo': 'Glumbo',
        'filepost': 'Filepost',
        'wupload': 'Wupload'
    };
    '''
    url = "http://www.cuevana.tv/player/sources?id="+id+"&tipo="+tipo

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:11.0) Gecko/20100101 Firefox/11.0"])
    headers.append(["Referer","http://www.cuevana.tv/"])
    data = scrapertools.cache_page(url,headers=headers)
    logger.info("data="+data)
    
    # Fuentes
    patron = 'var sources \= (.*?)\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    cadena = matches[0].replace(", sel_source = 0","")
    import simplejson as json
    sources = json.loads(cadena)

    # Calidades
    patron = 'var label \= (.*?)\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    cadena = matches[0]
    cadena = re.compile("\s+",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("'",'"')

    import simplejson as json
    qualities = json.loads(cadena)
    logger.info("qualities="+str(qualities))

    # Idiomas
    language_labels = {}
    language_labels["1"]="Espanol"
    language_labels["2"]="Ingles"
    language_labels["3"]="Portugues"
    language_labels["4"]="Aleman"
    language_labels["5"]="Frances"
    language_labels["6"]="Coreano"
    language_labels["7"]="Italiano"
    language_labels["8"]="Tailandes"
    language_labels["9"]="Ruso"
    language_labels["10"]="Mongol"
    language_labels["11"]="Polaco"

    # Presenta las opciones
    itemlist = []
    i=1
    
    '''
    for quality_id in sources:
        languages = sources[quality_id]

        for language_id in languages:
    '''

    for language_id in sources:
        logger.info("language_id="+str(language_id));
        qualitiesj = sources[language_id]
        
        for quality_id in qualitiesj:
            logger.info("quality_id="+str(quality_id));
            mirrors = sources[language_id][quality_id]

            for mirror in mirrors:
                logger.info("i=%d, mirror=%s, quality_id=%s, language_id=%s" % (i,mirror,str(quality_id),str(language_id)))
                titulo = "Opcion %d: %s %s (%s)" % (i, mirror , qualities[quality_id], language_labels[language_id])
                i=i+1
                url = "def=%s&audio=%s&host=%s&id=%s&tipo="+tipo
                url = url % (quality_id,language_id,mirror,id)
                
                subtitulo = pathSubtitle+id+"_ES.srt"
                
                itemlist.append( Item(channel=__channel__, action="play" , title=titulo, fulltitle=item.fulltitle , url=url, thumbnail=item.thumbnail, plot=item.plot, extra=id, subtitle=subtitulo, folder=False))

    return itemlist

def play(item):
    logger.info("[cuevana.py] play")
    url = "http://www.cuevana.tv/player/source_get"
    post = item.url
    id = item.extra
    headers = []
    headers.append( ["Host","www.cuevana.tv"])
    headers.append( ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0) Gecko/20100101 Firefox/8.0"])
    headers.append( ["Accept","*/*"])
    headers.append( ["Accept-Language","es-es,es;q=0.8,en-us;q=0.5,en;q=0.3"])
    headers.append( ["Accept-Encoding","gzip, deflate"])
    headers.append( ["Accept-Charset","ISO-8859-1,utf-8;q=0.7,*;q=0.7"])
    headers.append( ["Connection","keep-alive"])
    headers.append( ["Content-Type","application/x-www-form-urlencoded; charset=UTF-8"])
    headers.append( ["X-Requested-With","XMLHttpRequest"])
    headers.append( ["Referer","http://www.cuevana.tv/player/sources?id="+id+"&tipo=serie"])
    headers.append( ["Content-Length", len(post) ])
    headers.append( ["Pragma","no-cache"])
    headers.append( ["Cache-Control","no-cache"])

    data = scrapertools.cache_page(url=url, post=post)
    logger.info("data=#"+data+"#")
    patron = "recaptcha\/api\/challenge\?k\="
    matches = re.compile(patron).findall(data)
    if len(matches)>0:
        logger.info("[wupload.py] está pidiendo el captcha")
        recaptcha_key = get_match( data , 'recaptcha\/api\/challenge\?k\=([^&]+)')
        logger.info("[wupload.py] recaptcha_key="+recaptcha_key)
    
        data_recaptcha = scrapertools.cache_page("http://www.google.com/recaptcha/api/challenge?k="+recaptcha_key)
        patron="challenge.*?'([^']+)'"
        challenges = re.compile(patron, re.S).findall(data_recaptcha)
        if(len(challenges)>0):
            challenge = challenges[0]
            image = "http://www.google.com/recaptcha/api/image?c="+challenge
            
            #CAPTCHA
            exec "import pelisalacarta.captcha as plugin"
            tbd = plugin.Keyboard("","",image)
            tbd.doModal()
            confirmed = tbd.isConfirmed()
            if (confirmed):
               tecleado = tbd.getText()
            
            #logger.info("")
            #tecleado = raw_input('Grab ' + image + ' : ')
        url = url + "?" + post
        post = "recaptcha_challenge_field=%s&recaptcha_response_field=%s" % (challenge,tecleado.replace(" ","+"))
        location = scrapertools.get_header_from_response( url=url, header_to_get="location", post=post)
        location = urllib.unquote_plus(location)
        logger.info("ANDRES location="+location)
    else:
        logger.info("[wupload.py] no encontrado captcha")
        location = data.replace("%3A",":").replace("%2F","/")
    
    itemlist = servertools.find_video_items(data=location)
    for returnitem in itemlist:
        returnitem.channel=item.channel
        returnitem.subtitle=item.subtitle

    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto, categoria="*"):
    logger.info("[cuevana.py] search")
    
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.cuevana.tv/web/buscar?&q="+texto
    
        # Descarga la pagina
        data = scrapertools.cache_page(item.url)

        # Extrae las entradas
        patron = '\[(.*?)\]'
        matches = re.compile(patron,re.DOTALL).findall(data)
        #scrapertools.printMatches(matches)
        data = matches[ len(matches)-2 ]
        logger.info("data="+data)
    
        #Listar
        itemlist = []
        patron = '"id":"([^"]+)","url":"([^"]+)","tit":"([^"]+)","duracion":"([^"]+)","txt":"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for id,url,tit,duracion,txt in matches:
            scrapedtitle = tit
            scrapedurl = id
            scrapedthumbnail = "http://sc.cuevana.tv/box/"+id+".jpg"
            scrapedplot = txt
            if "peliculas" in url:
                itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )
            else:
                scrapedurl = get_serie_url(url)
                itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle) )

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def listar(item, categoria="*"):
    logger.info("[cuevana.py] listar")

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    patronvideos  = "<div class='result'>[^<]+"
    patronvideos += "<div class='right'><div class='tit'><a href='([^']+)'>([^<]+)</a>"
    patronvideos += ".*?<div class='txt'>([^<]+)<div class='reparto'>.*?"
    patronvideos += "<div class='img'>.*?<img src='([^']+)'[^>]+></a>"


    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = match[2]
        scrapedurl = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[0])
        scrapedthumbnail = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        ## <-- Trata diferenciadamente a las series y usa filtro de categoria para búsquedas generales
        if "tv/series/" in scrapedurl and categoria in ("S","*"):
           code = re.compile("/series/([0-9]+)/").findall(scrapedurl)[0]
           scrapedurl = "http://www.cuevana.tv/list_search_id.php?serie="+code
           itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , extra=code, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )
        elif "tv/peliculas/" in scrapedurl and categoria in ("F","*"):
           itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="listar", title="Página siguiente" , url=scrapedurl) )

    return itemlist

def get_match(data, regex) :
    match = "";
    m = re.search(regex, data)
    if m != None :
        match = m.group(1)
    return match

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())
    peliculas_items = peliculas(mainlist_items[0])

    # Comprueba primero las películas "Recientes" a ver si alguna tiene mirrors
    novedades_items = novedades(peliculas_items[1])
    
    bien = False
    for pelicula_item in novedades_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break
    
    if not bien:
        return bien

    # Comprueba luego las series
    seriesmenu_items = seriesMenu(mainlist_items[1])
    series_items = series(seriesmenu_items[0])
    episodios_items = episodios(series_items[0])
    bien = False
    for episodio_item in episodios_items:
        mirrors = findvideos(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien
