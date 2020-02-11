import random
import socket
import struct

import gibberish


# Generator handler class
# Manage generators' activity through this class.
class Generator:
    # Init
    # Args : s=settings object
    def __init__(self, s):
        self.g = []
        self.g.append(IPv4Generator())
        self.g.append(WordGenerator())

    # Get actives
    # Return a list of all active generators.
    # Args : None
    def get_actives(self):
        r = []
        for g in self.g:
            if g.active is True:
                r.append(g)
        return r

    # Activate
    # Manually activate a generator.
    # Args : v=generator class name
    def activate(self, v):
        for g in self.g:
            if g.__class__.__name__ == v:
                g.active = True
                return True
        return False

    # Generate
    # Generate an internet address with a random generator.
    # Args : None
    def generate(self):
        return random.choice(self.get_actives()).generate()

    # To string
    # Return list of generators loaded as a string.
    # Args : None
    def tostring(self):
        r = ""
        for g in self.get_actives():
            r += g.__class__.__name__ + " "
        return r


# Base class for generators
# Specific generators are inherited from that class
class aGenerator:
    # Init
    # Args : None
    def __init__(self):
        self.active = False
        self.max = 0


# IP address generator class
# Generates IP addresses.
class IPv4Generator(aGenerator):
    # Init
    # Args : None
    def __init__(self):
        aGenerator.__init__(self)
        self.max = (255**4)

    # Generate
    # Generate a random IP address.
    # Args : None
    def generate(self):
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

# WordGenerator
# Generates pseudo-words URLs.
class WordGenerator(aGenerator):
    # Init
    # Args : None
    def __init__(self):
        aGenerator.__init__(self)
        self.ext = [".com", ".org", ".net"]

    # Generate
    # Generate a few random words to make an URL.
    # Args : None
    def generate(self):
        return "".join(gibberish.generate_words(random.randint(2,4))) + random.choice(self.ext)
