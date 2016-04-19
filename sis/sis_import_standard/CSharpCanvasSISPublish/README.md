C-Sharp SIS Integration Examples
======

This client is a starting point for a C# .Net client for integrating an SIS
with Canvas. It makes use of the System.WebClient class as well as a basic JSON parser. 
It should be noted that only the most basic error handling is implemented: keep that in
mind if you choose to use this in production.

This client is a console-only, terminal-driven application that
accepts 4 arguments:

Canvas Hostname: (i.e. https://canvas.instructure.com)
Canvas Account ID: (i.e. 12345)
Access Token: (i.e. abc123...)
File Path: (i.e. C:\path\to\file)

These are provided from the terminal in that order, space separated.
The application will output basic logging as it runs.  It will upload the sis file, then
wait until the sis import is done to exit.

Installation
======

As was stated earlier, this project represents a starting point only.  You will need to
adjust a few files and tweak the project to do exactly what you need.  Particularly, you
will need to do the following:

Edit CanvasSISImport/Program.cs

Change line 12 to reflect the location of the sis files to import.  If you choose to
upload a ZIP file, make sure you change the second argument to "zip" as well.

Edit CanvasSISImport/libs/CanvasSIS.cs

Changes lines 13-15 to have  values for your environment.  Specifically your account id,
subdomain, and API access_token.


Support
======

As always, this is provided AS-IS, without warranty, and without any
support beyond this document and anyone kind enough to help from the
community.

This is an unsupported, community-created project. Keep that in 
mind. Instructure won't be able to help you fix or debug this.
That said, the community will hopefully help support and keep
both the script and this documentation up-to-date.
