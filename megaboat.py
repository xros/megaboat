# -*- coding: utf-8 -*-
# Copyright to Alexander Liu. 
# Any distrubites of this copy should inform its author. If for commercial, please inform the author for authentication. Apr 2014
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import etree
import time
import json
import urllib
import urllib2
# For media posting
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class ParsingContainer(object):
    """Parsing Wechat messages for whose types are of : 'text', 'image', 'voice', 'video', 'location', 'link'
    After making a new instance of the class, need to declare the 'MsgType'
    For example, 
    $~ python
    >>> holder = ParsingContainer()
    >>> hasattr(holder, "_Content")
    >>> True
    >>> holder.initType(MsgType='video')
    >>> hasattr(holder, "_PicUrl")
    >>> True
    >>> holder.initType(MsgType='text') # Or we can just ellipsis this operation since by default its 'text'
    >>> hasattr(holder, "_PicUrl")
    >>> False
    >>> hasattr(holder, "_Content")
    >>> True
    >>> holder.getElementByTag('Content')
    >>> ''
    """
    # By default, MsgType is set as 'text'
    MsgType = 'text'
    # Unique tages in all the mapping relationship
    # 
    # For those tags in-common of normal message
    global commonTag
    commonTag = ['ToUserName', 'FromUserName', 'CreateTime', 'MsgId', 'MsgType']
    # For normal message mapping
    global normalMapping
    normalMapping = {
                    'text':['Content'],
                    'image':['PicUrl', 'MediaId'],
                    'voice':['MediaId','Format'],
                    'video':['MediaId','ThumbMeiaId'],
                    'location':['Location_X','Location_Y','Scale', 'Label'],
                    'link':['Title','Description','Url'],
                  } 

    # For event message mapping
    global eventMapping
    eventMapping = {
                    # The list presents the combined tag set of the event message
                    'event':['Event','EventKey','Ticket','Latitude','Longitude','Precision' ],
                  }

    # For recognition message mapping
    global recognitionMapping 
    recognitionMapping = {
                    'voice':['MediaId','Format','Recognition'],
                  }

    def __init__(self, incomingMessage='<xml></xml>'):
        # pre-set some common variables 
        root = etree.fromstring(incomingMessage)
        # The 5 ones in common
        if root.find('ToUserName') is not None:
            self._ToUserName = root.find('ToUserName').text
        else:
            self._ToUserName = ''
        if root.find('FromUserName') is not None:
            self._FromUserName = root.find('FromUserName').text
        else:
            self._FromUserName = ''
        if root.find('CreateTime') is not None:
            self._CreateTime = root.find('CreateTime').text
        else:
            self._CreateTime = '1000000000'
        if root.find('MsgType') is not None:
            self._MsgType = root.find('MsgType').text
        else:
            self._MsgType = ''
        if root.find('MsgId') is not None:
            self._MsgId = root.find('MsgId').text
        else:
            self._MsgId = ''
        # Store the XML incomingMessage if has
            
        # For text message only
        if self.MsgType == 'text':
            if root.find('Content') is not None:
                self._Content = root.find('Content').text
            else:
                self._Content = ''
        # For image message only
        elif self.MsgType == 'image':
            if root.find('PicUrl') is not None:
                self._PicUrl = root.find('PicUrl').text
            else:
                self._PicUrl = ''
            if root.find('MediaId') is not None:
                self._MediaId = root.find('MediaId').text
            else:
                self._MediaId = ''
        # For voice message only
        elif self.MsgType == 'voice':
            if root.find('MediaId') is not None:
                self._MediaId = root.find('MediaId').text
            else:
                self._MediaId = ''
            if root.find('Format') is not None:
                self._Format = root.find('Format').text
            else:
                self._Format = ''
        # For video message only
        elif self.MsgType == 'video':
            if root.find('MediaId') is not None:
                self._MediaId = root.find('MediaId').text
            else:
                self._MediaId = ''
            if root.find('ThumbMediaId') is not None:
                self._ThumbMediaId = root.find('ThumbMediaId').text
            else:
                self._ThumbMediaId = ''
        # For location message only
        elif self.MsgType == 'location':
            if root.find('Location_X') is not None:
                self._Location_X = root.find('Location_X').text
            else:
                self._Location_X = ''
            if root.find('Location_Y') is not None:
                self._Location_Y = root.find('Location_Y').text
            else:
                self._Location_Y = ''
            if root.find('Scale') is not None:
                self._Scale = root.find('Scale').text
            else:
                self._Scale = ''
            if root.find('Label') is not None:
                self._Label = root.find('Label').text
            else:
                self._Label = ''
        # For link message only
        elif self.MsgType == 'link':
            if root.find('Title') is not None:
                self._Title = root.find('Title').text
            else:
                self._Title = ''
            if root.find('Description') is not None:
                self._Description = root.find('Description').text
            else:
                self._Description = ''
            if root.find('Url') is not None:
                self._Url = root.find('Url').text
            else:
                self._Url = ''
        # For event message only
        elif self.MsgType == 'event':
            # It has to have a ```self._Event``` for event message certainly
            if root.find('Event') is not None:
                self._Event = root.find('Event').text
            else:
                self._Event = ''
            
            if root.find('EventKey') is not None:
                self._EventKey = root.find('EventKey').text

            if root.find('Ticket') is not None:
                self._Ticket = root.find('Ticket').text

            if root.find('Latitude') is not None:
                self._Latitude = root.find('Latitude').text

            if root.find('Longitude') is not None:
                self._Longitude = root.find('Longitude').text

            if root.find('Precision') is not None:
                self._Precision = root.find('Precision').text

    def initType(self, MsgType='text', incomingMessage='<xml></xml>'):
        ''' To initialize message type
        '''
        MsgType_list = ['text', 'image', 'voice', 'video', 'location', 'link', 'event']
        if MsgType not in MsgType_list:
            raise ValueError, "MsgType '%s' not valid " % MsgType
        for i in MsgType_list:
            if MsgType == i:
                self.MsgType = i
                break
        # Delete the common tags
        for c in commonTag:
            try:
                delattr(self, '_' + c)
            except:
                pass
        # Delete the unuseful elements in normalMapping
        for k in normalMapping:
            if k !=self.MsgType:
                for m in normalMapping[k]:
                    try:
                        delattr(self, '_' + m)
                    except:
                        pass
        # Delete the unuseful elements in eventMapping
        for k in eventMapping:
            for e in eventMapping[k]:
                try:
                    delattr(self, '_' + e)
                except:
                    pass
        self.__init__(incomingMessage)
        
    # releasing method
    def __del__(self):
        pass

    #@property    
    def getElementByTag(self, tag):
        '''To get element from the tag
        '''
        try:
            gotten =  getattr(self, "_" + tag)
        except:
            return None
            ##raise ValueError
            #tmp = "Instance has no attribute _%s" % tag
            #raise AttributeError, tmp
        else:
            return gotten

    def digest(self, incomingMessage):
        '''To digest the XML message passed from wechat server
        Make the value variable
        The 'incomingMessage' is of XML 
        According to its content this will assgin values to ```self.MsgType and etc..``` Logistics as the followings:
        1) check parent message type :"MsgType"
        2) check subclass message type if "Voice Recognition", "Event", "Normal" 
        3) check children class message type
        '''
        root = etree.fromstring(incomingMessage)
        msgType = root.find("MsgType").text
        # Get message type based from the ```incomingMessage``` variable
        if msgType in ['text', 'image', 'voice', 'video', 'location', 'link', 'event']:
            # Check if the incomingMessage has tag 'Recognition' then, it is a voice recognition message
            if root.find("Recognition") is not None:
                self.type = 'recognition'
            # Check if the incomingMessage has tag 'Event' then, it is a voice event message
            elif root.find("Event") is not None:
                self.type = 'event'
            # After all then 'normal' message
            else:
                self.type = 'normal'
        
        # For normal messages
        if self.type == 'normal':
            if msgType == 'text':
                self.initType('text', incomingMessage)
            elif msgType == 'image':
                self.initType('image', incomingMessage)
            elif msgType == 'voice':
                self.initType('voice', incomingMessage)
            elif msgType == 'video':
                self.initType('video', incomingMessage)
            elif msgType == 'location':
                self.initType('location', incomingMessage)
            elif msgType == 'link':
                self.initType('link', incomingMessage)
            elif msgType == 'image':
                self.initType('image', incomingMessage)

        # TODO
        # For event messages
        if self.type == 'recognition':
            self.initType('voice', incomingMessage)
            # Construct a var ```self._Recognition``` since it is just of this more than that of 'normal message => voice'
            self._Recognition = root.find("Recognition").text
        # For recognition messages
        if self.type == 'event':
            self.initType('event', incomingMessage)


