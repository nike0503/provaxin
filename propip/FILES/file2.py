import telnetlib as tel
import ftplib as ft


def connect(url):
    ftp = ft.FTP(url) 
    ftp.login()

def interact(host,port):
    with tel.Telnet(host, port) as tn:
        tn.interact()

