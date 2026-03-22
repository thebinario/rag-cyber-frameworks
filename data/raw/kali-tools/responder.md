responder | Kali Linux Tools
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


responder


version: 3.2.2.0 arch: all responder Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large
top10

Tools:sniffing-spoofing
top10


Tool Documentation
Packages & Binaries

responderresponder
responder-BrowserListener
responder-DHCP_Auto
responder-FindSQLSrv
responder-Icmp-Redirect
responder-MultiRelay
responder-RunFinger
Learn more with OffSec
pen-200
pen-300
LIGHT

DARK
Tool Documentation:
responder Usage Example
Specify the IP address to redirect to (-i 192.168.1.202), enabling the WPAD rogue proxy (-w On), answers for netbios wredir (-r On), and fingerprinting (-f On):
root@kali:~# responder -i 192.168.1.202 -w On -r On -f On
NBT Name Service/LLMNR Responder 2.0.
Please send bugs/comments to: [email protected]
To kill this script hit CRTL-C

[+]NBT-NS &amp; LLMNR responder started
[+]Loading Responder.conf File..
Global Parameters set:
Responder is bound to this interface:ALL
Challenge set is:1122334455667788
WPAD Proxy Server is:ON
WPAD script loaded:function FindProxyForURL(url, host){if ((host == "localhost") || shExpMatch(host, "localhost.*") ||(host == "127.0.0.1") || isPlainHostName(host)) return "DIRECT"; if (dnsDomainIs(host, "RespProxySrv")||shExpMatch(host, "(*.RespProxySrv|RespProxySrv)")) return "DIRECT"; return 'PROXY ISAProxySrv:3141; DIRECT';}
HTTP Server is:ON
HTTPS Server is:ON
SMB Server is:ON
SMB LM support is set to:OFF
SQL Server is:ON
FTP Server is:ON
IMAP Server is:ON
POP3 Server is:ON
SMTP Server is:ON
DNS Server is:ON
LDAP Server is:ON
FingerPrint Module is:ON
Serving Executable via HTTP&amp;WPAD is:OFF
Always Serving a Specific File via HTTP&amp;WPAD is:OFF
Packages and Binaries:
responder
LLMNR/NBT-NS/mDNS Poisoner
This package contains Responder/MultiRelay, an LLMNR, NBT-NS and MDNS
poisoner. It will answer to specific NBT-NS (NetBIOS Name Service) queries
based on their name suffix (see: http://support.microsoft.com/kb/163409). By
default, the tool will only answer to File Server Service request, which is for
SMB.
The concept behind this is to target your answers, and be stealthier on the
network. This also helps to ensure that you don’t break legitimate NBT-NS
behavior. You can set the -r option via command line if you want to answer
to the Workstation Service request name suffix.
Installed size: 4.25 MB
How to install: sudo apt install responder
Dependencies:net-tools
python3
python3-aioquic
python3-netifaces
python3-pkg-resources
python3-pycryptodome
python3-six

responder
root@kali:~# responder -h
                                         __
  .----.-----.-----.-----.-----.-----.--|  |.-----.----.
  |   _|  -__|__ --|  _  |  _  |     |  _  ||  -__|   _|
  |__| |_____|_____|   __|_____|__|__|_____||_____|__|
                   |__|

Usage: python3 Responder.py -I eth0 -v

══════════════════════════════════════════════════════════════════════════════
  Responder - LLMNR/NBT-NS/mDNS Poisoner and Rogue Authentication Servers
══════════════════════════════════════════════════════════════════════════════
Captures credentials by responding to broadcast/multicast name resolution,
DHCP, DHCPv6 requests
══════════════════════════════════════════════════════════════════════════════

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit

  Required Options:
These options must be specified

    -I eth0, --interface=eth0
                        Network interface to use. Use 'ALL' for all
                        interfaces.

  Poisoning Options:
Control how Responder poisons name resolution requests

    -A, --analyze       Analyze mode. See requests without poisoning.
                        (passive)
    -e IP, --externalip=IP
                        Poison with a different IPv4 address than Responder's.
    -6 IPv6, --externalip6=IPv6
                        Poison with a different IPv6 address than Responder's.
    --rdnss             Poison via Router Advertisements with RDNSS. Sets
                        attacker as IPv6 DNS.
    --dnssl=DOMAIN      Poison via Router Advertisements with DNSSL. Injects
                        DNS search suffix.
    -t HEX, --ttl=HEX   Set TTL for poisoned answers. Hex value (30s = 1e) or
                        'random'.
    -N NAME, --AnswerName=NAME
                        Canonical name in LLMNR answers. (for Kerberos relay
                        over HTTP)

  DHCP Options:
DHCP and DHCPv6 poisoning attacks

    -d, --DHCP          Enable DHCPv4 poisoning. Injects WPAD in DHCP
                        responses.
    -D, --DHCP-DNS      Inject DNS server (not WPAD) in DHCPv4 responses.
    --dhcpv6            Enable DHCPv6 poisoning. WARNING: May disrupt network.

  WPAD / Proxy Options:
Web Proxy Auto-Discovery attacks

    -w, --wpad          Start WPAD rogue proxy server.
    -F, --ForceWpadAuth
                        Force NTLM/Basic auth on wpad.dat retrieval. (may show
                        prompt)
    -P, --ProxyAuth     Force proxy authentication. Highly effective. (can't
                        use with -w)
    -u HOST:PORT, --upstream-proxy=HOST:PORT
                        Upstream proxy for rogue WPAD proxy outgoing requests.

  Authentication Options:
Control authentication methods and downgrades

    -b, --basic         Return HTTP Basic auth instead of NTLM. (cleartext
                        passwords)
    --lm                Force LM hashing downgrade. (for Windows XP/2003)
    --disable-ess       Disable Extended Session Security. (NTLMv1 downgrade)
    -E, --ErrorCode     Return STATUS_LOGON_FAILURE. (enables WebDAV auth
                        capture)

  Output Options:
Control verbosity and logging

    -v, --verbose       Increase verbosity. (recommended)
    -Q, --quiet         Quiet mode. Minimal output from poisoners.

  Platform Options:
OS-specific settings

    -i IP, --ip=IP      Local IP to use. (OSX only)

══════════════════════════════════════════════════════════════════════════════
  Examples:
══════════════════════════════════════════════════════════════════════════════
  Basic poisoning:            python3 Responder.py -I eth0 -v

  ##Watch what's going on:
  Analyze mode (passive):     python3 Responder.py -I eth0 -Av

  ##Working on old networks:
  WPAD with forced auth:      python3 Responder.py -I eth0 -wFv

  ##Great module:
  Proxy auth:                 python3 Responder.py -I eth0 -Pv

  ##DHCPv6 + Proxy authentication:
  DHCPv6 attack:              python3 Responder.py -I eth0 --dhcpv6 -vP

  ##DHCP -> WPAD injection -> Proxy authentication:
  DHCP + WPAD injection:      python3 Responder.py -I eth0 -Pvd

  ##Poison requests to an arbitrary IP:
  Poison with external IP:    python3 Responder.py -I eth0 -e 10.0.0.100

  ##Poison requests to an arbitrary IPv6 IP:
  Poison with external IPv6:  python3 Responder.py -I eth0 -6 2800:ac:4000:8f9e:c5eb:2193:71:1d12
══════════════════════════════════════════════════════════════════════════════
  For more info: https://github.com/lgandx/Responder/blob/master/README.md
══════════════════════════════════════════════════════════════════════════════
responder-BrowserListener
responder-DHCP_Auto
responder-FindSQLSrv
root@kali:~# responder-FindSQLSrv --help
MSSQL Server Finder 0.3
responder-Icmp-Redirect
root@kali:~# responder-Icmp-Redirect -h
Usage: responder-Icmp-Redirect -I eth0 -i 10.20.30.40 -g 10.20.30.254 -t 10.20.30.48 -r 10.20.40.1

Options:
  -h, --help            show this help message and exit
  -i 10.20.30.40, --ip=10.20.30.40
                        The ip address to redirect the traffic to. (usually
                        yours)
  -g 10.20.30.254, --gateway=10.20.30.254
                        The ip address of the original gateway (issue the
                        command 'route -n' to know where is the gateway
  -t 10.20.30.48, --target=10.20.30.48
                        The ip address of the target
  -r 10.20.40.1, --route=10.20.40.1
                        The ip address of the destination target, example: DNS
                        server. Must be on another subnet.
  -s 10.20.40.1, --secondaryroute=10.20.40.1
                        The ip address of the destination target, example:
                        Secondary DNS server. Must be on another subnet.
  -I eth0, --interface=eth0
                        Interface name to use, example: eth0
  -a 10.20.30.40, --alternate=10.20.30.40
                        The alternate gateway, set this option if you wish to
                        redirect the victim traffic to another host than yours
responder-MultiRelay
root@kali:~# responder-MultiRelay -h
[!]MultiRelay/bin/ folder is empty. You need to run these commands:

apt-get install gcc-mingw-w64-x86-64
x86_64-w64-mingw32-gcc ./MultiRelay/bin/Runas.c -o ./MultiRelay/bin/Runas.exe -municode -lwtsapi32 -luserenv
x86_64-w64-mingw32-gcc ./MultiRelay/bin/Syssvc.c -o ./MultiRelay/bin/Syssvc.exe -municode

Additionally, you can add your custom mimikatz executables (mimikatz.exe and mimikatz_x86.exe)
in the MultiRelay/bin/ folder for the mimi32/mimi command.
responder-RunFinger
root@kali:~# responder-RunFinger -h
Usage: responder-RunFinger -i 10.10.10.224
or:
responder-RunFinger -i 10.10.10.0/24

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i 10.10.10.224, --ip=10.10.10.224
                        Target IP address or class C
  -f ips.txt, --filename=ips.txt
                        Target file
  -t 0.9, --timeout=0.9
                        Timeout for all connections. Use this option to fine
                        tune Runfinger.


Learn more with OffSec
Want to learn more about responder? get access to in-depth training and hands-on labs:
PEN-200: 16.3.3. Password Attacks: Cracking Net-NTLMv2
PEN-300: 20.1.3. Microsoft SQL Attacks: UNC Path Injection
PEN-200 course

PEN-300 course


Updated on: 2026-Mar-13

 Edit this page

readpe
rev-proxy-grapher


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