class RespondingContainer(object): 
    """Package XML to reponse to determained wechat message
    For more information please visit: http://mp.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E9%80%81%E8%A2%AB%E5%8A%A8%E5%93%8D%E5%BA%94%E6%B6%88%E6%81%AF
    Usage:
    >>> rc = RespondingContainer()
    >>> rc.initType('text')         # Or we can ellipsis this since it is of 'text' by default
    >>> # Notice we don't need to set the 'CreateTime' since it has been generated automatically :)
    >>> rc.setElementByTag(FromUserName='the_server', ToUserName='the_wechat_client',Content='Hello dude!')
    >>> tpl_out = rc.dumpXML()
    >>> tpl_out
    >>><xml>
    <ToUserName>the_wechat_client</ToUserName>
    <FromUserName>the_server</FromUserName>
    <CreateTime>1397808770</CreateTime>
    <MsgType>text</MsgType>
    <Content>Hello dude!</Content>
    </xml>
    >>>
    """
    def __init__(self, MsgType='text'):
        self._MsgType = MsgType
        # By default set root as the 'text' XML format
        the_tpl = globals()['tpl_' + self._MsgType].encode('utf-8').decode('utf-8')
        self.root = etree.fromstring(the_tpl)
        #print self.root.find("FromUserName").text
        #print type(self.root.find("FromUserName").text)

    def initType(self, MsgType='text'):
        tpl_list = ['text', 'image', 'voice', 'video', 'music', 'news']
        if MsgType not in tpl_list:
            raise ValueError, "Invalid responsing message MsgType '%s'" % MsgType
        else:
            ## Load the template
            #for i in tpl_list:
            #    if MsgType == i:
            #        self._MsgType = MsgType
            #        ## the the template
            #        the_xml = globals()['tpl_'+i]
            #        self.root = etree.fromstring( the_xml )
            #        break
            ## Set the default tag value
            ### Get all the tags 
            #child_list = []
            #for child in self.root.getchildren():
            #    child_list += [str(child)]
            ### Attach 'tag' object to class to make something as : 'self._FromUserName'
            #for i in child_list:
            #    if i == 'CreateTime':
            #        setattr(self,"_"+i, str(int(time.time())))
            #    else:
            #        setattr(self,"_"+i, '')
            self.__init__(MsgType)



    #def setElementByTag(self, tag):
    def setElementByTag(self, **kwargs):
        """ To package XML message into an object
        Usage:
        >>> setElementByTag(FromUserName='the_wechat_server',ToUserName='the_wechat_client',Content='Hello dude!')
        # In this way we can then use ```dumpXML()``` to get the XML we need to reponse to wechat clients! :)
        """

        ## assign the basic time
        self.root.find('CreateTime').text = str(int(time.time()))

        #print "-----"
        #print self._MsgType
        ## For text message only
        if self._MsgType == 'text':
            # To set attribute value to such as: 'self._FromUsername'
            for k, v in kwargs.items():
                try:
                    ## assign value to the object
                    #getattr(self, "_"+k) = v
                    ## assign/update value to the new XML object
                    self.root.find(k).text = v
                except Exception as e:
                    print  e
                    raise e
                    #raise AttributeError, "Message type '%s' has no attribute/tag '%s'" % (self._MsgType, k)

        ## For image message only
        elif self._MsgType == 'image':
            # To set attribute value of the XML special for image
            for k, v in kwargs.items():
                if k == 'MediaId':
                    #print v
                    #print etree.tostring(self.root)
                    self.root.find('Image').find('MediaId').text = v
                else:
                    try:
                        ## assign/update value to the new XML object
                        self.root.find(k).text = v
                    except Exception as e:
                        print  e
                        raise e

        ## For voice message only
        elif self._MsgType == 'voice':
            # To set attribute value of the XML special for image
            for k, v in kwargs.items():
                if k == 'MediaId':
                    #print v
                    #print etree.tostring(self.root)
                    self.root.find('Voice').find('MediaId').text = v
                else:
                    try:
                        ## assign/update value to the new XML object
                        self.root.find(k).text = v
                    except Exception as e:
                        print  e
                        raise e

        ## For video message only
        elif self._MsgType == 'video':
            # To set attribute value of the XML special for image
            for k, v in kwargs.items():
                if k == 'MediaId':
                    #print v
                    #print etree.tostring(self.root)
                    self.root.find('Video').find('MediaId').text = v
                elif k == 'Title':
                    self.root.find('Video').find('Title').text = v
                elif k == 'Description':
                    self.root.find('Video').find('Description').text = v
                elif k == 'MusicUrl':
                    self.root.find('Video').find('MusicUrl').text = v
                elif k == 'HQMusicUrl':
                    self.root.find('Video').find('HQMusicUrl').text = v
                elif k == 'ThumbMediaId':
                    self.root.find('Video').find('ThumbMediaId').text = v
                else:
                    try:
                        ## assign/update value to the new XML object
                        self.root.find(k).text = v
                    except Exception as e:
                        print  e
                        raise e

        ## For article message only
        elif self._MsgType == 'article':
            # To set attribute value of the XML special for image
            for k, v in kwargs.items():
                if k == 'ArticleCount':
                    self.root.find(k).text = v
                if k == 'Articles':
                    # TODO to generate articles as 
                    #print v
                    #print etree.tostring(self.root)
                    self.root.find('Video').find('MediaId').text = v
                elif k == 'Title':
                    self.root.find('Video').find('Title').text = v
                elif k == 'Description':
                    self.root.find('Video').find('Description').text = v
                elif k == 'MusicUrl':
                    self.root.find('Video').find('MusicUrl').text = v
                elif k == 'HQMusicUrl':
                    self.root.find('Video').find('HQMusicUrl').text = v
                elif k == 'ThumbMediaId':
                    self.root.find('Video').find('ThumbMediaId').text = v
                else:
                    try:
                        ## assign/update value to the new XML object
                        self.root.find(k).text = v
                    except Exception as e:
                        print  e
                        raise e

    def dumpXML(self):
        # To dump the XML we need
        # the ```self.root``` has been assigned already
        return etree.tostring(self.root, encoding='utf-8',method='xml',pretty_print=True)


