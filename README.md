megaboat
========

megaboat is a lib for Wechat API programming. This is written in python. It has been deployed on many projects such as internet of vehicles, and it works well with many web or internet frameworks such as Tornado, Django, Pyramid, Flask, web.py, cherrypy and etc.. 

Introduction
-----
* The module has 5 classes and 2 functions. The 5 classes are responsible of wechat events. This module is compatible with 6 types of the wechat messages including 'text, image, voice, video, link, location'. And 'article' will be added soon.
* class `ParsingContainer` is for parsing the data received from wechat server
* class `RespondingContainer` is for constructing the XML content
* class `PositiveRespondingContainer` is more positive the the class `RespondingContainer` 
* class `MenuManager` manages the wechat menu table construction
* class `MediaManager` helps to post 4 types of media to the wechat server, those include "image, voice, video, thumb"
* function `getAPIToken` will return a token from the wechat service if you need that. e.g. The class `MenuManger` would need that when creating/deleting menus
* function `postMessage2API` will use wechat cumstom service (RESTFul) API to pass 6 types of messages to those wechat clients
Usage
-----
* It is recommended to try this python module/lib using this way!
```bash
$~ python
>>> from megaboat import MenuManger
>>> help(MenuManager)
```
There is informative documentation out there. Here is a demo down blow about how to use this module in the programming way

```python
# Wechat lib [megaboat] Copyright to Alexander Liu
# The 5 classes
from megaboat import ParsingContainer
from megaboat import RespondingContainer
from megaboat import PositiveRespondingContainer
from megaboat import MenuManager                                                         
from megaboat import MediaManager
# The 2 functions
from megaboat import getAPIToken
from megaboat import postMessage2API
#
# Tutorial demo
## 1. Receiving from the wechat

from megaboat import ParsingContainer
pc = ParsingContainer()
pc.digest(incomingMessage)
msgType = pc.getElementByTag('MsgType')
# For text message
if msgType == 'text':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    content = pc.getElementByTag('Content').encode('utf-8').decode('utf-8')
    msgId = pc.getElementByTag('MsgId')
# For image message
elif msgType == 'image':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    picUrl = pc.getElementByTag('PicUrl')
    mediaId = pc.getElementByTag('MediaId')
    msgId = pc.getElementByTag('MsgId')
# For voice message
elif msgType == 'voice':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    mediaId = pc.getElementByTag('MediaId')
    format_ = pc.getElementByTag('Format')
    msgId = pc.getElementByTag('MsgId')
# For video message
elif msgType == 'video':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    mediaId = pc.getElementByTag('MediaId')
    thumbMediaId = pc.getElementByTag('ThumbMediaId')
    msgId = pc.getElementByTag('MsgId')
# For location message
elif msgType == 'location':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    location_X = pc.getElementByTag('Location_X')
    location_Y = pc.getElementByTag('Location_Y')
    scale = pc.getElementByTag('Scale')
    label = pc.getElementByTag('Label')
    msgId = pc.getElementByTag('MsgId')
# For link message
elif msgType == 'link':
    toUserName = pc.getElementByTag('ToUserName')
    fromUserName = pc.getElementByTag('FromUserName')
    createTime = pc.getElementByTag('CreateTime')
    msgType = pc.getElementByTag('MsgType')
    title = pc.getElementByTag('Title')
    description = pc.getElementByTag('Description')
    url = pc.getElementByTag('Url')
    msgId = pc.getElementByTag('MsgId')
 
 

# Now we have gotten all the messages those wechat passed onto us


 

## 2. Sending messages to the wechat
from megaboat import RespondingContainer
# For your own good, just find it yourself :)

```
### Happy hacking
