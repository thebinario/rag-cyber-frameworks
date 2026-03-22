dnsrecon | Kali Linux Tools
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


dnsrecon


version: 1.3.1 arch: all dnsrecon Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:information-gathering


Tool Documentation
Packages & Binaries

dnsrecondnsrecon
Learn more with OffSec
pen-200
LIGHT

DARK
Tool Documentation:
Video
dnsrecon Usage Example
Scan a domain (-d example.com), use a dictionary to brute force hostnames (-D /usr/share/wordlists/dnsmap.txt), do a standard scan (-t std), and save the output to a file (–xml dnsrecon.xml):
root@kali:~# dnsrecon -d example.com -D /usr/share/wordlists/dnsmap.txt -t std --xml dnsrecon.xml
[*] Performing General Enumeration of Domain:example.com
[*] DNSSEC is configured for example.com
[*] DNSKEYs:
Packages and Binaries:
dnsrecon
Powerful DNS enumeration script
DNSRecon is a Python script that provides the ability to perform:
Check all NS Records for Zone Transfers.
Enumerate General DNS Records for a given Domain
(MX, SOA, NS, A, AAAA, SPF and TXT).
Perform common SRV Record Enumeration.
Top Level Domain (TLD) Expansion.
Check for Wildcard Resolution.
Brute Force subdomain and host A and AAAA records
given a domain and a wordlist.
Perform a PTR Record lookup for a given IP Range or CIDR.
Check a DNS Server Cached records for A, AAAA and CNAME
Records provided a list of host records in a text file to check.
Enumerate Hosts and Subdomains using Google
Installed size: 1.45 MB
How to install: sudo apt install dnsrecon
Dependencies:python3
python3-dnspython
python3-loguru
python3-lxml
python3-netaddr
python3-requests

dnsrecon
DNS Enumeration and Scanning Tool
root@kali:~# dnsrecon -h
usage: dnsrecon [-h] [-d DOMAIN] [-iL INPUT_LIST] [-n NS_SERVER] [-r RANGE]
                [-D DICTIONARY] [-f] [-a] [-s] [-b] [-y] [-k] [-w] [-z]
                [--threads THREADS] [--lifetime LIFETIME]
                [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--tcp]
                [--db DB] [-x XML] [-c CSV] [-j JSON] [--iw]
                [--disable_check_nxdomain] [--disable_check_recursion]
                [--disable_check_bindversion] [-V] [-v] [-t TYPE]

options:
  -h, --help            show this help message and exit
  -d, --domain DOMAIN   Target domain.
  -iL, --input-list INPUT_LIST
                        File containing a list of domains to perform DNS enumeration on, one per line.
  -n, --name_server NS_SERVER
                        Domain server to use. If none is given, the SOA of the target will be used. Multiple servers can be specified using a comma separated list.
  -r, --range RANGE     IP range for reverse lookup brute force in formats (first-last) or in (range/bitmask).
  -D, --dictionary DICTIONARY
                        Dictionary file of subdomain and hostnames to use for brute force.
  -f                    Filter out of brute force domain lookup, records that resolve to the wildcard defined IP address when saving records.
  -a                    Perform AXFR with standard enumeration.
  -s                    Perform a reverse lookup of IPv4 ranges in the SPF record with standard enumeration.
  -b                    Perform Bing enumeration with standard enumeration.
  -y                    Perform Yandex enumeration with standard enumeration.
  -k                    Perform crt.sh enumeration with standard enumeration.
  -w                    Perform deep whois record analysis and reverse lookup of IP ranges found through Whois when doing a standard enumeration.
  -z                    Performs a DNSSEC zone walk with standard enumeration.
  --threads THREADS     Number of threads to use in reverse lookups, forward lookups, brute force and SRV record enumeration.
  --lifetime LIFETIME   Time to wait for a server to respond to a query. default is 3.0
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Log level to use. default is INFO
  --tcp                 Use TCP protocol to make queries.
  --db DB               SQLite 3 file to save found records.
  -x, --xml XML         XML file to save found records.
  -c, --csv CSV         Save output to a comma separated value file.
  -j, --json JSON       save output to a JSON file.
  --iw                  Continue brute forcing a domain even if a wildcard record is discovered.
  --disable_check_nxdomain
                        Disables check for NXDOMAIN hijacking on name servers.
  --disable_check_recursion
                        Disables check for recursion on name servers
  --disable_check_bindversion
                        Disables check for BIND version on name servers
  -V, --version         DNSrecon version
  -v, --verbose         Enable verbosity
  -t, --type TYPE       Type of enumeration to perform.
                        Possible types:
                            std:      SOA, NS, A, AAAA, MX and SRV.
                            rvl:      Reverse lookup of a given CIDR or IP range.
                            brt:      Brute force domains and hosts using a given dictionary.
                            srv:      SRV records.
                            axfr:     Test all NS servers for a zone transfer.
                            bing:     Perform Bing search for subdomains and hosts.
                            yand:     Perform Yandex search for subdomains and hosts.
                            crt:      Perform crt.sh search for subdomains and hosts.
                            snoop:    Perform cache snooping against all NS servers for a given domain, testing
                                      all with file containing the domains, file given with -D option.

                            tld:      Remove the TLD of given domain and test against all TLDs registered in IANA.
                            zonewalk: Perform a DNSSEC zone walk using NSEC records.


Learn more with OffSec
Want to learn more about dnsrecon? get access to in-depth training and hands-on labs:
PEN-200: 6.4.1. Information Gathering: DNS Enumeration
PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

dnsmap
dnstracer


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