# The down blow are the templates of all the responsing message valid for wechat
# For more information, please visit : http://mp.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E9%80%81%E8%A2%AB%E5%8A%A8%E5%93%8D%E5%BA%94%E6%B6%88%E6%81%AF
global tpl_text
global tpl_image
global tpl_voice
global tpl_video
global tpl_music
global tpl_news
tpl_text = u'''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[你好]]></Content>
</xml>'''

tpl_image = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[image]]></MsgType>
<Image>
<MediaId><![CDATA[media_id]]></MediaId>
</Image>
</xml>'''

tpl_voice = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[voice]]></MsgType>
<Voice>
<MediaId><![CDATA[media_id]]></MediaId>
</Voice>
</xml>'''

tpl_video = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[video]]></MsgType>
<Video>
<MediaId><![CDATA[media_id]]></MediaId>
<Title><![CDATA[title]]></Title>
<Description><![CDATA[description]]></Description>
</Video> 
</xml>'''

tpl_music = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[TITLE]]></Title>
<Description><![CDATA[DESCRIPTION]]></Description>
<MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl>
<HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>
<ThumbMediaId><![CDATA[media_id]]></ThumbMediaId>
</Music>
</xml>'''

tpl_news = '''<xml>
<ToUserName><![CDATA[toUser]]></ToUserName>
<FromUserName><![CDATA[fromUser]]></FromUserName>
<CreateTime>12345678</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>2</ArticleCount>
<Articles>
<item>
<Title><![CDATA[title1]]></Title> 
<Description><![CDATA[description1]]></Description>
<PicUrl><![CDATA[picurl]]></PicUrl>
<Url><![CDATA[url]]></Url>
</item>
<item>
<Title><![CDATA[title]]></Title>
<Description><![CDATA[description]]></Description>
<PicUrl><![CDATA[picurl]]></PicUrl>
<Url><![CDATA[url]]></Url>
</item>
</Articles>
</xml>'''

