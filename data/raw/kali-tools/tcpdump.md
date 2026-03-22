tcpdump | Kali Linux Tools
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


tcpdump


version: 4.99.6 arch: any tcpdump Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:forensics
information-gathering
respond
sniffing-spoofing


Packages & Binaries

tcpdumptcpdump
Learn more with OffSec
pen-200
LIGHT

DARK
Packages and Binaries:
tcpdump
Command-line network traffic analyzer
This program allows you to dump the traffic on a network. tcpdump
is able to examine IPv4, ICMPv4, IPv6, ICMPv6, UDP, TCP, SNMP, AFS
BGP, RIP, PIM, DVMRP, IGMP, SMB, OSPF, NFS and many other packet
types.
It can be used to print out the headers of packets on a network
interface, filter packets that match a certain expression. You can
use this tool to track down network problems, to detect attacks
or to monitor network activities.
Installed size: 1.31 MB
How to install: sudo apt install tcpdump
Dependencies:libc6
libpcap0.8t64
libssl3t64
systemd | systemd-standalone-sysusers | systemd-sysusers

tcpdump
Dump traffic on a network
root@kali:~# tcpdump -h
tcpdump version 4.99.6
libpcap version 1.10.6 (64-bit time_t, with TPACKET_V3)
OpenSSL 3.5.5 27 Jan 2026
64-bit build, 64-bit time_t
Usage: tcpdump [-AbdDefghHIJKlLnNOpqStuUvxX#] [ -B size ] [ -c count ] [--count]
		[ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
		[ -i interface ] [ --immediate-mode ] [ -j tstamptype ]
		[ -M secret ] [ --number ] [ --print ] [ -Q in|out|inout ]
		[ -r file ] [ -s snaplen ] [ -T type ] [ --version ]
		[ -V file ] [ -w file ] [ -W filecount ] [ -y datalinktype ]
		[ --time-stamp-precision precision ] [ --micro ] [ --nano ]
		[ -z postrotate-command ] [ -Z user ] [ expression ]


Learn more with OffSec
Want to learn more about tcpdump? get access to in-depth training and hands-on labs:
PEN-200: 18.2.2. Linux Privilege Escalation: Inspecting Service Footprints
PEN-200: 20. Tunneling Through Deep Packet Inspection
Digital Forensics Foundations: 6.2.2. Network Forensics: Tcpdump and Wireshark
IT Generalist Common Tools: 1.4. Wireshark Essentials: Remote Packet Capture
Network Penetration Testing Essentials: 6.5.2. Networking Fundamentals: Tcpdump
PEN-200 course


Updated on: 2026-Mar-13

 Edit this page

sudo
tlssled


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