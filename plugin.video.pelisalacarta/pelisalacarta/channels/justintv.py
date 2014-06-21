# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para justin.tv by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys
import xbmc,xbmcgui,xbmcplugin

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
from platformcode.xbmc import xbmctools
try:
    import json
except:
    import simplejson as json

__channel__ = "justintv"
__category__ = "G"
__type__ = "generic"
__title__ = "Justin.tv"
__language__ = ""
__creationdate__ = "20111128"

DEBUG = config.get_setting("debug")
pluginhandle = int(sys.argv[1])

IMAGES_PATH = xbmc.translatePath( os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'posters' ) )
fanart = xbmc.translatePath(os.path.join( config.get_runtime_path(), 'resources' , 'images' ,'fanart','justintv.png'))
if config.get_setting("thumbnail_type")=="0":
    WEB_PATH = "http://pelisalacarta.mimediacenter.info/posters/"
else:
    WEB_PATH = "http://pelisalacarta.mimediacenter.info/banners/"

jtv_icon = WEB_PATH+"justintv.png"

all = config.get_localized_string(30419)

languages = [all,'Arabic','Català','Cerky','Dansk','Deutsch','Greek','English','Español','Eusti Keel','suomi','Francais',
            'Hindi' ,'Hrvatski','bahasa Indonesia','Italiano','Hebrew','Japanese','Korean','Lietuviu','Nederlands',
            'Norsk','Polski','Portugues','Romana','Russian','Serbian','Svenska','Talagog','Turkey','Tieng Viet',
            'Chinese','Taiwanese']
abbrev   = ['all','ar','ca','cs','da','de','el','en','es','et','fi','fr','hi','hr','id','it','iw','ja','ko','lt','nl','no','pl','pt',
            'ro','ru','sr','sv','tl','tr','vi','zh-CN','zh-TW']
limit = 50
URL_CATEGORY_MENU = 'http://%s.justin.tv/directory/dropmenu/category?lang=%s&amp;order=hot'
URL_SUBCATEGORY_MENU = 'http://%s.justin.tv/directory/dropmenu/subcategory/%s?order=hot&amp;lang=%s'
MenuLang = {'English':'en','Spanish':'es','Italian':'it','Catalan':'ca','French':'fr','Portuguese':'pt','German':'de'}
try:
    language_menu = MenuLang[xbmc.getLanguage()]
except:
    language_menu = 'en'

def isGeneric():
    return True

def mainlist(item):
    logger.info("[justintv.py] mainlist")

    itemlist = []
    try:
        lang = config.get_setting('justin_lang')
        if "," in lang:
            langs = lang.split(",")
            lang = ''
            for i in langs:
                idx  = abbrev.index(i)
                if len(lang)>0:
                    lang = lang + "," + languages[idx]
                else:
                    lang = languages[idx]
            
        else:
            idx  = abbrev.index(lang)
            lang = languages[idx]
    except:
        lang = 'all'
        idx  = abbrev.index(lang)
        lang = languages[idx]
    

    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30420) + ' (%s)' %lang, action="_language"     ,url = "", thumbnail =WEB_PATH+ "language.jpg",fanart = fanart, folder = False))
    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30414), action="listcategory"     ,url = "true", thumbnail='http://www-cdn.jtvnw.net/images/redesign/fp_vector_camera.png',fanart = fanart))
    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30413), action="listcategory"     ,url = "false", thumbnail='',fanart = fanart))
    return itemlist