# Positive response
class PositiveRespondingContainer(object):
    '''Using wechat custom service API to pass 6 types of messages to those wechat clients \n
    who sent messages to the public wechat service. Those 6 types of messages include:
    text, image, voice, video, music, news
    The dumped is of dict format.
    We need to json.loads(the_dict_object) if we want to pass the right reponse back
    '''
    def __init__(self, MsgType='text'):
        self._MsgType = MsgType
        # By default set the ```self.the_dict``` as from the 'text' JSON format
        the_json_tpl = globals()['json_' + self._MsgType].encode('utf-8').decode('utf-8')
        self.the_dict = json.loads(the_json_tpl)
        if MsgType == 'text':
            pass

    def initType(self, MsgType='text'):
        if MsgType not in ['text', 'image', 'voice', 'video', 'music', 'news']:
            raise ValueError, "It has no message type: '%s'" % MsgType
        else:
            # pass the message type to have ```self.the_dict```
            self.__init__(MsgType)

    def setElementByKey(self, **kwargs):
        '''To set the ```self.the_dict``` according to the message type by such as ```initType(MsgType='text')```
        Notice: all the kwargs 's key in this function  should be of lower case. Official wechat define that. Don't claim '''
        ## For text message only
        if self._MsgType == 'text':
            for k, v in kwargs.items():
                try:
                    if k == 'content':
                        self.the_dict['text'][k] = v
                    else:
                        self.the_dict[k] = v
                except Exception as e:
                    print e
                    raise e
        ## For image message only
        elif self._MsgType == 'image':
            for k, v in kwargs.items():
                try:
                    if k == 'media_id':
                        self.the_dict['image'][k] = v
                    else:
                        self.the_dict[k] = v
                except Exception as e:
                    print e
                    raise e
        ## For voice message only
        elif self._MsgType == 'voice':
            for k, v in kwargs.items():
                try:
                    if k == 'media_id':
                        self.the_dict['voice'][k] = v
                    else:
                        self.the_dict[k] = v
                except Exception as e:
                    print e
                    raise e
        ## For video message only
        elif self._MsgType == 'video':
            for k, v in kwargs.items():
                try:
                    if k == 'media_id':
                        self.the_dict['video'][k] = v
                    elif k == 'title':
                        self.the_dict['video'][k] = v
                    elif k == 'description':
                        self.the_dict['video'][k] = v
                    else:
                        self.the_dict[k] = v
                except Exception as e:
                    print e
                    raise e
        ## For music message only
        elif self._MsgType == 'music':
            for k, v in kwargs.items():
                try:
                    if k == 'musicurl':
                        self.the_dict['music'][k] = v
                    elif k == 'title':
                        self.the_dict['music'][k] = v
                    elif k == 'description':
                        self.the_dict['music'][k] = v
                    elif k == 'hqmusicurl':
                        self.the_dict['music'][k] = v
                    elif k == 'thumb_media_id':
                        self.the_dict['music'][k] = v
                    else:
                        self.the_dict[k] = v
                except Exception as e:
                    print e
                    raise e
        ## For news message only
        elif self._MsgType == 'news':
            for k, v in kwargs.items():
                try:
                    # here we just check whether the ```v``` is type of list the ```v``` should be packaged in a list already
                    # if list, then its the elment of the key ```articles``` for the news message
                    '''
                        "articles": [
                         {
                             "title":"Happy Day",
                             "description":"Is Really A Happy Day",
                             "url":"URL",
                             "picurl":"PIC_URL"
                         },
                         {
                             "title":"Happy Day",
                             "description":"Is Really A Happy Day",
                             "url":"URL",
                             "picurl":"PIC_URL"
                         }
                         ]
                    '''
                    if k == 'articles': 
                        if type(v) == list:
                            self.the_dict['news'][k] = v
                        else:
                            raise ValueError, "The value of the key 'articles' should be of type list" 
                    elif k == 'touser':
                        self.the_dict['touser'] = v
                    elif k == 'msgtype':
                        self.the_dict['msgtype'] = 'news'
                except Exception as e:
                    print e
                    raise e
    

    # package article
    def packageArticle(title= "default title", description="default description", url="http://www.baidu.com", picurl="http://www.baidu.com/img/bdlogo.gif"):
        '''This will return an article in a list which contains a dict.
        While construcing the JSON dumped,
        This is used with the function ```setElementByKey(touser='someone', msgtype='news', articles=packageArticle())```
        '''
        return [{"title": title, "description":description, "url":url, "picurl":picurl}]


    # to dump the the dict as for later on JSON loading
    def dumpDict(self):
        return self.the_dict
    



