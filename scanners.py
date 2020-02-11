import logging
import random
import telnetlib
import urllib.request
from ftplib import FTP


# Scanners handler class
# Manage scanners' activity through this class.
class Scanner:
    # Init
    # Args : s=settings object
    def __init__(self, s):
        self.s = []
        self.s.append(WEBScanner())
        self.s.append(FTPScanner())
        self.s.append(TELNETScanner())

        self.bl = []
        self.results = []

        t = int(s.get('Core', 'timeout'))
        for s in self.s:
            s.timeout = t

    # Get actives
    # Return a list of all active scanners.
    # Args : None
    def get_actives(self):
        r = []
        for s in self.s:
            if s.active is True:
                r.append(s)
        return r

    # Activate
    # Manually activate a scanner.
    # Args : v=scanner class name
    def activate(self, v):
        for s in self.s:
            if s.__class__.__name__ == v:
                s.active = True
                return True
        return False

    # Scan
    # Scan an internet address with all active scanners.
    # Args : v=address, b=behavior
    def scan(self, v, b):
        if v not in self.bl:
            if b is 0: # Random
                s = random.choice(self.get_actives())
                r = s.check(v)
                if r is not None:
                    logging.info(u"F " + str(r.p) + " @ " + str(r.rv))
                    self.results.append(r)
                else:
                    self.bl.append(v)

            elif b is 1: # Intelligent
                s = random.choice(self.get_actives())
                r = s.check(v)
                if r is not None:
                    logging.info(u"F " + str(r.p) + " @ " + str(r.rv))
                    self.results.append(r)
                    ga = self.get_actives()
                    ga.remove(s)
                    for sc in ga:
                        r = sc.check(v)
                        if r is not None:
                            logging.info(u"F " + str(r.p) + " @ " + str(r.rv))
                            self.results.append(r)
                self.bl.append(v)

            elif b is 2: # Complete
                for s in self.get_actives():
                    r = s.check(v)
                    if r is not None:
                        logging.info(u"F " + str(r.p) + " @ " + str(r.rv))
                        self.results.append(r)
                    else:
                        self.bl.append(v)
        return

    # To string
    # Return list of scanners loaded as a string.
    # Args : None
    def tostring(self):
        r = ""
        for s in self.get_actives():
            r += s.__class__.__name__ + " "
        return r


# Result class
# Class to hold results' data.
class Result:
    # Init
    # Args : v=url, rv=address, protocol, str=string displayed to user
    def __init__(self, v, rv, protocol, str):
        self.v = v
        self.rv = rv
        self.p = protocol
        self.str = str


# Base class for scanners
# Specific scanners are inherited from that class
class aScanner:
    # Init
    # Args : None
    def __init__(self):
        self.active = False
        self.timeout = 0


# Web http(s) scanner class
# Scans an address for http/https protocol.
class WEBScanner(aScanner):
    # Init
    # Args : None
    def __init__(self):
        aScanner.__init__(self)

    # Check
    # Return result if found something.
    # Args : v=address
    def check(self, v):
        vi = "https://" + v
        try:
            raw = urllib.request.urlopen(vi, timeout=self.timeout).read()
            return Result(vi, v, 'https', 'a web server')
        except:
            vi = "http://" + v
            try:
                raw = urllib.request.urlopen(vi, timeout=self.timeout).read()
                return Result(vi, v, 'http', 'a web server')
            except:
                return None


# FTP scanner class
# Scans an address for ftp protocol.
class FTPScanner(aScanner):
    # Init
    # Args : None
    def __init__(self):
        aScanner.__init__(self)
        self.exclude = ['.', '..', 'pub', 'incoming', 'robots.txt']

    # Check
    # Return result if found something.
    # Args : v=address
    def check(self, v):
        try:
            ftp = FTP(v, timeout=self.timeout)
            ftp.login()
            filenames = ftp.nlst()
            for x in self.exclude:
                if x in filenames:
                    filenames.remove(x)
            if len(filenames) > 0:
                return Result('ftp://' + v, v, 'ftp', 'a ftp server')
        except:
            return None
        return None


# Telnet scanner class
# Scans an address for an telnet access.
class TELNETScanner(aScanner):
    # Init
    # Args : None
    def __init__(self):
        aScanner.__init__(self)

    # Check
    # Return result if found something.
    # Args : v=address
    def check(self, v):
        try:
            tn = telnetlib.Telnet(v, timeout=self.timeout)
            tn.close()
            return Result('telnet '+v, v, 'telnet', 'a telnet host')
        except:
            pass
        return None