def listcategory(item):
    itemlist = []
    config.set_setting("streamlive",item.url)
    listcat = getlistcategory()
    if item.url=='false':
        title = config.get_localized_string(30408)
    else:
        title = ''
    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30416)+title, action="favorites"     ,url = "", thumbnail=WEB_PATH+ "favoritos.png",fanart = fanart))
    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30415), action="getplayByID"     ,url = "", thumbnail="http://thecustomizewindows.com/wp-content/uploads/2011/12/Best-Keyboard-Apps.png",fanart = fanart))
    itemlist.append( Item(channel=__channel__, title=config.get_localized_string(30417), action="search"        ,url = "", thumbnail=WEB_PATH+"buscador.png",fanart = fanart))
    for category in listcat:
        itemlist.append( Item(channel=__channel__, title=scrapertools.unescape(category[1]), action="subCategories" ,url = category[0], thumbnail="http://www-cdn.jtvnw.net/images/category_icons/%s.png" %category[0],fanart = fanart))

    return itemlist
    
def getlistcategory():
    data = scrapertools.cache_page(URL_CATEGORY_MENU %(language_menu,language_menu))
    patron = '<li class="category"><a href="/directory/([^\?]+)\?.+?">(.+?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    list = []
    for match in matches:
        list.append([match[0],match[1]])
    return list

def search(item,texto):
    
    texto = texto.replace(' ','+')
    item.title = 'search'
    item.url = url =  'http://api.justin.tv/api/stream/search/'+texto+'.json?offset=0&limit='+str(limit)
    itemlist = getlistchannel(item)
    if config.get_setting('streamlive')=='true':
        xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
    else:
        return itemlist

    
def getplayByID(item):
    logger.info("[justintv.py] plyByID")
    tecleado = ""
    default = ""
    itemlist = []
    tecleado = teclado(heading=config.get_localized_string(30405))
    if len(tecleado)>0:
        item.url = 'http://api.justin.tv/api/stream/list.json?channel='+tecleado
        itemlist = getlistchannel(item)
        if len(itemlist)>0:
            if config.get_setting('streamlive') == 'true':
                xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
            else:
                return itemlist
        elif config.get_setting('streamlive') != 'true':
            xbmc.executebuiltin("XBMC.Notification(Justin tv,Streaming no encontrado... verificando archivos"+",5000,"+jtv_icon+")")
            item.url = tecleado
            item.action = 'getplayByID'
            itemlist = listarchives(item)
            if itemlist is not None and len(itemlist)>0:
                return itemlist
            else:
                channelANDarchivesEmpty()
        else:
            channelEmpty()
    return

def teclado(default="", heading="", hidden=False):
    tecleado = ""
    keyboard = xbmc.Keyboard(default,heading,hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)<=0:
            return ""
    return tecleado
    
def subCategories(item):
    logger.info("[justin.tv.py] subCategories")

    category = item.url
    
    url = URL_SUBCATEGORY_MENU %(language_menu,category,language_menu)
    data = scrapertools.cache_page(url)
    logger.info(data)
    itemlist = []
    patron = '<li class="subcategory"><a href="/directory/'+category+'/([^\?]+)\?.+?">(.+?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    scrapedthumbnail = ""
    scrapedplot = item.title
    itemlist.append( Item(channel=item.channel , action="listchannel"   , title=config.get_localized_string(30421) , url="all" , thumbnail=scrapedthumbnail, plot=scrapedplot,category=category,fanart=fanart ))
    for match in matches:
        scrapedurl = match[0]
        scrapedtitle =match[1]

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=item.channel , action="listchannel"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot,category=category,fanart=fanart ))
    
    return itemlist

def favorites(item):
    if item.url == '':
        username = config.get_setting("justin_login")
    else:
        username = item.url
    if username == "":
        LoginEmpty()
        config.open_settings()
        item.url = config.get_setting("justin_login")
        if item.url == '':return
        favorites(item)
        return 
    item.title = "favorites"
    if config.get_setting('streamlive')=='true':
        livetrue='&live=true'
    else:
        livetrue = ''
    item.url = 'http://api.justin.tv/api/user/favorites/'+str(username)+'.json?offset=0&limit='+str(limit)+livetrue
    itemlist = getlistchannel(item)
    if not livetrue:
        return itemlist
    xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
    return 