json_text = '''{
    "touser":"OPENID",
    "msgtype":"text",
    "text":
    {
         "content":"Hello World"
    }
}'''

json_image = '''{
    "touser":"OPENID",
    "msgtype":"image",
    "image":
    {
      "media_id":"MEDIA_ID"
    }
}'''

json_voice = '''{
    "touser":"OPENID",
    "msgtype":"voice",
    "voice":
    {
      "media_id":"MEDIA_ID"
    }
}'''

json_video = '''{
    "touser":"OPENID",
    "msgtype":"video",
    "video":
    {
      "media_id":"MEDIA_ID",
      "title":"TITLE",
      "description":"DESCRIPTION"
    }
}'''

json_music = '''{
    "touser":"OPENID",
    "msgtype":"music",
    "music":
    {
      "title":"MUSIC_TITLE",
      "description":"MUSIC_DESCRIPTION",
      "musicurl":"MUSIC_URL",
      "hqmusicurl":"HQ_MUSIC_URL",
      "thumb_media_id":"THUMB_MEDIA_ID" 
    }
}'''

json_news = '''{
    "touser":"OPENID",
    "msgtype":"news",
    "news":{
        "articles": [
         {
             "title":"Happy Day",
             "description":"Is Really A Happy Day",
             "url":"URL",
             "picurl":"PIC_URL"
         },
         {
             "title":"Happy Day",
             "description":"Is Really A Happy Day",
             "url":"URL",
             "picurl":"PIC_URL"
         }
         ]
    }
}'''




