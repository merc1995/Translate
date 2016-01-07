#!/usr/bin/env python
# -*- coding:utf-8 -*-
#coding:utf-8
#By eathings
from urllib import quote
import urllib
import urllib2
import re
import json
import win32com.client
import wave  
import urllib, urllib2, pycurl  
import base64  
import json
import types
class Youdao:#使用有道API进行翻译
	def __init__(self):
		self.url = 'http://fanyi.youdao.com/openapi.do'
		self.key = 'xxx' #有道API key 需要自己申请
		self.keyfrom = 'xxx' #有道keyfrom  同上

	def get_translation(self,words,heh):
		url = self.url + '?keyfrom=' + self.keyfrom + '&key='+self.key + '&type=data&doctype=json&version=1.1&q=' + words
		result = urllib2.urlopen(url).read()
		json_result = json.loads(result)
		json_result = json_result["translation"]
		for i in json_result:
			heh=i
			break
		return heh
        


## get access token by api key & secret key  
#global quan
def get_token():  
    apiKey = "xx" #申请百度语音API
    secretKey = "xx" 
   
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
   
    res = urllib2.urlopen(auth_url)  
    json_data = res.read()
    print json.loads(json_data)['access_token']
    return json.loads(json_data)['access_token']  
   
def dump_res(buf):
    global quan
    #print buf
    quan=buf
   
## post audio to server  使用百度语音进行识别
def use_cloud(token):  
    fp = wave.open('jingyesi.wav', 'rb')
    #fp = wave.open('vad_0 00_00_04-00_00_11.wav', 'rb') #在此修改文件名
    nf = fp.getnframes()  
    f_len = nf * 2 
    audio_data = fp.readframes(nf)  
   
    cuid = "B8-88-E3-33-03-2F" #my PC  MAC  
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token  
    http_header = [  
        'Content-Type: audio/pcm; rate=8000',  
        'Content-Length: %d' % f_len  
    ]  
   
    c = pycurl.Curl()  
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
    #c.setopt(c.RETURNTRANSFER, 1)  
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict  
    c.setopt(c.POST, 1)  
    c.setopt(c.CONNECTTIMEOUT, 30)  
    c.setopt(c.TIMEOUT, 30)  
    c.setopt(c.WRITEFUNCTION, dump_res)  
    c.setopt(c.POSTFIELDS, audio_data)  
    c.setopt(c.POSTFIELDSIZE, f_len)  
    c.perform() #pycurl.perform() has no return val  
   
if __name__ == "__main__":  
    token = get_token()  
    use_cloud(token)
    l=quan.find(r'["')
    r=quan.find(r'"]')
    #print int(l)
    #print r
    #print quan[l+2:l+3]
    #print "msg::::"+quan
    msg=quan[l+2:r].decode('utf-8').encode('gbk') #注意编码格式
    print "msg::::"+msg
    youdao = Youdao()
    #while True:
    #msg=raw_input()
    mm='';
    #if msg == 'quit':
    #	    break
    msg1=urllib.quote(msg.decode('gbk').encode('utf-8'))
    #print msg1
    mm=youdao.get_translation(msg1,mm)
    print mm
    spk = win32com.client.Dispatch("SAPI.SpVoice")
    spk.Speak(mm)
