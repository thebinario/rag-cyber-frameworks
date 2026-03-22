fierce | Kali Linux Tools
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


fierce


version: 1.6.0 arch: all fierce Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:information-gathering


Tool Documentation
Packages & Binaries

fiercefierce

LIGHT

DARK
Tool Documentation:
fierce Usage Example
Run a default scan against the target domain (--domain example.com):
root@kali:~# fierce --domain example.com
DNS Servers for example.com:
    b.iana-servers.net
    a.iana-servers.net

Trying zone transfer first...
    Testing b.iana-servers.net
        Request timed out or transfer not allowed.
    Testing a.iana-servers.net
        Request timed out or transfer not allowed.

Unsuccessful in zone transfer (it was worth a shot)
Okay, trying the good old fashioned way... brute force

Checking for wildcard DNS...
Nope. Good.
Now performing 2280 test(s)...
Packages and Binaries:
fierce
Domain DNS scanner
Fierce is a semi-lightweight scanner that helps locate non-contiguous
IP space and hostnames against specified domains. It’s really meant as
a pre-cursor to nmap, unicornscan, nessus, nikto, etc, since all of
those require that you already know what IP space you are looking for.
This does not perform exploitation and does not scan the whole internet
indiscriminately. It is meant specifically to locate likely targets both
inside and outside a corporate network.
Because it uses DNS primarily you will often find mis-configured networks
that leak internal address space. That’s especially useful in targeted malware.
Originally written by RSnake along with others at http://ha.ckers.org/.
This is simply a conversion to Python 3 to simplify and modernize the codebase.
Installed size: 242 KB
How to install: sudo apt install fierce
Dependencies:python3
python3-dnspython

fierce
DNS scanner that helps locate non-contiguous IP space and hostnames against specified domains.
root@kali:~# fierce -h
usage: fierce [-h] [--domain DOMAIN] [--connect] [--wide]
              [--traverse TRAVERSE] [--search SEARCH [SEARCH ...]]
              [--range RANGE] [--delay DELAY]
              [--subdomains SUBDOMAINS [SUBDOMAINS ...] |
              --subdomain-file SUBDOMAIN_FILE]
              [--dns-servers DNS_SERVERS [DNS_SERVERS ...] |
              --dns-file DNS_FILE] [--tcp]

        A DNS reconnaissance tool for locating non-contiguous IP space.


options:
  -h, --help            show this help message and exit
  --domain DOMAIN       domain name to test
  --connect             attempt HTTP connection to non-RFC 1918 hosts
  --wide                scan entire class c of discovered records
  --traverse TRAVERSE   scan NUMBER IPs before and after discovered records. This respects Class C boundaries and won't enter adjacent subnets.
  --search SEARCH [SEARCH ...]
                        filter on these domains when expanding lookup
  --range RANGE         scan an internal IP range, use cidr notation
  --delay DELAY         time to wait between lookups
  --subdomains SUBDOMAINS [SUBDOMAINS ...]
                        use these subdomains
  --subdomain-file SUBDOMAIN_FILE
                        use subdomains specified in this file (one per line)
  --dns-servers DNS_SERVERS [DNS_SERVERS ...]
                        use these dns servers for reverse lookups
  --dns-file DNS_FILE   use dns servers specified in this file for reverse lookups (one per line)
  --tcp                 use TCP instead of UDP


Updated on: 2026-Mar-13

 Edit this page

exploitdb
flashrom


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