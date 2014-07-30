megaboat
========

megaboat is a lib for Wechat API programming. This is written in python. It has been deployed on many projects such as internet of vehicles, and it works well with many web or internet frameworks such as Tornado, Django, Pyramid, Flask, web.py, cherrypy and etc.. 
Usage
-----
* `
# Wechat lib [megaboat] Copyright to Alexander Liu
# The 5 classes
from megaboat import ParsingContainer
from megaboat import RespondingContainer
from megaboat import PositiveRespondingContainer
from megaboat import MenuManager                                                         from megaboat import MediaManager
# The 2 functions                                                                        from megaboat import getAPIToken
from megaboat import postMessage2API
#
# Tutorial
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


 

## 2. Sending to the wechat
from megaboat import RespondingContainer

from megaboat import PositiveRespondingContainer
from megaboat import MenuManager
from megaboat import MediaManager
# The 2 functions
from megaboat import getAPIToken
from megaboat import postMessage2API
#
 `
