# OpenLeecher

### What does it do?

OpenLeecher is a CLI/GUI tool for scanning Internet. It has no useful purpose except to be lost on the world wide web.
It scans random generated addresses with the hope to find content, depending how you set up the session.

Imagine the internet as a big city, full of houses. Each house is someone's router, its own internet connection. Houses are usually locked, but some of them aren't : there could be a website inside them, so the owner would want people from outside his house to be able to visit inside.
Also, sometimes, owners just don't know how to lock a door.

What OpenLeecher does, it chooses a random house and ring the bell. If no one answers, it moves to the next. Simple as that.


### How does it work?

There is two main parts of this software : generators, and scanners. Generators output addresses (find houses), while scanners try to talk to them on different protocols (ring bells).
If something is found, it will be displayed, and logged. The GUI makes it easier to just preview content without opening an external program.


Second thing is the threads. Checking one house at a time would take a ton of time, and we wouldn't be truly exploiting a computer's resources.
That's why we use threads to ring multiple bells at a time. The maximum number of threads can be adjusted in real-time, even when the program has already started a session.


### Usage

For CLI, run `openleecher -h` to get the help, displaying all available arguments.

For GUI, run `openleecher --gui`.

**CLI is not available on Windows. Running the script and/or the binary will launch the GUI.**