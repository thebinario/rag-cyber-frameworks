whatweb | Kali Linux Tools
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


whatweb


version: 0.6.3 arch: all whatweb Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:information-gathering
vulnerability
web


Tool Documentation
Packages & Binaries

whatwebwhatweb
Learn more with OffSec
pen-200
LIGHT

DARK
Tool Documentation:
WhatWeb Usage Example
root@kali:~# whatweb -v -a 3 192.168.0.102
WhatWeb report for http://192.168.0.102
Status    : 200 OK
Title     : Toolz TestBed
IP        : 192.168.0.102
Country   : RESERVED, ZZ

Summary   : JQuery, Script, X-UA-Compatible[IE=edge], HTML5, Apache[2.2,2.2.22], HTTPServer[Ubuntu Linux][Apache/2.2.22 (Ubuntu)]

Detected Plugins:
[ Apache ]
  The Apache HTTP Server Project is an effort to develop and
  maintain an open-source HTTP server for modern operating
  systems including UNIX and Windows NT. The goal of this
  project is to provide a secure, efficient and extensible
  server that provides HTTP services in sync with the current
  HTTP standards.

  Version      : 2.2.22 (from HTTP Server Header)
  Version      : 2.2
  Version      : 2.2
  Google Dorks: (3)
  Website     : http://httpd.apache.org/

[ HTML5 ]
  HTML version 5, detected by the doctype declaration


[ HTTPServer ]
  HTTP server header string. This plugin also attempts to
  identify the operating system from the server header.

  OS           : Ubuntu Linux
  String       : Apache/2.2.22 (Ubuntu) (from server string)

[ JQuery ]
  A fast, concise, JavaScript that simplifies how to traverse
  HTML documents, handle events, perform animations, and add
  AJAX.

  Website     : http://jquery.com/

[ Script ]
  This plugin detects instances of script HTML elements and
  returns the script language/type.


[ X-UA-Compatible ]
  This plugin retrieves the X-UA-Compatible value from the
  HTTP header and meta http-equiv tag. - More Info:
  http://msdn.microsoft.com/en-us/library/cc817574.aspx

  String       : IE=edge

HTTP Headers:
  HTTP/1.1 200 OK
  Server: Apache/2.2.22 (Ubuntu)
  Last-Modified: Fri, 02 Feb 2018 15:27:56 GMT
  ETag: "11f-2e38-5643c5b56a8d3"
  Accept-Ranges: bytes
  Vary: Accept-Encoding
  Content-Encoding: gzip
  Content-Length: 3541
  Connection: close
  Content-Type: text/html

root@kali:~#
Packages and Binaries:
whatweb
Next generation web scanner
WhatWeb identifies websites. It recognises web technologies including
content management systems (CMS), blogging platforms, statistic/analytics
packages, JavaScript libraries, web servers, and embedded devices.
WhatWeb has over 900 plugins, each to recognise something different.
It also identifies version numbers, email addresses, account IDs,
web framework modules, SQL errors, and more.
Installed size: 18.75 MB
How to install: sudo apt install whatweb
Dependencies:ruby
ruby-addressable
ruby-ipaddress

whatweb
Next generation Web scanner. Identify technologies used by websites.
root@kali:~# whatweb -h

