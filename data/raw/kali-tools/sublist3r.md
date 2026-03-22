sublist3r | Kali Linux Tools
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


sublist3r


version: 1.1 arch: all sublist3r Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
everything


Tool Documentation
Packages & Binaries

sublist3rsublist3r

LIGHT

DARK
Tool Documentation:
sublist3r Usage Examples
Search for subdomains of kali.org (-d kali.org) using the Bing search engine (-e bing) with 3 threads (-t 3).
root@kali:~# sublist3r -d kali.org -t 3 -e bing

                 ____        _     _ _     _   _____
                / ___| _   _| |__ | (_)___| |_|___ / _ __
                \___ \| | | | '_ \| | / __| __| |_ \| '__|
                 ___) | |_| | |_) | | \__ \ |_ ___) | |
                |____/ \__,_|_.__/|_|_|___/\__|____/|_|

                # Coded By Ahmed Aboul-Ela - @aboul3la

[-] Enumerating subdomains now for kali.org
[-] Searching now in Bing..
[-] Total Unique Subdomains Found: 19
www.kali.org
archive-3.kali.org
archive-4.kali.org
archive-5.kali.org
bugs.kali.org
cdimage.kali.org
docs.kali.org
ar.docs.kali.org
he.docs.kali.org
id.docs.kali.org
tr.docs.kali.org
forums.kali.org
git.kali.org
http.kali.org
images.kali.org
pkg.kali.org
repo.kali.org
security.kali.org
tools.kali.org
Packages and Binaries:
sublist3r
Fast subdomains enumeration tool for penetration testers
This package contains a Python security tool designed to enumerate subdomains
of websites using OSINT. It helps penetration testers and bug hunters collect
and gather subdomains for the domain they are targeting over the network.
Sublist3r enumerates subdomains using many search engines such as Google,
Yahoo, Bing, Baidu, and Ask. Sublist3r also enumerates subdomains using
Netcraft, Virustotal, ThreatCrowd, DNSdumpster, and ReverseDNS.
Subbrute was integrated with Sublist3r to increase the possibility of finding
more subdomains using bruteforce with an improved wordlist.
Installed size: 1.85 MB
How to install: sudo apt install sublist3r
Dependencies:python3
python3 | python3-supported-max | python3-supported-min
python3-dnspython
python3-requests

sublist3r
Tool designed to enumerate subdomains of websites using OSINT
root@kali:~# sublist3r -h
usage: sublist3r [-h] -d DOMAIN [-b [BRUTEFORCE]] [-p PORTS] [-v [VERBOSE]]
                 [-t THREADS] [-e ENGINES] [-o OUTPUT] [-n]

OPTIONS:
  -h, --help            show this help message and exit
  -d, --domain DOMAIN   Domain name to enumerate it's subdomains
  -b, --bruteforce [BRUTEFORCE]
                        Enable the subbrute bruteforce module
  -p, --ports PORTS     Scan the found subdomains against specified tcp ports
  -v, --verbose [VERBOSE]
                        Enable Verbosity and display results in realtime
  -t, --threads THREADS
                        Number of threads to use for subbrute bruteforce
  -e, --engines ENGINES
                        Specify a comma-separated list of search engines
  -o, --output OUTPUT   Save the results to text file
  -n, --no-color        Output without color

Example: python3 /usr/bin/sublist3r -d google.com


Updated on: 2026-Mar-02

 Edit this page

subfinder
subversion


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