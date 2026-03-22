wfuzz | Kali Linux Tools
Join Free CTF
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


wfuzz


version: 3.1.0 arch: all wfuzz Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:fuzzing
web


Tool Documentation
Packages & Binaries

wfuzzwfuzz
Learn more with OffSec
web-200
LIGHT

DARK
Tool Documentation:
wfuzz Usage Example
Use colour output (-c), a wordlist as a payload (-z file,/usr/share/wfuzz/wordlist/general/common.txt), and hide 404 messages (–hc 404) to fuzz the given URL (http://192.168.1.202/FUZZ):
root@kali:~# wfuzz -c -z file,/usr/share/wfuzz/wordlist/general/common.txt --hc 404 http://192.168.1.202/FUZZ

********************************************************
* Wfuzz 2.2.11 - The Web Fuzzer                        *
********************************************************

Target: http://192.168.1.202/FUZZ
Payload type: file,/usr/share/wfuzz/wordlist/general/common.txt

Total requests: 950
==================================================================
ID  Response   Lines      Word         Chars          Request
==================================================================

00429:  C=200      4 L        25 W      177 Ch    " - index"
00466:  C=301      9 L        28 W      319 Ch    " - javascript"
Packages and Binaries:
wfuzz
Web application bruteforcer
Wfuzz is a tool designed for bruteforcing Web Applications,
it can be used for finding resources not linked
directories, servlets, scripts, etc, bruteforce GET and
POST parameters for checking different kind of injections
(SQL, XSS, LDAP,etc), bruteforce Forms parameters
(User/Password), Fuzzing, etc.
Installed size: 1.54 MB
How to install: sudo apt install wfuzz
Dependencies:python3
python3-chardet
python3-legacy-cgi
python3-pycurl
python3-pyparsing

wfuzz
A web application bruteforcer
root@kali:~# wfuzz --help
********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
*                                                      *
* Version up to 1.4c coded by:                         *
* Christian Martorella ([email protected]) *
* Carlos del ojo ([email protected])                   *
*                                                      *
* Version 1.4d to 3.1.0 coded by:                      *
* Xavier Mendez ([email protected])            *
********************************************************

Usage:	wfuzz [options] -z payload,params <url>

	FUZZ, ..., FUZnZ  wherever you put these keywords wfuzz will replace them with the values of the specified payload.
	FUZZ{baseline_value} FUZZ will be replaced by baseline_value. It will be the first request performed and could be used as a base for filtering.


Options:
	-h/--help                 : This help
	--help                    : Advanced help
	--filter-help             : Filter language specification
	--version                 : Wfuzz version details
	-e <type>                 : List of available encoders/payloads/iterators/printers/scripts

	--recipe <filename>       : Reads options from a recipe. Repeat for various recipes.
	--dump-recipe <filename>  : Prints current options as a recipe
	--oF <filename>           : Saves fuzz results to a file. These can be consumed later using the wfuzz payload.

	-c                        : Output with colors
	-v                        : Verbose information.
	-f filename,printer       : Store results in the output file using the specified printer (raw printer if omitted).
	-o printer                : Show results using the specified printer.
	--interact                : (beta) If selected,all key presses are captured. This allows you to interact with the program.
	--dry-run                 : Print the results of applying the requests without actually making any HTTP request.
	--prev                    : Print the previous HTTP requests (only when using payloads generating fuzzresults)
	--efield <expr>           : Show the specified language expression together with the current payload. Repeat for various fields.
	--field <expr>            : Do not show the payload but only the specified language expression. Repeat for various fields.

	-p addr                   : Use Proxy in format ip:port:type. Repeat option for using various proxies.
	                            Where type could be SOCKS4,SOCKS5 or HTTP if omitted.

	-t N                      : Specify the number of concurrent connections (10 default)
	-s N                      : Specify time delay between requests (0 default)
	-R depth                  : Recursive path discovery being depth the maximum recursion level.
	-D depth                  : Maximum link depth level.
	-L,--follow               : Follow HTTP redirections
	--ip host:port            : Specify an IP to connect to instead of the URL's host in the format ip:port
	-Z                        : Scan mode (Connection errors will be ignored).
	--req-delay N             : Sets the maximum time in seconds the request is allowed to take (CURLOPT_TIMEOUT). Default 90.
	--conn-delay N            : Sets the maximum time in seconds the connection phase to the server to take (CURLOPT_CONNECTTIMEOUT). Default 90.

	-A, --AA, --AAA           : Alias for -v -c and --script=default,verbose,discover respectively
	--no-cache                : Disable plugins cache. Every request will be scanned.
	--script=                 : Equivalent to --script=default
	--script=<plugins>        : Runs script's scan. <plugins> is a comma separated list of plugin-files or plugin-categories
	--script-help=<plugins>   : Show help about scripts.
	--script-args n1=v1,...   : Provide arguments to scripts. ie. --script-args grep.regex="<A href=\"(.*?)\">"

	-u url                    : Specify a URL for the request.
	-m iterator               : Specify an iterator for combining payloads (product by default)
	-z payload                : Specify a payload for each FUZZ keyword used in the form of name[,parameter][,encoder].
	                            A list of encoders can be used, ie. md5-sha1. Encoders can be chained, ie. md5@sha1.
	                            Encoders category can be used. ie. url
	                            Use help as a payload to show payload plugin's details (you can filter using --slice)
	--zP <params>             : Arguments for the specified payload (it must be preceded by -z or -w).
	--zD <default>            : Default parameter for the specified payload (it must be preceded by -z or -w).
	--zE <encoder>            : Encoder for the specified payload (it must be preceded by -z or -w).
	--slice <filter>          : Filter payload's elements using the specified expression. It must be preceded by -z.
	-w wordlist               : Specify a wordlist file (alias for -z file,wordlist).
	-V alltype                : All parameters bruteforcing (allvars and allpost). No need for FUZZ keyword.
	-X method                 : Specify an HTTP method for the request, ie. HEAD or FUZZ

	-b cookie                 : Specify a cookie for the requests. Repeat option for various cookies.
	-d postdata               : Use post data (ex: "id=FUZZ&catalogue=1")
	-H header                 : Use header (ex:"Cookie:id=1312321&user=FUZZ"). Repeat option for various headers.
	--basic/ntlm/digest auth  : in format "user:pass" or "FUZZ:FUZZ" or "domain\FUZ2Z:FUZZ"

	--hc/hl/hw/hh N[,N]+      : Hide responses with the specified code/lines/words/chars (Use BBB for taking values from baseline)
	--sc/sl/sw/sh N[,N]+      : Show responses with the specified code/lines/words/chars (Use BBB for taking values from baseline)
	--ss/hs regex             : Show/hide responses with the specified regex within the content
	--filter <filter>         : Show/hide responses using the specified filter expression (Use BBB for taking values from baseline)
	--prefilter <filter>      : Filter items before fuzzing using the specified expression. Repeat for concatenating filters.


Learn more with OffSec
Want to learn more about wfuzz? get access to in-depth training and hands-on labs:
WEB-200: 8.2.5. SQL Injection: Fuzzing
WEB-200: 9.5.3. Directory Traversal Attacks: Fuzzing the Path Parameter
WEB-200 course


Updated on: 2025-Dec-09

 Edit this page

weevely
wget


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