class SubscriberManager(object):
    '''To manage the subscriber groups, profile, location, list.
    Usage:
    >>> sm = SubscriberManager()
    >>> sm.loadToken('abcdefg1234567')
    >>> hisprofile = sm.getSubscriberProfile(openid='his_open_id', lang='zh_CN')
    
    '''
    def __init__(self, token=''):
        self._token = token

    def loadToken(self, token=''):
        '''Firstly load the access token, then use the functions below'''
        self._token = token

    def getSubscriberProfile(self, openid='', lang='zh_CN'):
        '''The open_id parameter is unique to unique wechat public service.
        This function will return a dict if ```token``` and ```open_id``` are valid.
        If not exists or not valid will return None.
        For the parameter 'zh_CN', there are others: 'zh_TW, en'
        For more information: please visit, http://mp.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E7%94%A8%E6%88%B7%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF'''
        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=" + self._token + "&openid=" + openid + "&lang=" + lang
        try:
            a = urllib2.urlopen(url)
        except Exception as e:
            print e
            return None
        else:
            gotten = a.read()
            a_dict = json.loads(gotten)
            # means wrong appid or secret
            if a_dict.has_key('errcode'):
                return None
            else:
                return a_dict

    def createGroup(self, name=''):
        '''Create a determained group name. 
        If created, then it will return the new group id of type 'int'.
        If not, will return None.
        '''
        url = "https://api.weixin.qq.com/cgi-bin/groups/create?access_token=" + self._token 
        postData = '{"group": {"name": "%s"} }' % name
        request = urllib2.Request(url,data=postData)
        request.get_method = lambda : 'POST'
        try: 
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            return None
        else:
            a_dict = json.loads(response.read())
            if a_dict.has_key('errcode'):
                return None
            else:
                return a_dict['group']['id']

    def getAllgroups(self):
        ''' A dict will be returned.
        For more information please visit: 
        http://mp.weixin.qq.com/wiki/index.php?title=%E5%88%86%E7%BB%84%E7%AE%A1%E7%90%86%E6%8E%A5%E5%8F%A3#.E6.9F.A5.E8.AF.A2.E6.89.80.E6.9C.89.E5.88.86.E7.BB.84
        '''
        url = "https://api.weixin.qq.com/cgi-bin/groups/get?access_token=" + self._token
        try:
            response = urllib2.urlopen(url)
        except Exception as e:
            print e
            return None
        else:
            a_dict = json.loads(response.read())
            if a_dict.has_key('errcode'):
                return None
            else:
                return a_dict

    def getHisGroupID(self, openid=''):
        '''Get a subscriber's group ID. The ID is of type 'int'.
        If openid wrong or token invalid, 'None' will be returned.
        For more information, please visit:
        http://mp.weixin.qq.com/wiki/index.php?title=%E5%88%86%E7%BB%84%E7%AE%A1%E7%90%86%E6%8E%A5%E5%8F%A3#.E6.9F.A5.E8.AF.A2.E7.94.A8.E6.88.B7.E6.89.80.E5.9C.A8.E5.88.86.E7.BB.84'''
        url = "https://api.weixin.qq.com/cgi-bin/groups/getid?access_token="+ self._token
        postData = '{"openid":"%s"}' % openid
        request = urllib2.Request(url,data=postData)
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            return None
        else:
            a_dict = json.loads(response.read())
            if a_dict.has_key('errcode'):
                return None
            else:
                return a_dict['groupid']

    def updateGroupName(self, groupid='', new_name=''):
        '''Update the determained group id with the new_name.
        'True' or False if updated or not.
        For more information, please visit:
        http://mp.weixin.qq.com/wiki/index.php?title=%E5%88%86%E7%BB%84%E7%AE%A1%E7%90%86%E6%8E%A5%E5%8F%A3#.E4.BF.AE.E6.94.B9.E5.88.86.E7.BB.84.E5.90.8D
        '''
        url = "https://api.weixin.qq.com/cgi-bin/groups/update?access_token=" + self._token 
        postData = '{"group":{"id":%s,"name":"%s"}}' % (groupid, new_name)
        request = urllib2.Request(url,data=postData)
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            return False
        else:
            a_dict = json.loads(response.read())
            #print a_dict
            if a_dict.has_key('errcode'):
                if a_dict['errcode'] == 0:
                    return True
                else:
                    return False
            else:
                return False

    def moveHimToGroup(self, openid='', groupid=''):
        '''Move him to other group.
        'True' or 'False' if moved or not.
        For more information please visit:
        http://mp.weixin.qq.com/wiki/index.php?title=%E5%88%86%E7%BB%84%E7%AE%A1%E7%90%86%E6%8E%A5%E5%8F%A3#.E7.A7.BB.E5.8A.A8.E7.94.A8.E6.88.B7.E5.88.86.E7.BB.84'''
        url = "https://api.weixin.qq.com/cgi-bin/groups/members/update?access_token=" + self._token 
        postData = '{"openid":"%s","to_groupid":%s}' % (openid, groupid)
        request = urllib2.Request(url,data=postData)
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            return False
        else:
            a_dict = json.loads(response.read())
            #print a_dict
            if a_dict.has_key('errcode'):
                if a_dict['errcode'] == 0:
                    return True
                else:
                    return False
            else:
                return False

    def getSubscriberList(self, next_openid=''):
        '''To get subscriber list.
        A dict will be return if valid.
        If ```token``` and ```next_openid``` are valid, then a dict will be returned.
        If the ```next_openid``` does not exist, official wechat server takes it as '' by default
        If not, a 'None' will be returned.
        For more information please visit:
        http://mp.weixin.qq.com/wiki/index.php?title=%E8%8E%B7%E5%8F%96%E5%85%B3%E6%B3%A8%E8%80%85%E5%88%97%E8%A1%A8
        '''
        url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=" + self._token + "&next_openid=" + next_openid
        try:
            response = urllib2.urlopen(url)
        except Exception as e:
            print e
            return None
        else:
            a_dict = json.loads(response.read())
            #print a_dict
            if a_dict.has_key('errcode'):
                return None
            else:
                return a_dict







