#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    # def __str__(self):
    #     return str(self.code)+"\r\n"+str(self.body)

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        clientSocket.connect((host,port))
        return clientSocket

    def get_code(self, data):
        firstLine = (data.split("\r\n"))[0]
        code = int((firstLine.split(" "))[1])
        return code

    def get_headers(self,data):
        data = data.split("\r\n\r\n")
        data = data[0].split["\r\n"]
        headers = "\r\n".join(data[1:])
        return headers

    def get_body(self, data):
        data = data.split("\r\n\r\n")
        body = data[1]
        return body


    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host,port,path = self.parseURL(url)
        if port == 80:
            Host = host
        else:
            Host = host+":"+str(port)
        con = self.connect(host,port)
        # form the request
        request = "GET %s HTTP/1.1\r\n" % path
        request += "Host: %s\r\n" % Host
        request += "\r\n"
        # send out the request
        con.sendall(request)
        data = self.recvall(con)
        code = self.get_code(data)
        body = self.get_body(data)

        #print(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, port, path = self.parseURL(url)
        if port == 80:
            Host = host
        else:
            Host = host+":"+str(port)
        con = self.connect(host, port)
        # form the request
        request = "POST %s HTTP/1.1\r\n" % path
        request += "Host: %s\r\n" % Host
        if args:
            requestBody = self.encode(args)
            request += "Content-Length: %d\r\n" % len(requestBody)
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
            request += "\r\n"
            request += requestBody+"\r\n"
        else:
            request += "\r\n"
        # send out the request
        con.sendall(request)
        data = self.recvall(con)
        code = self.get_code(data)
        body = self.get_body(data)

       # print(data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

    def parseURL(self,url):
        start = url.index("http://")
        mainPart = url[start+7:]
        try:
            slashIndex = mainPart.index("/")
            path = mainPart[slashIndex:]
            mainPart = mainPart[:slashIndex]
            try:
                colon = mainPart.index(":")
                host = mainPart[:colon]
                port = int(mainPart[colon + 1:])
            except ValueError:
                host = mainPart
                port = 80

        except ValueError:
            path = "/"
            try:
                colon = mainPart.index(":")
                host = mainPart[:colon]
                port = int(mainPart[colon+1:])
            except ValueError:
                host = mainPart
                port = 80
        return host,port,path

    def encode(self,args):
        return urllib.urlencode(args)
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
