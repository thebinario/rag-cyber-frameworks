dirb | Kali Linux Tools
 DIRECTORY: http://192.168.1.224/.svn/
+ http://192.168.1.224/.svn/entries (CODE:200|SIZE:2726)
+ http://192.168.1.224/cgi-bin/ (CODE:403|SIZE:1122)
==> DIRECTORY: http://192.168.1.224/config/
==> DIRECTORY: http://192.168.1.224/docs/
==> DIRECTORY: http://192.168.1.224/external/
"> DIRECTORY: http://192.168.1.224/.svn/
+ http://192.168.1.224/.svn/entries (CODE:200|SIZE:2726)
+ http://192.168.1.224/cgi-bin/ (CODE:403|SIZE:1122)
==> DIRECTORY: http://192.168.1.224/config/
==> DIRECTORY: http://192.168.1.224/docs/
==> DIRECTORY: http://192.168.1.224/external/
"> DIRECTORY: http://192.168.1.224/.svn/
+ http://192.168.1.224/.svn/entries (CODE:200|SIZE:2726)
+ http://192.168.1.224/cgi-bin/ (CODE:403|SIZE:1122)
==> DIRECTORY: http://192.168.1.224/config/
==> DIRECTORY: http://192.168.1.224/docs/
==> DIRECTORY: http://192.168.1.224/external/
"> DIRECTORY: http://192.168.1.224/.svn/
+ http://192.168.1.224/.svn/entries (CODE:200|SIZE:2726)
+ http://192.168.1.224/cgi-bin/ (CODE:403|SIZE:1122)
==> DIRECTORY: http://192.168.1.224/config/
==> DIRECTORY: http://192.168.1.224/docs/
==> DIRECTORY: http://192.168.1.224/external/
">Join Free CTF
Get Kali
Blog
Documentation Documentation Pages
Tools Documentation
Frequently Asked Questions
Known Issues

Community Community Support
Forums
Discord
Join Newsletter
Mirror Location
Get Involved

Courses
Developers Git Repositories
Packages
Auto Package Test
Bug Tracker
Kali NetHunter Stats

About Kali Linux Overview
Press Pack
Wallpapers
Kali Swag Store
Meet The Kali Team
Partnerships
Contact Us


dirb


version: 2.22 arch: any dirb Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:web


Tool Documentation
Packages & Binaries

dirbdirb
dirb-gendict
html2dic
Learn more with OffSec
web-200
pen-200
LIGHT