def addToFavorites(item):
    ''' Poner aqui el proceso para añadir un canal en favoritos/follows de una cuenta en Justin.tv'''
    pass

def removeFromFavorites(item):
    ''' Poner aqui el proceso para eliminar un canal de favoritos/follows de una cuenta en Justin.tv'''
    pass

def listchannel(item):
    
    if not "|Next Page >>" in item.title:
        try:
            lang = config.get_setting("justin_lang")
            if len(lang) == 0:
                lang = 'all'
        except:
            lang = "all"
        item.title = item.url
        if lang == 'all':
            lang = ''
        else:
            lang = '&language='+lang
        if 'all' in item.url:
            item.url = "http://api.justin.tv/api/stream/list.json?category=%s%s&offset=0&limit=%d" %(item.category,lang,limit)
        else:
            item.url = "http://api.justin.tv/api/stream/list.json?subcategory=%s%s&offset=0&limit=%d" %(item.title,lang,limit)
    itemlist = getlistchannel(item)
    if config.get_setting('streamlive')=='true':
        xbmctools.renderItems(itemlist, [], '', 'Movies',isPlayable='true')
        return 
    else:
        return itemlist

def getlistchannel(item):
    logger.info("[justintv.py] getlistchannel")
    
    url = item.url
    title = item.title
    if "|Next Page >>" in item.title:
        item.title = item.title.split('|')[0]
    if item.title == 'favorites':
        context = '|9' # Eliminar un canal de favoritos, en el listado de favoritos solo remover
    else:
        context = '|8' # Añade un canal a favoritos, en los demas listados solo añadir
    data = scrapertools.cache_page(url)
    logger.info(data)
    datadict = json.loads(data)
    totalItems = len(datadict)
    itemlist = []
    #print item.action
    c = 0
    try:
        datadict =  sorted(datadict, key=lambda k: k['video_bitrate'],reverse=True)
    except:
        pass
    for match in datadict:
        try:
            name = match['name'].split('user_')[-1]
        except:
            try:
                name = match['channel']['login']
                if name is None or name =='':
                    raise
            except:
                name = match['login']
        try:
            title = match['channel']['title']
            if title is None or title == '':
                raise
        except:
            try:
                title = match['title']
                if title is None:
                    title = ''
            except:
                title = ''
        try:
            title = title
            if title is None or title == '':
                raise
        except:
            title = name
                
        try:
            tags = scrapertools.unescape(match['channel']['tags'])
            if tags is None or tags == '':
                raise
        except:
            try:
                tags = scrapertools.unescape(match['tags']).strip()
                if tags is None or tags == '':
                    raise
            except:
                tags = ''
        try:
            status = scrapertools.unescape(match['channel']['status']).strip()
            if status is None or status == '':
                raise
        except:
            try:
                status = scrapertools.unescape(match['status']).strip()
                if status is None or status == '':
                    raise
            except:
                status = ''
        try:
            subcat = match['channel']['category_title']
            if subcat is None or subcat == '':
                raise
        except:
            try:
                subcat = match['category']
                if subcat is None:
                    raise
            except:
                subcat = ''
        try:
            views = match['channel']['views_count']
        except:
            try:
                views = match['channel_view_count']
            except:
                views = ''
            
        try:
            bitrate = str(match['video_bitrate']).split('.')[0]
        except:
            bitrate = ''
        try:
            lang = match['language']
        except:
            lang = ''
        try:
            scrapedthumbnail = match['channel']['screen_cap_url_medium']
            
        except:
            scrapedthumbnail = match['screen_cap_url_medium']
        try:
            fanart_thumb = match['channel']['image_url_huge']
        except:
            try:
                fanart_thumb = match['image_url_huge']
            except:
                fanart_thumb = fanart
        scrapedurl = name
        
        idx = abbrev.index(lang)
        lang = languages[idx].decode('utf-8')
        scrapedplot = title +'\nStatus: '+status+'\nTags: '+tags+ '\nChannel Name: '+name+'\nBitrate: '+bitrate+'\nLanguage: '+lang+'\nViews: '+views

        if config.get_setting("streamlive") == "true":
            scrapedtitle =title + ' [%s] BitRate: %s  (%s)' %(name,bitrate,lang)
            itemlist.append( Item(channel   = item.channel,
                                  action    = "playVideo"  ,
                                  title     = scrapedtitle.encode("utf-8") ,
                                  url       = scrapedurl , 
                                  thumbnail = scrapedthumbnail, 
                                  plot      = scrapedplot.encode("utf-8"),
                                  category  = item.plot, 
                                  totalItems= totalItems,
                                  fanart    = scrapedthumbnail, 
                                  context   = '7', # 7 Lista videos archivados 
                                  folder    = False 
                                ))
        else:
            scrapedtitle =title + ' [%s]  (%s)' %(name,lang)
            itemlist.append( Item(channel    = item.channel , 
                                  action     = "listarchives"   , 
                                  title      = scrapedtitle.encode("utf-8") , 
                                  url        = scrapedurl , 
                                  thumbnail  = scrapedthumbnail, 
                                  plot       = scrapedplot.encode("utf-8"),
                                  category   = item.plot, 
                                  totalItems = totalItems,
                                  fanart     = fanart_thumb, 
                                  extra      = fanart_thumb, 
                                  context    = '6', # 6 ver canal en vivo 
                                  folder     = True 
                                ))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

    if totalItems >=limit:
        offset1 = re.compile('offset=(.+?)&').findall(url)[0]
        offset2 = str(int(offset1)+limit+1)
        scrapedurl = item.url.replace("offset="+offset1,"offset="+offset2)
        scrapedtitle = item.title+"|Next Page >>"
        scrapedthumbnail = ''
        scrapedplot = ''
        itemlist.append( Item(channel=item.channel , action="listchannel"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, category=item.category, fanart=fanart ))
    return itemlist