.$$$     $.                                   .$$$     $.
$$$$     $$. .$$$  $$$ .$$$$$$.  .$$$$$$$$$$. $$$$     $$. .$$$$$$$. .$$$$$$.
$ $$     $$$ $ $$  $$$ $ $$$$$$. $$$$$ $$$$$$ $ $$     $$$ $ $$   $$ $ $$$$$$.
$ `$     $$$ $ `$  $$$ $ `$  $$$ $$' $ `$ `$$ $ `$     $$$ $ `$      $ `$  $$$'
$. $     $$$ $. $$$$$$ $. $$$$$$ `$  $. $  :' $. $     $$$ $. $$$$   $. $$$$$.
$::$  .  $$$ $::$  $$$ $::$  $$$     $::$     $::$  .  $$$ $::$      $::$  $$$$
$;;$ $$$ $$$ $;;$  $$$ $;;$  $$$     $;;$     $;;$ $$$ $$$ $;;$      $;;$  $$$$
$$$$$$ $$$$$ $$$$  $$$ $$$$  $$$     $$$$     $$$$$$ $$$$$ $$$$$$$$$ $$$$$$$$$'


WhatWeb - Next generation web scanner version 0.6.3.
Developed by Andrew Horton (urbanadventurer) and Brendan Coles (bcoles).
Homepage: https://morningstarsecurity.com/research/whatweb

Usage: whatweb [options] <URLs>

TARGET SELECTION:
  <TARGETs>			Enter URLs, hostnames, IP addresses, filenames or
  				IP ranges in CIDR, x.x.x-x, or x.x.x.x-x.x.x.x
  				format.
  --input-file=FILE, -i		Read targets from a file. You can pipe
				hostnames or URLs directly with -i /dev/stdin.

TARGET MODIFICATION:
  --url-prefix			Add a prefix to target URLs.
  --url-suffix			Add a suffix to target URLs.
  --url-pattern			Insert the targets into a URL.
				e.g. example.com/%insert%/robots.txt

AGGRESSION:
The aggression level controls the trade-off between speed/stealth and
reliability.
  --aggression, -a=LEVEL	Set the aggression level. Default: 1.
  1. Stealthy			Makes one HTTP request per target and also
  				follows redirects.
  3. Aggressive			If a level 1 plugin is matched, additional
  				requests will be made.
  4. Heavy			Makes a lot of HTTP requests per target. URLs
  				from all plugins are attempted.

HTTP OPTIONS:
  --user-agent, -U=AGENT	Identify as AGENT instead of WhatWeb/0.6.3.
  --header, -H			Add an HTTP header. eg "Foo:Bar". Specifying a
				default header will replace it. Specifying an
				empty value, e.g. "User-Agent:" will remove it.
  --follow-redirect=WHEN	Control when to follow redirects. WHEN may be
				`never', `http-only', `meta-only', `same-site',
				or `always'. Default: always.
  --max-redirects=NUM		Maximum number of redirects. Default: 10.

AUTHENTICATION:
  --user, -u=<user:password>	HTTP basic authentication.
  --cookie, -c=COOKIES		Use cookies, e.g. 'name=value; name2=value2'.
  --cookie-jar=FILE		Read cookies from a file and save cookies to the
				same file. Creates the file if it doesn't exist.
  --no-cookies			Disable automatic cookie handling (improves performance with high thread counts).

PROXY:
  --proxy			<hostname[:port]> Set proxy hostname and port.
				Default: 8080.
  --proxy-user			<username:password> Set proxy user and password.

PLUGINS:
  --list-plugins, -l		List all plugins.
  --info-plugins, -I=[SEARCH]	List all plugins with detailed information.
				Optionally search with keywords in a comma
				delimited list.
  --search-plugins=STRING	Search plugins for a keyword.
  --plugins, -p=LIST		Select plugins. LIST is a comma delimited set
				of selected plugins. Default is all.
				Each element can be a directory, file or plugin
				name and can optionally have a modifier, +/-.
				Examples: +/tmp/moo.rb,+/tmp/foo.rb
				title,md5,+./plugins-disabled/
				./plugins-disabled,-md5
				-p + is a shortcut for -p +plugins-disabled.
  --grep, -g=STRING|REGEXP	Search for STRING or a Regular Expression. Shows
				only the results that match.
				Examples: --grep "hello"
				--grep "/he[l]*o/"
  --custom-plugin=DEFINITION	Define a custom plugin named Custom-Plugin,
				Examples: ":text=>'powered by abc'"
				":version=>/powered[ ]?by ab[0-9]/"
				":ghdb=>'intitle:abc \"powered by abc\"'"
				":md5=>'8666257030b94d3bdb46e05945f60b42'"
				"{:text=>'powered by abc'}"
  --dorks=PLUGIN		List Google dorks for the selected plugin.

OUTPUT:
  --verbose, -v			Verbose output includes plugin descriptions.
				Use twice for debugging.
  --colour,--color=WHEN		control whether colour is used. WHEN may be
				`never', `always', or `auto'.
  --quiet, -q			Do not display brief logging to STDOUT.
  --no-errors			Suppress error messages.

LOGGING:
  --log-brief=FILE		Log brief, one-line output.
  --log-verbose=FILE		Log verbose output.
  --log-errors=FILE		Log errors.
  --log-xml=FILE		Log XML format.
  --log-json=FILE		Log JSON format.
  --log-sql=FILE		Log SQL INSERT statements.
  --log-sql-create=FILE		Create SQL database tables.
  --log-json-verbose=FILE	Log JSON Verbose format.
  --log-magictree=FILE		Log MagicTree XML format.
  --log-object=FILE		Log Ruby object inspection format.
  --log-mongo-database		Name of the MongoDB database.
  --log-mongo-collection	Name of the MongoDB collection.
				Default: whatweb.
  --log-mongo-host		MongoDB hostname or IP address.
				Default: 0.0.0.0.
  --log-mongo-username		MongoDB username. Default: nil.
  --log-mongo-password		MongoDB password. Default: nil.
  --log-elastic-index		Name of the index to store results. Default: whatweb
  --log-elastic-host		Host:port of the elastic http interface. Default: 127.0.0.1:9200

PERFORMANCE & STABILITY:
  --max-threads, -t		Number of simultaneous threads. Default: 25.
  --open-timeout		Time in seconds. Default: 15.
  --read-timeout		Time in seconds. Default: 30.
  --wait=SECONDS		Wait SECONDS between connections.
				This is useful when using a single thread.

HELP & MISCELLANEOUS:
  --short-help			Short usage help.
  --help, -h			Complete usage help.
  --debug			Raise errors in plugins.
  --version			Display version information.

EXAMPLE USAGE:
* Scan example.com.
  ./whatweb example.com

* Scan reddit.com slashdot.org with verbose plugin descriptions.
  ./whatweb -v reddit.com slashdot.org

* An aggressive scan of wired.com detects the exact version of WordPress.
  ./whatweb -a 3 www.wired.com

* Scan the local network quickly and suppress errors.
  whatweb --no-errors 192.168.0.0/24

* Scan the local network for https websites.
  whatweb --no-errors --url-prefix https:// 192.168.0.0/24

* Scan for crossdomain policies in the Alexa Top 1000.
  ./whatweb -i plugin-development/alexa-top-100.txt \
  --url-suffix /crossdomain.xml -p crossdomain_xml


Learn more with OffSec
Want to learn more about whatweb? get access to in-depth training and hands-on labs:
PEN-200: 27.1.2. Assembling the Pieces: WEBSRV1
PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

whatmask
wifipumpkin3


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