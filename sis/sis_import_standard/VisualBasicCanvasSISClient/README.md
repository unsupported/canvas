Windows-based SIS Integration Examples
======

This client is a Visual Basic .Net client for integrating an SIS
with Canvas. It makes use of the System.WebClient class and is
extremely simple. It should be noted that only the most basic error
handling is implemented: keep that in mind if you choose to use this
in production.

This client is a console-only, terminal-driven application that
accepts 4 arguments:

Canvas Hostname: (i.e. https://canvas.instructure.com)
Canvas Account ID: (i.e. 12345)
Access Token: (i.e. abc123...)
File Path: (i.e. C:\path\to\file)

These are provided from the terminal in that order, space separated.
The application will output basic status (the URL, etc.) as it runs.
It will also output the entire response from Canvas. This response
will, unless errors arise, be JSON-encoded and can easily be parsed.

As always, this is provided AS-IS, without warranty, and without any
support beyond this document and anyone kind enough to help from the
community.

Installation
======

Please checkout this repository (canvas-contrib) to your local dev
environment and open "Canvas SIS Client.sln" in Visual Studio 2010.
At this time, only VS 2010 is supported.

Support
======

This is an unsupported, community-created project. Keep that in 
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.

Good luck!