def listarchives(item):
    logger.info("[justin.tv.py] listarchives")
    if "Next Page >>" in item.title:
        url = item.url
    else:
        url = 'http://api.justin.tv/api/channel/archives/'+item.url+'.json?offset=0&limit='+str(limit)
    try:
        data = scrapertools.cache_page(url)
        if len(data)==0:raise
    except:
        if item.action == 'getplayByID':
            return
        archivesempty()
        return
    logger.info(data)
    datadict = json.loads(data)
    totalItems = len(datadict)
    itemlist = []

    for match in datadict:
        try:
            video_url = match['video_file_url']
        except:continue
        try:
            broadcast_part = match['broadcast_part']
        except:
            broadvast_part = ''
        try:
            start_time = match['start_time']
        except:
            start_time = ''
        try:
            thumbnail = match['image_url_medium']
        except:
            thumbnail = ''
        try:
            duration = match['length']
        except:
            duration = ''
        #print 'duration: '+duration
        try:
            title = match['title']
        except:
            title = ''
        scrapedtitle = title + " Part: (%s) Start time: %s" %(broadcast_part,start_time)
        itemlist.append( Item(channel=item.channel , action="play"   , server = 'Directo', title=scrapedtitle.encode("utf-8") , url=video_url , thumbnail=thumbnail, plot=item.url,category = item.category,duration=duration, totalItems=totalItems,fanart = item.extra,context='6',  folder=False ))

    if totalItems >=limit:
        offset1 = re.compile('offset=(.+?)&').findall(url)[0]
        offset2 = str(int(offset1)+limit+1)
        scrapedurl = url.replace("offset="+offset1,"offset="+offset2)
        scrapedtitle = "Next Page >>"
        scrapedthumbnail = ''
        scrapedplot = ''
        itemlist.append( Item(channel=item.channel , action="listarchives"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot, category=item.category, extra=item.extra ))
    
    return itemlist
    
