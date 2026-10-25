Your Day 3 results match what we expected:

Image	On disk	Compressed	What it shows
full	1.67 GB	428 MB	Full Python base, about 7× bigger
v1	245 MB	58.9 MB	Slim base, the original
v3 / bad / v13	248 MB	59.4 MB	Slim with httpx added, about 3 MB more
multi	252 MB	60 MB	Multi-stage with a non-root user

Takeaways for your notes:

The base image matters most. Switching from python:3.12 to -slim saved about 1.4 GB. Nothing else comes close.
bad and good are the same size. The wrong layer order costs build time, not size. That’s what your Day 2 timing showed.
multi is slightly bigger than v1, not smaller. That’s normal here. The venv carries its own copy of pip, and the new user adds a home folder. Your app has no compilers or build tools for the builder stage to leave behind, so there’s nothing to trim. Multi-stage pays off for apps that compile things, like many ML libraries. Today’s real win is the non-root user.