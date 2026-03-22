wafw00f | Kali Linux Tools
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


wafw00f


version: 2.3.2 arch: all wafw00f Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:information-gathering
vulnerability
web


Packages & Binaries

wafw00fwafw00f

LIGHT

DARK
Packages and Binaries:
wafw00f
Identify and fingerprint Web Application Firewall products
This package identifies and fingerprints Web Application Firewall (WAF)
products using the following logic:
Sends a normal HTTP request and analyses the response; this identifies a
number of WAF solutions.
If that is not successful, it sends a number of (potentially malicious)
HTTP requests and uses simple logic to deduce which WAF it is.
If that is also not successful, it analyses the responses previously
returned and uses another simple algorithm to guess if a WAF or security
solution is actively responding to the attacks.
Installed size: 260 KB
How to install: sudo apt install wafw00f
Dependencies:python3
python3-pluginbase
python3-requests

wafw00f
Identify and fingerprint Web Application Firewall products
root@kali:~# wafw00f -h
Usage: wafw00f url1 [url2 [url3 ... ]]
example: wafw00f http://www.victim.org/

Options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable verbosity, multiple -v options increase
                        verbosity
  -a, --findall         Find all WAFs which match the signatures, do not stop
                        testing on the first one
  -r, --noredirect      Do not follow redirections given by 3xx responses
  -t TEST, --test=TEST  Test for one specific WAF
  -o OUTPUT, --output=OUTPUT
                        Write output to csv, json or text file depending on
                        file extension. For stdout, specify - as filename.
  -f FORMAT, --format=FORMAT
                        Force output format to csv, json or text.
  -i INPUT, --input-file=INPUT
                        Read targets from a file. Input format can be csv,
                        json or text. For csv and json, a `url` column name or
                        element is required.
  -l, --list            List all WAFs that WAFW00F is able to detect
  -p PROXY, --proxy=PROXY
                        Use an HTTP proxy to perform requests, examples:
                        http://hostname:8080, socks5://hostname:1080,
                        http://user:pass@hostname:8080
  -V, --version         Print out the current version of WafW00f and exit.
  -H HEADERS, --headers=HEADERS
                        Pass custom headers via a text file to overwrite the
                        default header set.
  -T TIMEOUT, --timeout=TIMEOUT
                        Set the timeout for the requests.
  --no-colors           Disable ANSI colors in output.


Updated on: 2026-Mar-02

 Edit this page

vinetto
whois


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