def playVideo(item):
    logger.info("[justin.tv.py] playVideo")

    channelname=item.url
    if channelname.endswith('.flv'):
        channelname = item.plot
    rtmp = ""
    try:
        if config.get_setting('realdebridpremium')=="true":
            from servers import realdebrid
            url = "http://justin.tv/"+channelname
            rtmp = realdebrid.get_video_url( page_url=url , premium=(config.get_setting("realdebridpremium")=="true") , user=config.get_setting("realdebriduser") , password=config.get_setting("realdebridpassword"), video_password="" )
            logger.info('rtmp = %s'%rtmp)
    except:pass
    
    if rtmp.startswith('rtmp'):
        listItem = xbmcgui.ListItem(path = rtmp)
        listItem.setProperty('IsPlayable', 'true')
        xbmcplugin.setResolvedUrl(pluginhandle, True, listItem)
    else:
        req = urllib2.Request('http://justin.tv/')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile('swfobject.embedSWF\("(.+?)"').findall(link)
        swf = ' swfUrl='+str(match[0])
        req = urllib2.Request('http://usher.justin.tv/find/'+channelname+'.json?type=live')
        req.addheaders = ('Referer', 'http://justin.tv/')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        logger.info(link)
        datadict = json.loads(link)
        try:
            token = ' jtv='+datadict[0]["token"].replace('\\','\\5c').replace('"','\\22').replace(' ','\\20')
            connect = datadict[0]["connect"]+'/'+datadict[0]["play"]
            Pageurl = ' Pageurl=http://www.justin.tv/'+channelname
            rtmp = connect+token+swf+Pageurl
            logger.info('rtmp = %s'%rtmp)
            listItem = xbmcgui.ListItem(path = rtmp)
            listItem.setProperty('IsPlayable', 'true')
            xbmcplugin.setResolvedUrl(pluginhandle, True, listItem)
        except:
            logger.info('canal %s esta offline'%channelname)
            xbmcplugin.setResolvedUrl(pluginhandle, False, xbmcgui.ListItem())
            channeloffline(channelname)

def _language(item):
    _language_(item)
    return

def _language_(item):
    lang = config.get_setting('justin_lang')
    if "," in lang:
        lang = lang.split(",")
    elif lang == "":
        lang = ["all"]
    else:
        lang = [lang]
    lenguajes = languages
    squareRoot=scrapertools.unescape("&#8730;")
    for i in lang:
        if i == 'all':
            idx  = abbrev.index(i)
            lenguajes[idx]=lenguajes[idx]+"     "+squareRoot
            break
        idx  = abbrev.index(i)
        lenguajes[idx]=lenguajes[idx]+"     "+squareRoot
            
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Choice a language", lenguajes)
    if seleccion == -1:return
    abb = languages[seleccion]
    logger.info("seleccion : %s %s" %(seleccion,abb))
    lang = ''
    for count,i in enumerate(lenguajes):
        if seleccion == 0:
            lang = 'all'
            break
        
        if squareRoot in i:
            if count == seleccion:continue
            if abbrev[count]=='all':continue
            if len(lang)>0:
                lang = lang + "," + abbrev[count]
            else:
                lang = abbrev[count]
        if count == seleccion:
            if len(lang)>0:
                lang = lang + "," + abbrev[count]
            else:
                lang = abbrev[count]
    config.set_setting('justin_lang',lang)
    logger.info("lenguajes configurados: "+lang)
    xbmc.executebuiltin( "Container.Refresh" )
    return 

def channelEmpty():
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ," "*18+config.get_localized_string(30411))
def LoginEmpty():
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ," "*18+config.get_localized_string(30422))
def channeloffline(channelname):
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ,config.get_localized_string(30423)%channelname)
def archivesempty():
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ," "*18+config.get_localized_string(30412))
def channelANDarchivesEmpty():
    return xbmcgui.Dialog().ok("Pelisalacarta - Justin TV" ," "*18+config.get_localized_string(30411)," "*18+config.get_localized_string(30412))