def getAPIToken(appid='', appsecret=''):
    '''Get wechat API token for cusmter service or others.
    If ```appid``` and ```appsecret``` are correct then a string 'token' will be return.
    If not , 'return None' '''
    default_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&'
    url = default_url + 'appid=' + appid + '&secret=' + appsecret
    try:
        a = urllib2.urlopen(url)
    except Exception as e:
        print e
        return None
    else:
        gotten = a.read()
        a_dict = json.loads(gotten)
        if a_dict.has_key('access_token'):
            return a_dict['access_token']
        # means wrong appid or secret
        else:
            return None


def postMessage2API(token='',messageString=''):
    '''Using the token, post the message to determained user.
    This returns a Boolean value'''
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=" + token
    request = urllib2.Request(url, messageString)
    request.get_method = lambda : 'POST'
    try:
        response = urllib2.urlopen(request)
    except Exception as e:
        print e
        return False
    else:
        j = json.loads(response.read())
        # The above works 
        #print j
        # to check if the message was accepted
        if j['errcode'] == 0:
            return True
        else:
            return False


class MenuManager(object):
    '''To manage the bottom menu of the wechat service
    Usage:
    >>> mm = MenuManager()
    >>> mm.loadToken('something_the_api_token')
    >>> flag = mm.createMenu('the_menu_format_constructed_from_a_JSON_as_a_string')
    >>> flag
    True
    >>> menu_got = mm.getMenu()
    >>> menu_got
    {u'menu': {u'button': [{u'type': u'click', u'name': u'\u7b2c\u4e00\u94ae', u'key': u'V1001_TODAY_MUSIC', u'sub_button': []}, {u'type': u'click', u'name': u'\u7b2c\u4e8c\u94ae', u'key': u'V1001_TODAY_SINGER', u'sub_button': []}, {u'name': u'\u7b2c\u4e09\u94ae', u'sub_button': [{u'url': u'http://www.soso.com/', u'type': u'view', u'name': u'\u641c\u641c', u'sub_button': []}, {u'url': u'http://v.qq.com/', u'type': u'view', u'name': u'\u770b\u7535\u5f71', u'sub_button': []}, {u'type': u'click', u'name': u'\u5938\u6211\u5e05', u'key': u'V1001_GOOD', u'sub_button': []}]}]}}
    >>> flag2 = mm.deleteMenu()
    >>> flag2
    True
    >>> mm.getMenu()
    >>> # nothing gotten:  it means no menu at all

    '''

    def __init__(self, token=''):
        self._token = token
    def loadToken(self, token=''):
        '''Load the token before using other functions'''
        self._token = token
    def createMenu(self, menu_format=''):
        '''Create menu, it needs a token and the menu format. 
        The ```menu_format``` is of type string.
        But ```menu_format``` is constructed from a JSON.
        For more information please visit:
        http://mp.weixin.qq.com/wiki/index.php?title=%E8%87%AA%E5%AE%9A%E4%B9%89%E8%8F%9C%E5%8D%95%E5%88%9B%E5%BB%BA%E6%8E%A5%E5%8F%A3
        '''
        token = self._token
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + token 
        request = urllib2.Request(url, menu_format)
        request.get_method = lambda : 'POST'
        try:
            response = urllib2.urlopen(request)
        except Exception as e:
            print e
            return False
        else:
            j = json.loads(response.read())
            # The above works 
            #print j
            # to check if the message was accepted
            if j['errcode'] == 0:
                return True
            else:
                return False

    def getMenu(self):
        '''Get the menu format from the API.
        If there be, then a dict would be returned.
        If not, 'None' will be returned.
        '''
        token = self._token
        url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="+ token
        try:
            response = urllib2.urlopen(url)
        except Exception as e:
            # its better to raise something here if the wechat remote server is down
            print e
            return None
        else:
            a_dict = json.loads(response.read())
            if a_dict.has_key('errcode'):
                if a_dict['errcode'] != 0:
                    return None
                else:
                    return a_dict
            else:
                return a_dict

    def deleteMenu(self):
        token = self._token
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=" + token
        try:
            response = urllib2.urlopen(url)
        except Exception as e:
            print e
            return False
        else:
            a_dict = json.loads(response.read())
            if a_dict.has_key('errcode'):
                if a_dict['errcode'] == 0:
                    return True
                else:
                    return False
            else:
                return False





