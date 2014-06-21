# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series.ly
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import os
import urllib2


from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriesly"
__category__ = "F,S,A,D"
__type__ = "generic"
__title__ = "Series.ly"
__language__ = "ES"
__creationdate__ = "20111119"

DEBUG = config.get_setting("debug")


try:
    import xbmcgui
    isxbmc=True
except:
    isxbmc=False


def isGeneric():
    return True

"""Handler para library_service"""
def episodios(item):
    # Obtiene de nuevo los tokens
    episode_list = serie_capitulos(item)
    for episode in episode_list:
        episode.extra = item.extra
    return episode_list

"""Handler para launcher (library)"""
def findvideos(item):
    return multiple_links(item)

"""Handler para launcher (library)"""
def play(item):
    return links(item)

def mainlist(item):
    logger.info("[seriesly.py] mainlist")
   
    itemlist = []

    if config.get_setting("serieslyaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title="Habilita tu cuenta en la configuración..." , action="openconfig" , url="" , folder=False ) )
    else:
        auth_token, user_token = getCredentials()
       
        if user_token:
           
            extra_params = '%s|%s' % ( auth_token, user_token )

            itemlist.append( Item(channel=__channel__, title="Buscar", action="search") )
            itemlist.append( Item(channel=__channel__, title="Mis series", action="categorias", extra=extra_params, url="series" ) )
            itemlist.append( Item(channel=__channel__, title="Mis pelis", action="categorias", extra=extra_params, url="movies" ) )
            itemlist.append( Item(channel=__channel__, title="Mis documentales", action="categorias", extra=extra_params, url="documentaries" ) )
            itemlist.append( Item(channel=__channel__, title="Mis tvshows", action="categorias", extra=extra_params, url="tvshows" ) )
            itemlist.append( Item(channel=__channel__, title="Mis listas", action="listasMenu", extra=extra_params, url="listas" ) )
            if isxbmc: itemlist.append( Item(channel=__channel__, title="Explora series.ly", action="exploraMenu", url="explora" ) )
            

        else:
            itemlist.append( Item( channel=__channel__ , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )

    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []

def getCredentials():
          
    auth_token,user_token = perform_login()
   
    return [auth_token,user_token]

def categorias(item):
   
    itemlist = []
    if item.url=="movies": 
        itemlist.append( Item(channel=__channel__, title="Vistas", action="categoria", url='Vistas', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Favoritas", action="categoria", url='Favouritas', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Pendientes", action="categoria", url='Pendientes', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Peliculas Mas Vistas", action="mas_vistas", url=item.url ) )
        itemlist.append( Item(channel=__channel__, title="Peliculas Por Categorias", action="menu_cat", url=item.url, extra="cat" ) )
        
   
    elif item.url=="series":
        itemlist.append( Item(channel=__channel__, title="Viendo", action="categoria", url='Viendo', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Finalizadas", action="categoria", url='Finalizada', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Pendientes", action="categoria", url='Pendiente', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Series Mas Vistas", action="mas_vistas" , url=item.url ) )
        itemlist.append( Item(channel=__channel__, title="Series Por Categorias", action="menu_cat", url=item.url, extra="cat" ) )
        
    elif item.url=="documentaries":
        itemlist.append( Item(channel=__channel__, title="Vistos", action="categoria", url='Vistas', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Favoritas", action="categoria", url='Favoritas', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Pendientes", action="categoria", url='Pendientes', extra=item.url) )
        itemlist.append( Item(channel=__channel__,title="Documentales mas vistos",action="mas_vistas",url=item.url))

    elif item.url=="tvshows":
        itemlist.append( Item(channel=__channel__, title="Viendo", action="categoria", url='Viendo', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Finalizadas", action="categoria", url='Finalizada', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Pendientes", action="categoria", url='Pendiente', extra=item.url) )
        itemlist.append( Item(channel=__channel__, title="Tvshows Mas Vistos", action="mas_vistas" , url=item.url ) )
        itemlist.append( Item(channel=__channel__, title="Tvshows Por Categorias", action="menu_cat", url=item.url, extra="cat" ) )
        

    itemlist.append( Item(channel=__channel__, title="Buscar", action="search", url=item.url) )

    return itemlist

def menu_cat(item):

    itemlist=[]

    categorias=get_constant("categorias")

    for c in categorias:
        itemlist.append( Item(channel=__channel__, title=categorias[c], action="search_cat", category=c, url=item.url, plot="0") )

    itemlist = sorted( itemlist , key=lambda item: item.title)

    return itemlist

def categoria(item):

    logger.info("[seriesly.py] categoria")

    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
   
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )

    tipo=item.extra

    # Videos Usuario (Filtradas por categoria)
    url='http://api.series.ly/v2/user/media/%s'%tipo
    data = scrapertools.cache_page(url, post=post)
    List = load_json(data)

    if "error" in List:
        if List["error"]!=0:
            error_message(List["error"])
            return []
    else:
        return []


    if List[tipo] == None : List[tipo] = []   
    logger.info("hay %d %s" % (len(List[tipo]), tipo ))
   
    cat_filter = item.url

    itemlist = []
    default = '2'


    if tipo=="series" or tipo =="tvshows":
        if item.url == 'Pendiente' : cat_filter = 2
        elif item.url == 'Viendo' : cat_filter = 1
        elif item.url == 'Finalizada' : cat_filter = 3

    if tipo=="movies" or tipo=="documentaries":
        if item.url == 'Favouritas' : cat_filter = 2
        elif item.url == 'Vistas' : cat_filter = 1
        elif item.url == 'Pendientes' : cat_filter = 3

   
    for movieItem in List[tipo]:
            # Añade al listado de XBMC filtrando por categoria

            status = movieItem['status']           
            if status == cat_filter:

                itemlist.append( generate_item(movieItem, tipo, auth_token))
               

    itemlist = sorted( itemlist , key=lambda item: item.title)
    return itemlist

def serie_capitulos(item):
   
    logger.info('[seriesly.py] serie_capitulos')
   
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
   
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    serieInfo = load_json(scrapertools.cache_page(item.url, post=post))

    if "error" in serieInfo:
        if serieInfo["error"]!=0:
            error_message(serieInfo["error"])
            return []
    else:
        return []

    if serieInfo == None:
        serieInfo = {}

    if (not serieInfo.has_key('seasons_episodes')) or serieInfo['seasons_episodes'] == None:
        serieInfo['seasons_episodes'] = []
   
    # Juntamos todos los episodios con enlaces en una sola lista
    episodeList=[]
    for i in serieInfo["seasons_episodes"]:
        for j in serieInfo["seasons_episodes"][i]:
            if j['haveLinks']: episodeList.append(j)

    logger.info('[seriesly serie_capitulos]hay %d capitulos' % len(episodeList))

    itemlist = []
    for episode in episodeList:

        if episode.has_key('watched'):
            viewed = episode['watched']
            if viewed == False : episode['estado'] = ' [Pendiente]'
            elif viewed == True : episode['estado'] = ' [Visto]'
            else : episode['estado'] = ' [?]'
        else:
            episode['estado'] = ''

        # Añadimos un 0 al principo de la temporada y capitulo para su ordenacion
        episode["episode"] = str(episode["episode"])
        if len(episode["episode"])==1:
            episode["episode"]="0"+episode["episode"]

        episode["season"] = str(episode["season"])
        if len(episode["season"])==1:
            episode["season"]="0"+episode["season"]
       
        itemlist.append(
            Item(channel=__channel__,
                action = 'multiple_links',
                title = '%(season)sx%(episode)s %(title)s%(estado)s' % episode,
               
                url = 'http://api.series.ly/v2/media/episode/links?&idm=%(idm)s&mediaType=5' % episode,
                thumbnail = item.thumbnail,
                plot = "",
                show = item.show,
                extra = item.extra
               
            )
        )
   
    itemlist = sorted( itemlist , key=lambda item: item.title)

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel='seriesly', title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="serie_capitulos###", show=elimina_tildes(item.show)) )

    return itemlist

def elimina_tildes(s):
    import unicodedata
    nkfd_form = unicodedata.normalize('NFD', s.decode('utf-8'))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

def mas_vistas(item):

    logger.info("[seriesly.py] mas_vistas")
   
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
    post = 'auth_token=%s&user_token=%s&limit=100' % ( qstr(auth_token), qstr(user_token) )
   
    # Extrae las entradas (carpetas)
    tipo=item.url
    url="http://api.series.ly/v2/media/most_seen/"+tipo
    topInfo = load_json(scrapertools.cache_page(url, post=post))

    if "error" in topInfo:
        if topInfo["error"]!=0:
            error_message(topInfo["error"])
            return []
    else:
        return []

    if topInfo == None : topInfo = {}
    if topInfo[tipo] == None : topInfo[tipo] = []
   
    logger.info("hay %d videos" % len(topInfo[tipo]))
   
    itemlist = []
    for movieItem in topInfo[tipo]:
        # Añade al listado de XBMC
        itemlist.append( generate_item(movieItem, tipo, auth_token)) 
   
    return itemlist


def listasMenu(item):
    
   
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
   
    # Extrae las entradas (carpetas)
    url="http://api.series.ly/v2/user/media/lists"
    listasInfo = load_json(scrapertools.cache_page(url, post=post))
    
    
    ownList=[]
    followList=[]

    #generamos un dict para las listas propias y otro para las que seguimos

    if  len(listasInfo["own"]) >=1 :
        for lista in listasInfo["own"]:
            logger.info(str(lista))
            if "last_medias" in lista:
                
                ownList.append({"id_list":lista["id_list"],
                                "title": lista["title"],
                                "medias_num": lista["medias_num"] })


    if  len(listasInfo["following"]) >=1 :
        for lista in listasInfo["following"]:
            logger.info(str(lista))
            if "last_medias" in lista:
                followList.append({"id_list":lista["id_list"],
                                "title": lista["title"],
                                "medias_num": lista["medias_num"] })

    #creamos el menu y pasamos las listas en el campo extra para no tener que utilizar más cuota
    #Utilizo json.dump para pasar el dict para que me coja los acentos, si no desaparecían las listas

    import json

    itemlist=[]
    itemlist.append( Item(channel=__channel__, title="Propias", action="listas", url='Viendo', extra=json.dumps(ownList)) )
    itemlist.append( Item(channel=__channel__, title="Siguiendo", action="listas", url='Finalizada', extra=json.dumps(followList)) )

    return itemlist

def listas(item):
    logger.info("[seriesly.py] listas_vistas")

    import urllib
    import json

    d=urllib.unquote(item.extra)
    listaDict=load_json(d)

    itemlist=[]
    for element in listaDict:
        logger.info(element)
        title=element["title"]
        
        itemlist.append( Item(channel=__channel__, title=title, action="lista", url='Viendo', extra=json.dumps(element)) )
        
    return itemlist

def lista(item):

    import urllib
    import json

    d=urllib.unquote(item.extra)
    listaDict=load_json(str(d))
    

    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
    post = 'auth_token=%s&id_list=%s' % ( qstr(auth_token), qstr(listaDict["id_list"]) )
   
    # Extrae las entradas (carpetas)
    url="http://api.series.ly/v2/media/list"
    lista = load_json(scrapertools.cache_page(url, post=post))


    logger.info(str(lista))

    itemlist=[]
        
    for element in lista["list_info"]["medias"]:
        logger.info(str(element))
        video={ 'idm': element["idm"],
                'seasons': 0,
                'episodes':0,
                'poster':{"large":element["img"]},
                'name': element["name"],
                'mediaType':get_constant("mediaType")[int(element["mediaType"])],
                'auth_token':auth_token
            }
        itemlist.append(generate_item(video, video["mediaType"], auth_token))

              


    return itemlist


def generate_item(video , tipo, auth_token):
   
    logger.info('video')
    logger.info(str(video))
    
    if tipo == "None": return Item()
    if 'name' not in video: return Item()
   
    if tipo=="series" or tipo == "tvshows":  
        
        url = 'http://api.series.ly/v2/media/full_info?auth_token='+ auth_token+'&idm=%s&mediaType=%s' %(video["idm"],get_constant("mediaType")[tipo])
        #Si la serie no tiene temporada, al abrirla tampoco tiene capitulos
        if "seasons" not in video:
            return Item()

        if "seasons"==0: #por lo general este caso es cuando trabajamos con listas

            action = 'serie_capitulos'
            title = '%(name)s Serie' % video

        else:
            action = 'serie_capitulos'
            title = '%(name)s (%(seasons)d Temporadas) (%(episodes)d Episodios)' % video

    elif tipo =="movies" or tipo == "documentaries":
                url = 'http://api.series.ly/v2/media/episode/links?auth_token='+ auth_token+'&idm=%s&mediaType=%s' %(video["idm"],get_constant("mediaType")[tipo])
                if "year" not in video: video["year"]= ""
                title = '%(name)s (%(year)s)' % video
                action= 'multiple_links'

   

    if "plot_es" not in video : video["plot_es"]= " "

    logger.info(action)
    item=Item(channel=__channel__,
                 action = action,
                 title = title,
                 url = url,
                 thumbnail = video['poster']["large"],
                 plot = video["plot_es"],
                 show = video['name'],
                 extra = ""
            )

    logger.info(item.title)
    return item

def multiple_links(item):
    logger.info("[seriesly.py] multiple_links")
   
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
   
    # Extrae las entradas (carpetas)
    post = 'auth_token=%s&user_token=%s' % ( qstr(auth_token), qstr(user_token) )
    data = scrapertools.cache_page(item.url+"&"+post)
    linkList = load_json(data)

    if "error" in linkList:
        if linkList["error"]!=0:
            error_message(linkList["error"])
            return []
    else:
        return []
   
    if linkList == None : linkList = []
   
    logger.info("hay %d videos" % len(linkList))
   
    tipoList=["streaming","direct_download"]
    itemlist = [] 

    for tipo in tipoList:
       
        if tipo in linkList:
            for link in linkList[tipo]:
                if "quality" not in link:
                    link["quality"]= ""
		
		if "features" not in link:
		    link["features"]= ""

                if link['subtitles']!="":
                    linktitle = '%(host)s - %(lang)s (sub %(subtitles)s) %(quality)s %(features)s' % link
                else:
                    linktitle = '%(host)s - %(lang)s %(quality)s %(features)s' % link

                itemlist.append(
                    Item(channel=__channel__,
                        action = "links",
                        title = linktitle, 
                        url = link['video_url']+"?"+post,
                        thumbnail = item.thumbnail,
                        plot = "",
                        extra=link["date_created"]
                    )
                )

   
    return itemlist

def links(item):   
       
    itemlist = []
    try:
        count = 0
        exit = False
        while(not exit and count < 5):
            #A veces da error al intentar acceder
            try:
                logger.info(str(item.url))
                page = urllib2.urlopen(item.url)
                urlvideo = "\"" + page.geturl() + "\""
                logger.info(str(page.read()))
                logger.info(item.url)
                exit = True
            except:
                import traceback
                logger.info(traceback.format_exc())
                count = count + 1
       

        logger.info("urlvideo="+urlvideo)
        for video in servertools.findvideos(urlvideo) :
            #scrapedtitle = title.strip() + " " + match[1] + " " + match[2] + " " + video[0]
            scrapedtitle = scrapertools.htmlclean(video[0])
            scrapedurl = video[1]
            server = video[2]
            itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle, url=scrapedurl, thumbnail=item.thumbnail, plot="", server=server, extra="", category=item.category, fanart=item.thumbnail, folder=False))
    except: 
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
               
       
    return itemlist

def search_cat(item):
    
    filters=None
    
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
    post = 'auth_token=%s' % ( qstr(auth_token) )
    logger.info(str(item.url))

    
    #busqueda general
    url="http://api.series.ly/v2/media/browse"
    post="auth_token="+auth_token

    
    if item.extra =="":

        post=post+"&order=most_viewed"

        #busquda por tipo
        if item.url != "" :
            mediaType=get_constant("mediaType")[item.url]
            post=post+"&mediaType=%s" % mediaType

        #busqueda por genero
        if item.category != "":
            post=post+"&genre="+item.category

    else:
        logger.info("item.extra")
        logger.info(item.extra)

        filters=load_json(item.extra)
        post=post+"&mediaType=%(mediaType)s&genre=%(genre)s&min_year=%(min_year)s&max_year=%(max_year)s&order=%(order)s&limit=%(limit)s" % filters 


    #paginacion
    if item.plot != "":
        post=post+"&page="+item.plot
        plot=int(item.plot)+1
        item.plot=str(plot)
   
    # Extrae las entradas (carpetas)
    serieList = load_json(scrapertools.cache_page(url, post))
    

    if "error" in serieList:
        if serieList["error"]!=0:
            error_message(serieList["error"])
            return []
    else:
        return []
   

    if serieList == None : serieList = []
   
    logger.info("hay %d series" % len(serieList))
   
    itemlist = []
    for serieItem in serieList['results']["medias"]:
        logger.info(str(serieItem))
        
        tipo=get_constant("mediaType")[serieItem["mediaType"]]
       
       
        itemlist.append(generate_item(serieItem, tipo, auth_token))
        
         
    
    #Añadimos Pagina Siguiente
    if len(itemlist)>0:


        item= Item(channel=__channel__, title="Pagina Siguiente", action="search_cat", category=item.category, url=item.url, plot=item.plot )

        if filters is not None:

            import json
            item.extra=json.dumps(filters)

        itemlist.append(item)
        
    logger.info(str(itemlist))
    return itemlist


def exploraMenu(item):
    filters=get_default_filters()

    itemlist=[]

    itemlist.append( Item(channel=__channel__, title="Explorar" %filters  , action="browse"))

    tipo=["Todos","Series","Peliculas",  "Documentales", "Tvshows" ]
    itemlist.append( Item(channel=__channel__, title="Tipo: %s" %tipo[filters["mediaType"]]  , action="change_filter", extra="tipo" ))

    itemlist.append( Item(channel=__channel__, title="Genero: %s" %get_constant("categorias")[filters["genre"]]  , action="change_filter", extra="genre" ))

    orden=["Mas nuevo", "Mas viejo", "Puntuacion", "Mas visto", "Trending"]
    order=[ 'newest', 'oldest', 'rating', 'most_viewed', 'trending']    
    itemlist.append( Item(channel=__channel__, title="Orden: %s" %orden[order.index(filters["order"])]  , action="change_filter", extra="order" ))

    itemlist.append( Item(channel=__channel__, title="Año mínimo: %(min_year)s" %filters  , action="change_filter", extra="min_year" ))
    itemlist.append( Item(channel=__channel__, title="Año máximo: %(max_year)s" %filters  , action="change_filter", extra="max_year" ))
    itemlist.append( Item(channel=__channel__, title="Nº de Resultados: %(limit)s" %filters  , action="change_filter", extra="limits" ))

    return itemlist

def change_filter(item):
    

    filters=get_default_filters()
    dialog=xbmcgui.Dialog()

    if item.extra=="order":
        orden=["Mas nuevo", "Mas viejo", "Puntuacion", "Mas visto", "Trending"]
        order=[ 'newest', 'oldest', 'rating', 'most_viewed', 'trending']
        filters["order"]=order[dialog.select("Selecciona el orden",orden)]

    if item.extra == "min_year":
        filters["min_year"]=dialog.numeric(0, "Selecciona el año de partida", str(filters["min_year"]))

    if item.extra == "max_year":
        filters["max_year"]=dialog.numeric(0, "Selecciona el año Final",str(filters["max_year"]))

    if item.extra== "limits":
        limites=["10", "24", "48"]
        limits=[10,24,48]
        filters["limit"]=limits[dialog.select("Resultados por Pagina",limites)]

    if item.extra=="tipo":
        tipo=["Todos","Series","Peliculas",  "Documentales", "Tvshows" ]
        filters["mediaType"]=dialog.select("Selecciona el Tipo",tipo)

    if item.extra=="genre":
        cat=[]
        genre=[]
        categorias=get_constant("categorias")

        for c in sorted(categorias,key=categorias.get):
            cat.append(categorias[c])
            genre.append(c)
    
        filters["genre"]=genre[dialog.select("Selecciona el Genero",cat)]


    import json
    path=config.get_data_path()
    f =open(path+"seriesly.default.json", "w+")
    json.dump(filters,f)
    f.close()

    return exploraMenu(Item(channel=__channel__, title="Explora series.ly", action="exploraMenu", url="explora" ))


def browse(item):

    filters=get_default_filters()
    import json
    return search_cat(Item(channel=__channel__, extra=json.dumps(filters), plot="0"))

   

def search(item,texto="", categoria="*"):

   
    item.channel="seriesly"
    res = search_videos(item, texto)
   
   
    return res

def search_videos(item, texto=None):
    logger.info("[seriesly.py] search")
   
    # Obtiene de nuevo los tokens
    auth_token, user_token = getCredentials()
    post = 'auth_token=%s' % ( qstr(auth_token) )
    logger.info(str(item.url))

    #Añadido por culpa del if de la paginacion
    if texto is None:
        query=""
    else:
        query=texto

    #busqueda general
    url="http://api.series.ly/v2/search"
    post="auth_token="+auth_token+"&q="+query

    

    #busquda por tipo
    if item.url != "" :
        mediaType=get_constant("mediaType")[item.url]
        post=post+"&filter=%s" % mediaType

   

    #paginacion
    if item.plot != "":
        post=post+"&page="+item.plot
        plot=int(item.plot)+1
        item.plot=str(plot)
   
    # Extrae las entradas (carpetas)
    serieList = load_json(scrapertools.cache_page(url, post))
    

    if "error" in serieList:
        if serieList["error"]!=0:
            error_message(serieList["error"])
            return []
    else:
        return []
   

    if serieList == None : serieList = []
   
    logger.info("hay %d series" % len(serieList))
   
    #return get_search_list(serieList)


    itemlist = []
    for serieItem in serieList['response']['results']:
        logger.info(str(serieItem))

        if "mediaType" in serieItem["object"]:
        
            tipo=get_constant("mediaType")[serieItem['object']["mediaType"]]
       
       
            itemlist.append(generate_item(serieItem['object'], tipo, auth_token))
         
    
    #Añadimos Pagina Siguiente
    if texto is None:
        itemlist.append( Item(channel=__channel__, title="Pagina Siguiente", action="search_videos", extra=item.extra, url=item.url, plot=item.plot ))

    return itemlist




def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        
        rdct = {}
        for k, v in dct.items() :
            
        
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        
        return rdct

    try:
        import json
    except:
        try:
            import simplejson as json
        except:
            from lib import simplejson as json

    try :       
        json_data = json.loads(data, object_hook=to_utf8)
        return json_data
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

''' URLEncode a string '''
def qstr(string):
    return string # urllib2.quote(string)   

def perform_login():

        auth_token,user_token=check_token()

        """url="http://api.series.ly/v2/app/show_quota"
        post="auth_token=%s&user_token=%s"%(auth_token,user_token)
        logger.info(url)
        data = scrapertools.cache_page(url,post=post)
        logger.info("****")
        logger.info(data)
        logger.info("****")"""

        if not auth_token or not user_token :
   
            auth_token=generate_authtoken()

            user_token=generate_usertoken(auth_token)
            if not user_token:
                return [auth_token,user_token]
       
       
        logger.info("****")
        logger.info(auth_token)
        logger.info("****")
        logger.info(user_token)
        logger.info("****")

        url="http://api.series.ly/v2/app/show_quota"
        post="auth_token=%s&user_token=%s"%(user_token,auth_token)
                   
        return [auth_token,user_token]

def generate_authtoken():


        url = "http://api.series.ly/v2/auth_token/"
        #post='id_api=1363&secret=zHX3TPEW2tvZRFneAAU7'
        post='id_api=8&secret=N5X54c4OeDUwU8dWBbMW'
        data = scrapertools.cache_page(url,post=post)
        logger.info("****")
        logger.info(data)
        logger.info("****")
       
        auth_data= load_json(data)

        if "error" in auth_data:
            if auth_data["error"]!=0:
                error_message(auth_data["error"])
                return False
        else:
            return False


        auth_token = auth_data["auth_token"]

        path=config.get_data_path()
        f =open(path+"seriesly_auth", "w+")
        f.write(str(data+";"))
        f.close()

       
        return auth_token

def generate_usertoken(auth_token):

       
        LOGIN = config.get_setting("serieslyuser")
        PASSWORD = config.get_setting("serieslypassword")

        url = "http://api.series.ly/v2/user/user_token"
        post = "auth_token=%s&username=%s&password=%s&remember=1&user_agent=''" % ( auth_token, qstr(LOGIN), qstr(PASSWORD) )
        data = scrapertools.cache_page(url,post=post)
        logger.info("****")
        logger.info(data)
        logger.info("****")
       
        user_data=load_json(data)


        if "error" in user_data:
            if user_data["error"]!=0:
                error_message(user_data["error"])
                return False
        else:
            return False

        path=config.get_data_path()
        logger.info(path)
        f =open(path+"seriesly_auth", "a")
        f.write(str(data))
        logger.info(str(data))
        f.close()

        user_token=user_data["user_token"]

        return user_token


def check_token():

   
    path=config.get_data_path()
    try:
        f =open(path+"seriesly_auth", "r")
        data= f.read()
        f.close()
    
        auth, user=data.split(";")
        
        logger.info(data)

        auth = load_json(auth)
        user = load_json(user)

        import time
        t=time.time()
        logger.info(str(auth["auth_expires_date"]-t))
        if auth["auth_expires_date"]>t and user["user_expires_date"]>t:
            return auth["auth_token"], user["user_token"]
    except:
        pass
    return False, False 


def get_constant(texto):

    constants={}

    constants["categorias"]={   "action":       "Acción",
                                "comedy":       "Comedia",
                                "family":       "Familiar",
                                "history":      "Histórico",
                                "mystery":      "Misterio",
                                "sci-fi":          "Ciencia Ficción",
                                "war":          "Guerra",
                                "adventure":    "Aventura",
                                "crime":        "Crimen",
                                "fantasy":      "Fantasía",
                                "horror":       "Horror",
                                "news":         "Actualidad",
                                "sport":        "Deportes",
                                "western":      "Western",
                                "animation":    "Animación",
                                "documentary":  "Documental",
                                "film-noir":    "Cine Negro",
                                "music":        "Música",
                                "drama":        "Drama",
                                "musical":      "Musical",
                                "romance":      "Romance",
                                "thriller":     "Thriller",
                                "reallity":     "Reallity Show"}

    constants["mediaType"]= {1:"series",
                            2:"movies",
                            3:"documentaries",
                            4:"tvshows",
                            5:"episode",
                            "series":1,
                            "movies":2,
                            "documentaries":3,
                            "tvshows":4,
                            "episode":5,
                            "": "None",
                            "None": "" }

    constants["error"]= {    "0":"Success response code",
                            "1":"INVALID_AUTH_TOKEN",
                            "2":"EMPTY_API_OR_SECRET",
                            "3":"EMPTY_USR_OR_PWD",
                            "4":"BAD_QUERY_SYNTAX",
                            "5":"OPERATION_DENIED",
                            "7":"INVALID_USER_TOKEN",
                            "8":"INVALID_MEDIATYPE",
                            "9":"MISSING_MEDIATYPE",
                            "10":"MISSING_IDM",
                            "11":"INVALID_HOST",
                            "12":"MISSING_IDV",
                            "13":"INVALID_LANGUAGE",
                            "15":"APP_NOT_FOUND",
                            "16":"APP_INACTIVE",
                            "17":"APP_CANT_LOGIN",
                            "18":"APP_MISSCONFIGURED",
                            "19":"METHOD_NOT_EXIST",
                            "20":"QUOTA_EXCEEDED",
                            "21":"APP_NOT_ALLOWED",
                            "22":"VIDEO_NOT_FOUND",
                            "30":"USER_OPERATION_DENIED",
                            "31":"USER_NOT_FOUND",
                            "32":"USER_INACTIVE",
                            "42":"NO_RESULTS_FOUND",
                            "50":"MEDIA_NOT_FOUND",
                            "51":"EMPTY_LINKS",
                            "52":"INVALID_EPISODES_IDS"}

    return constants[texto]

def error_message(error):
    
    try:
        import xbmcgui
        dialog=xbmcgui.Dialog()
    
        text=get_constant("error")[str(error)]

        dialog.ok("SERIES.LY", text)
    except:
        logger.info("se ha producido en un error "+str(error))

def get_default_filters():
    filters={'mediaType': 1, 'min_year': '1900', 'limit': 10, 'genre': 'sci-fi', 'max_year': '2022', 'order': 'trending'}

    path=config.get_data_path()

    try:
        j=open(path+"seriesly.default.json","r")
        filters=load_json(j.read())
        logger.info("filtros: %s"%str(filters))
    except:
        import json

        f =open(path+"seriesly.default.json", "w+")
        json.dump(filters,f)
        f.close()
    
    return filters