DARK
Tool Documentation:
dirb Usage Example
Scan the web server (http://192.168.1.224/) for directories using a dictionary file (/usr/share/wordlists/dirb/common.txt):
root@kali:~# dirb http://192.168.1.224/ /usr/share/wordlists/dirb/common.txt

-----------------
DIRB v2.21
By The Dark Raver
-----------------

START_TIME: Fri May 16 13:41:45 2014
URL_BASE: http://192.168.1.224/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

-----------------

GENERATED WORDS: 4592

---- Scanning URL: http://192.168.1.224/ ----
==> DIRECTORY: http://192.168.1.224/.svn/
+ http://192.168.1.224/.svn/entries (CODE:200|SIZE:2726)
+ http://192.168.1.224/cgi-bin/ (CODE:403|SIZE:1122)
==> DIRECTORY: http://192.168.1.224/config/
==> DIRECTORY: http://192.168.1.224/docs/
==> DIRECTORY: http://192.168.1.224/external/
Packages and Binaries:
dirb
URL bruteforcing tool
DIRB is a Web Content Scanner. It looks for existing (and/or hidden) Web
Objects. It basically works by launching a dictionary based attack against
a web server and analyzing the responses.
DIRB comes with a set of preconfigured attack wordlists for easy usage but
you can use your custom wordlists. Also DIRB sometimes can be used as a
classic CGI scanner, but remember that it is a content scanner not a
vulnerability scanner.
DIRB’s main purpose is to help in professional web application auditing.
Specially in security related testing. It covers some holes not covered by
classic web vulnerability scanners. DIRB looks for specific web objects that
other generic CGI scanners can’t look for. It doesn’t search vulnerabilities
nor does it look for web contents that can be vulnerable.
Installed size: 1.44 MB
How to install: sudo apt install dirb
Dependencies:libc6
libcurl4t64

dirb
Web Content Scanner
root@kali:~# man dirb
DIRB(1)                     General Commands Manual                     DIRB(1)

NAME
       dirb - Web Content Scanner

SYNOPSIS
       dirb <url_base> <url_base> [<wordlist_file(s)>] [options]

DESCRIPTION
       DIRB IS a Web Content Scanner. It looks for existing (and/or hidden) Web
       Objects.  It  basically  works  by  launching a dictionary basesd attack
       against a web server and analizing the response.

OPTIONS
       -a <agent_string>
              Specify your custom USER_AGENT.  (Default is: "Mozilla/4.0  (com-
              patible; MSIE 6.0; Windows NT 5.1)")

       -b     Don't squash or merge sequences of /../ or /./ in the given URL.

       -c <cookie_string>
              Set a cookie for the HTTP request.

       -E <certificate>
              Use the specified client certificate file.

       -f     Fine tunning of NOT_FOUND (404) detection.

       -H <header_string>
              Add a custom header to the HTTP request.

       -i     Use case-insensitive Search.

       -l     Print "Location" header when found.

       -N <nf_code>
              Ignore responses with this HTTP code.

       -o <output_file>
              Save output to disk.

       -p <proxy[:port]>
              Use this proxy. (Default port is 1080)

       -P <proxy_username:proxy_password>
              Proxy Authentication.

       -r     Don't Search Recursively.

       -R     Interactive  Recursion.   (Ask  in  which directories you want to
              scan)

       -S     Silent Mode. Don't show tested words. (For dumb terminals)

       -t     Don't force an ending '/' on URLs.

       -u <username:password>
              Username and password to use.

       -v     Show Also Not Existent Pages.

       -w     Don't Stop on WARNING messages.

       -x <extensions_file>
              Amplify search with the extensions on this file.

       -X <extensions>
              Amplify search with this extensions.

       -z <milisecs>
              Amplify search with this extensions.

SEE ALSO
       brain(x)

The Dark Raver                     27/01/2009                           DIRB(1)
dirb-gendict
Generate dictionary incrementally
root@kali:~# dirb-gendict -h
Usage: dirb-gendict -type pattern
  type: -n numeric [0-9]
        -c character [a-z]
        -C uppercase character [A-Z]
        -h hexa [0-f]
        -a alfanumeric [0-9a-z]
        -s case sensitive alfanumeric [0-9a-zA-Z]
  pattern: Must be an ascii string in which every 'X' character wildcard
           will be replaced with the incremental value.

Example: dirb-gendict -n thisword_X
  thisword_0
  thisword_1
  [...]
  thisword_9
html2dic
Dump word dictionary from html input file
root@kali:~# man html2dic
HTML2DIC(1)                 General Commands Manual                 HTML2DIC(1)

NAME
       html2dic - Dump word dictionary from html input file

SYNOPSIS
       html2dic <file>

DESCRIPTION
       html2dic extract all words from an HTML page, generating a dictionary of
       all word found, one word per line.  Output is printed on stdout.

SEE ALSO
       dirb(1),dirb-gendict(1)

Philippe Thierry                   15/06/2017                       HTML2DIC(1)


Learn more with OffSec
Want to learn more about dirb? get access to in-depth training and hands-on labs:
WEB-200: 2.2.5. Web Application Enumeration Methodology: Automated HTTP Endpoint Discovery
WEB-200 course

PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

dhcpig
dirbuster


LIGHT

DARK
Links
Home
Download / Get Kali
Blog
OS Documentation
Tool Documentation
System Status
Archived Releases
Partnerships
Platforms
ARM (SBC)
NetHunter (Mobile)

Amazon AWS

Docker

Linode

Microsoft Azure

Microsoft Store (WSL)

Vagrant
Development
Bug Tracker
Continuous Integration
Network Mirror
Package Tracker

GitLab
Community

Discord
Support Forum

PeerTube
Follow Us

Bluesky

Facebook

Instagram

Mastodon

Substack

X

Newsletter

RSS
Policies
Cookie Policy
Privacy Policy
Trademark Policy

© OffSec Services Limited 2026. All rights reserved.

Kali Linux is part of OffSec's Community Projects
Learn more about OffSec's free, open-source penetration testing tools for cybersecurity professionals