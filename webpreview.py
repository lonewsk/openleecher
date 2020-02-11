import telnetlib
from ftplib import FTP

# Web preview class
# Class used to build HTML previews of content for QT Web engine to display
class WebPreview:
    def __init__(self):
        self.pre = """<html>
        <head>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js"></script>
        </head>
        <body style=\"background:white;\">"""
        self.aft = "</body></html>"

    # Loading webpage
    # Display a loading message with url
    # Args u=server's address
    def loading(self, u):
        r = "<h6>Loading "+u+"</h6>"
        return self.pre + r + self.aft

    # Preview ftp
    # Read ftp server and preview it as html
    # Args : u=server's address
    def ftp(self, u):
        depth = 1
        r = "<h5>FTP server @ " + u + "</h5><hr/>"
        try:
            ftp = FTP(u)
            ftp.login()
            filenames = ftp.nlst()
            r += "<b>" + str(len(filenames)) + " files found.</b>"
            r += "<ul class=\"collection\">"
            for f in filenames:
                r += "<li class=\"collection-item\">" + str(f) + "</li>"
            r += "</ul>"
        except:
            r += "<p style=\"color:red;\">Connection aborted.</p>"
        return self.pre + r + self.aft

    # Preview telnet
    # Read telnet server's answer and preview it as html
    # Args : u=server's address
    def telnet(self, u):
        r = "<h5>Telnet @ " + u + "</h5><br/><hr/>"
        try:
            tn = telnetlib.Telnet(u, 23, timeout=5)
            r += tn.read_until(b"login", timeout=5).decode('ascii')
            tn.close()
        except:
            r += "<p style=\"color:red;\">Connection aborted.</p>"
        return self.pre + r + self.aft


    # Load content
    # Return HTML code for a content address
    # Args: url=server's address with protocol, rawurl=direct connect address
    def load(self, url, rawurl):
        if url.startswith('ftp'):
            return self.ftp(rawurl)
        elif url.startswith('telnet'):
            return self.telnet(rawurl)
        return ""