class MediaManager(object):
    '''There are four types of media suppored by wechat.
    image, voice, video, thumb
    Post the file to the offical wechat server and get the response.
    '''
    def __init__(self, media_type='image', token = ''):
        self._media_type = media_type
        self._token = token

    def loadToken(self, token = ''):
        self._token = token

    def uploadMedia(self, media_type='image', media_path=''):
        '''Post the determained media file to the offical URL
        If the image is valid, then a_dict will be returned. 
        If not, 'None' will be returned. 
        For more information, please visit: http://mp.weixin.qq.com/wiki/index.php?title=%E4%B8%8A%E4%BC%A0%E4%B8%8B%E8%BD%BD%E5%A4%9A%E5%AA%92%E4%BD%93%E6%96%87%E4%BB%B6'''
        if media_type not in ['image', 'voice', 'video', 'thumb']:
            raise ValueError, "Media type: '%s' not valid" % media_type
        else:
            self._media_type = media_type
        url = "http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token=" + self._token + "&type=" + self._media_type
        register_openers()
        try:
            datagen, headers = multipart_encode({"image1": open(media_path,"rb")})
        except Exception as e:
            #print e
            return None
            #raise e
        else:
            request = urllib2.Request(url,data=datagen,headers=headers)
            try:
                response = urllib2.urlopen(request)
            except Exception as e:
                print e
                return None
           
