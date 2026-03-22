netcat | Kali Linux Tools
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


netcat


version: 1.10 arch: any netcat Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:information-gathering
vulnerability


Packages & Binaries

netcat-traditionalnc.traditional
Learn more with OffSec
pen-200
LIGHT

DARK
Packages and Binaries:
netcat-traditional
TCP/IP swiss army knife
A simple Unix utility which reads and writes data across network
connections using TCP or UDP protocol. It is designed to be a reliable
“back-end” tool that can be used directly or easily driven by other
programs and scripts. At the same time it is a feature-rich network
debugging and exploration tool, since it can create almost any kind
of connection you would need and has several interesting built-in
capabilities.
This is the “classic” netcat, written by Hobbit. It lacks many
features found in netcat-openbsd.
Installed size: 139 KB
How to install: sudo apt install netcat-traditional
Dependencies:libc6

nc.traditional
TCP/IP swiss army knife
root@kali:~# nc.traditional -h
[v1.10-50.1]
connect to somewhere:	nc [-options] hostname port[s] [ports] ...
listen for inbound:	nc -l -p port [-options] [hostname] [port]
options:
	-c shell commands	as `-e'; use /bin/sh to exec [dangerous!!]
	-e filename		program to exec after connect [dangerous!!]
	-b			allow broadcasts
	-g gateway		source-routing hop point[s], up to 8
	-G num			source-routing pointer: 4, 8, 12, ...
	-h			this cruft
	-i secs			delay interval for lines sent, ports scanned
        -k                      set keepalive option on socket
	-l			listen mode, for inbound connects
	-n			numeric-only IP addresses, no DNS
	-o file			hex dump of traffic
	-p port			local port number
	-r			randomize local and remote ports
	-q secs			quit after EOF on stdin and delay of secs
	-s addr			local source address
	-T tos			set Type Of Service
	-t			answer TELNET negotiation
	-u			UDP mode
	-v			verbose [use twice to be more verbose]
	-w secs			timeout for connects and final net reads
	-C			Send CRLF as line-ending
	-z			zero-I/O mode [used for scanning]
port numbers can be individual or ranges: lo-hi [inclusive];
hyphens in port names must be backslash escaped (e.g. 'ftp\-data').


Learn more with OffSec
Want to learn more about netcat? get access to in-depth training and hands-on labs:
PEN-200: 6.4.2. Information Gathering: TCP/UDP Port Scanning Theory
Network Penetration Testing Essentials: 19.2.2. File Transfers: Netcat
Network Penetration Testing Essentials: 10.6. Linux Networking and Services I: Netcat (nc)
Security Operations Essentials: 8.6. Linux Networking and Services I: Netcat (nc)
Network Penetration Testing Essentials: 14.2.1. Working with Shells
Network Penetration Testing Essentials: 14.2.1. Working with Shells: Netcat Shells
PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

netbase
netdiscover


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