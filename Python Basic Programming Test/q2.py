import socket
import urllib2

try:
    # try opening google
    page = urllib2.urlopen("http://google.com/")
    # get the ip
    ip = socket.gethostbyname(socket.gethostname())
    print("This PCs IP Address is: " + ip)
except urllib2.URLError:
    # opening the page failed
    print("Not connected")