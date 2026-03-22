ettercap | Kali Linux Tools
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


ettercap


version: 0.8.4 arch: any ettercap Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:exploitation
sniffing-spoofing
social-engineering


Packages & Binaries

ettercap-common

ettercap-graphicalettercap
ettercap-pkexec
etterfilter
etterlog


ettercap-text-onlyettercap
etterfilter
etterlog

LIGHT

DARK
Packages and Binaries:
ettercap-common
Multipurpose sniffer/interceptor/logger for switched LAN
Ettercap supports active and passive dissection of many protocols
(even encrypted ones) and includes many feature for network and host
analysis.
Data injection in an established connection and filtering (substitute
or drop a packet) on the fly is also possible, keeping the connection
synchronized.
Many sniffing modes are implemented, for a powerful and complete
sniffing suite. It is possible to sniff in four modes: IP Based, MAC Based,
ARP Based (full-duplex) and PublicARP Based (half-duplex).
Ettercap also has the ability to detect a switched LAN, and to use OS
fingerprints (active or passive) to find the geometry of the LAN.
This package contains the Common support files, configuration files,
plugins, and documentation. You must also install either
ettercap-graphical or ettercap-text-only for the actual GUI-enabled
or text-only ettercap executable, respectively.
Installed size: 12.01 MB
How to install: sudo apt install ettercap-common
Dependencies:ethtool
geoip-database
libc6
libcurl4t64
libluajit-5.1-2 | libluajit-5.1-2
libmaxminddb0
libnet9
libpcap0.8t64
libpcre2-8-0
libssl3t64
zlib1g

ettercap-graphical
Ettercap GUI-enabled executable
Ettercap supports active and passive dissection of many protocols
(even encrypted ones) and includes many feature for network and host
analysis.
Data injection in an established connection and filtering (substitute
or drop a packet) on the fly is also possible, keeping the connection
synchronized.
Many sniffing modes are implemented, for a powerful and complete
sniffing suite. It is possible to sniff in four modes: IP Based, MAC Based,
ARP Based (full-duplex) and PublicARP Based (half-duplex).
Ettercap also has the ability to detect a switched LAN, and to use OS
fingerprints (active or passive) to find the geometry of the LAN.
This package contains the ettercap GUI-enabled executable.
Installed size: 595 KB
How to install: sudo apt install ettercap-graphical
Dependencies:ettercap-common
libc6
libgdk-pixbuf-2.0-0
libglib2.0-0t64
libgtk-3-0t64
libncurses6
libpcre2-8-0
libtinfo6
pkexec
zlib1g

ettercap
Multipurpose sniffer/content filter for man in the middle attacks
root@kali:~# ettercap -h

ettercap 0.8.4 copyright 2001-2026 Ettercap Development Team


Usage: ettercap [OPTIONS] [TARGET1] [TARGET2]

TARGET is in the format MAC/IP/IPv6/PORTs (see the man for further detail)

Sniffing and Attack options:
  -M, --mitm <METHOD:ARGS>    perform a mitm attack
  -o, --only-mitm             don't sniff, only perform the mitm attack
  -b, --broadcast             sniff packets destined to broadcast
  -B, --bridge <IFACE>        use bridged sniff (needs 2 ifaces)
  -p, --nopromisc             do not put the iface in promisc mode
  -S, --nosslmitm             do not forge SSL certificates
  -u, --unoffensive           do not forward packets
  -r, --read <file>           read data from pcapfile <file>
  -f, --pcapfilter <string>   set the pcap filter <string>
  -R, --reversed              use reversed TARGET matching
  -t, --proto <proto>         sniff only this proto (default is all)
      --certificate <file>    certificate file to use for SSL MiTM
      --private-key <file>    private key file to use for SSL MiTM

User Interface Type:
  -T, --text                  use text only GUI
       -q, --quiet                 do not display packet contents
       -s, --script <CMD>          issue these commands to the GUI
  -C, --curses                use curses GUI
  -D, --daemon                daemonize ettercap (no GUI)
  -G, --gtk                   use GTK+ GUI

Logging options:
  -w, --write <file>          write sniffed data to pcapfile <file>
  -L, --log <logfile>         log all the traffic to this <logfile>
  -l, --log-info <logfile>    log only passive infos to this <logfile>
  -m, --log-msg <logfile>     log all the messages to this <logfile>
  -c, --compress              use gzip compression on log files

Visualization options:
  -d, --dns                   resolves ip addresses into hostnames
  -V, --visual <format>       set the visualization format
  -e, --regex <regex>         visualize only packets matching this regex
  -E, --ext-headers           print extended header for every pck
  -Q, --superquiet            do not display user and password

LUA options:
      --lua-script <script1>,[<script2>,...]     comma-separted list of LUA scripts
      --lua-args n1=v1,[n2=v2,...]               comma-separated arguments to LUA script(s)

General options:
  -i, --iface <iface>         use this network interface
  -I, --liface                show all the network interfaces
  -Y, --secondary <ifaces>    list of secondary network interfaces
  -n, --netmask <netmask>     force this <netmask> on iface
  -A, --address <address>     force this local <address> on iface
  -P, --plugin <plugin>       launch this <plugin> - multiple occurance allowed
      --plugin-list <plugin1>,[<plugin2>,...]       comma-separated list of plugins
  -F, --filter <file>         load the filter <file> (content filter)
  -z, --silent                do not perform the initial ARP scan
  -6, --ip6scan               send ICMPv6 probes to discover IPv6 nodes on the link
  -j, --load-hosts <file>     load the hosts list from <file>
  -k, --save-hosts <file>     save the hosts list to <file>
  -W, --wifi-key <wkey>       use this key to decrypt wifi packets (wep or wpa)
  -a, --config <config>       use the alternative config file <config>

Standard options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


ettercap-pkexec
Graphical pkexec-based launcher for ettercap
root@kali:~# man ettercap-pkexec
ETTERCAP(8)                 System Manager's Manual                 ETTERCAP(8)

NAME
       ettercap-pkexec - graphical pkexec-based launcher for ettercap

       This  launcher  depends  on policykit-1 and the menu packages, and basi-
       cally wraps the ettercap binary command
       with a pkexec action script usually defined  on  /usr/share/polkit-1/ac-
       tions/org.pkexec.ettercap.policy,
       allowing  users  to  directly  call  ettercap  from  the desktop or menu
       launcher with root privileges.
       The commands available are exactly the same as the ettercap man page.

       Please refer to man ettercap for the list of available parameters.
       (don't forget to change "ettercap" to "ettercap-pkexec" as  caller  pro-
       gram).

       example:

       ettercap-pkexec -G will start ettercap with root privileges and the GTK2
       interface.

AUTHOR
       This  code was originally taken from arch distro, and refactored to work
       with cmake system by
       Gianfranco Costamagna (LocutusOfBorg) <[email protected]>

ORIGINAL AUTHORS
       Alberto Ornaghi (ALoR) <[email protected]>
       Marco Valleri (NaGA) <[email protected]>

PROJECT STEWARDS
       Emilio Escobar (exfil)  <[email protected]>
       Eric Milam (Brav0Hax)  <[email protected]>

OFFICIAL DEVELOPERS
       Mike Ryan (justfalter)  <[email protected]>
       Gianfranco Costamagna (LocutusOfBorg)  <[email protected]>
       Antonio Collarino (sniper)  <[email protected]>
       Ryan Linn   <[email protected]>
       Jacob Baines   <[email protected]>

CONTRIBUTORS
       Dhiru Kholia (kholia)  <[email protected]>
       Alexander Koeppe (koeppea)  <[email protected]>
       Martin Bos (PureHate)  <[email protected]>
       Enrique Sanchez
       Gisle Vanem  <[email protected]>
       Johannes Bauer  <[email protected]>
       Daten (Bryan Schneiders)  <[email protected]>

SEE ALSO
       etter.conf(5) ettercap_curses(8) ettercap_plugins(8) etterlog(8)  etter-
       filter(8)

AVAILABILITY
       https://github.com/Ettercap/ettercap/downloads

GIT
       git clone git://github.com/Ettercap/ettercap.git
       or
       git clone https://github.com/Ettercap/ettercap.git

BUGS
       Our software never has bugs.
       It just develops random features.   ;)

       KNOWN-BUGS

       -  ettercap  doesn't handle fragmented packets... only the first segment
       will be displayed by the sniffer. However all  the  fragments  are  cor-
       rectly forwarded.

       +  please send bug-report, patches or suggestions to <ettercap-betatest-
       [email protected]> or  visit  https://github.com/Ettercap/etter-
       cap/issues.

       + to report a bug, follow the instructions in the README.BUGS file

PHILOLOGICAL HISTORY
       "Even  if  blessed  with  a  feeble  intelligence,  they  are  cruel and
       smart..."  this is the description of Ettercap, a monster of the RPG Ad-
       vanced Dungeons & Dragon.

       The name "ettercap" was chosen because it has an assonance with  "ether-
       cap"  which  means  "ethernet capture" (what ettercap actually does) and
       also because such monsters have a powerful poison... and you  know,  arp
       poisoning... ;)

The Lord Of The (Token)Ring
       (the fellowship of the packet)

       "One Ring to link them all, One Ring to ping them,
        one Ring to bring them all and in the darkness sniff them."

Last words
       "Programming  today  is  a  race  between software engineers striving to
       build bigger and better idiot-proof programs, and the Universe trying to
       produce bigger and better idiots. So far, the Universe  is  winning."  -
       Rich Cook

ettercap 0.8.4                                                      ETTERCAP(8)
etterfilter
Filter compiler for ettercap content filtering engine
root@kali:~# etterfilter -h

Usage: etterfilter [OPTIONS] filterfile

General Options:
  -o, --output <file>         output file (default is filter.ef)
  -t, --test <file>           test the file (debug mode)
  -d, --debug                 print some debug info while compiling
  -w, --suppress-warnings     ignore warnings during compilation

Standard Options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


etterfilter 0.8.4 copyright 2001-2026 Ettercap Development Team


etterlog
Log analyzer for ettercap log files
root@kali:~# etterlog -h

Usage: etterlog [OPTIONS] logfile

General Options:
  -a, --analyze               analyze a log file and return useful infos
  -c, --connections           display the table of connections
  -f, --filter <TARGET>       print packets only from this target
  -t, --proto <proto>         display only this proto (default is all)
  -F, --filcon <CONN>         print packets only from this connection
  -s, --only-source           print packets only from the source
  -d, --only-dest             print packets only from the destination
  -r, --reverse               reverse the target/connection matching
  -n, --no-headers            skip header information between packets
  -m, --show-mac              show mac addresses in the headers
  -k, --color                 colorize the output
  -l, --only-local            show only local hosts parsing info files
  -L, --only-remote           show only remote hosts parsing info files

Search Options:
  -e, --regex <regex>         display only packets that match the regex
  -u, --user <user>           search for info about the user <user>
  -p, --passwords             print only accounts information
  -i, --show-client           show client address in the password profiles
  -I, --client <ip>           search for pass from a specific client

Editing Options:
  -C, --concat                concatenate more files into one single file
  -o, --outfile <file>        the file used as output for concatenation
  -D, --decode                used to extract files from connections

Visualization Method:
  -B, --binary                print packets as they are
  -X, --hex                   print packets in hex mode
  -A, --ascii                 print packets in ascii mode (default)
  -T, --text                  print packets in text mode
  -E, --ebcdic                print packets in ebcdic mode
  -H, --html                  print packets in html mode
  -U, --utf8 <encoding>       print packets in uft-8 using the <encoding>
  -Z, --zero                  do not print packets, only headers
  -x, --xml                   print host infos in xml format

Standard Options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


etterlog 0.8.4 copyright 2001-2026 Ettercap Development Team


ettercap-text-only
Ettercap console-mode executable
Ettercap supports active and passive dissection of many protocols
(even encrypted ones) and includes many feature for network and host
analysis.
Data injection in an established connection and filtering (substitute
or drop a packet) on the fly is also possible, keeping the connection
synchronized.
Many sniffing modes are implemented, for a powerful and complete
sniffing suite. It is possible to sniff in four modes: IP Based, MAC Based,
ARP Based (full-duplex) and PublicARP Based (half-duplex).
Ettercap also has the ability to detect a switched LAN, and to use OS
fingerprints (active or passive) to find the geometry of the LAN.
This package contains the ettercap text-mode-only executable.
Installed size: 305 KB
How to install: sudo apt install ettercap-text-only
Dependencies:ettercap-common
libc6
libncurses6
libpcre2-8-0
libtinfo6
zlib1g

ettercap
Multipurpose sniffer/content filter for man in the middle attacks
root@kali:~# ettercap -h

ettercap 0.8.4 copyright 2001-2026 Ettercap Development Team


Usage: ettercap [OPTIONS] [TARGET1] [TARGET2]

TARGET is in the format MAC/IP/IPv6/PORTs (see the man for further detail)

Sniffing and Attack options:
  -M, --mitm <METHOD:ARGS>    perform a mitm attack
  -o, --only-mitm             don't sniff, only perform the mitm attack
  -b, --broadcast             sniff packets destined to broadcast
  -B, --bridge <IFACE>        use bridged sniff (needs 2 ifaces)
  -p, --nopromisc             do not put the iface in promisc mode
  -S, --nosslmitm             do not forge SSL certificates
  -u, --unoffensive           do not forward packets
  -r, --read <file>           read data from pcapfile <file>
  -f, --pcapfilter <string>   set the pcap filter <string>
  -R, --reversed              use reversed TARGET matching
  -t, --proto <proto>         sniff only this proto (default is all)
      --certificate <file>    certificate file to use for SSL MiTM
      --private-key <file>    private key file to use for SSL MiTM

User Interface Type:
  -T, --text                  use text only GUI
       -q, --quiet                 do not display packet contents
       -s, --script <CMD>          issue these commands to the GUI
  -C, --curses                use curses GUI
  -D, --daemon                daemonize ettercap (no GUI)
  -G, --gtk                   use GTK+ GUI

Logging options:
  -w, --write <file>          write sniffed data to pcapfile <file>
  -L, --log <logfile>         log all the traffic to this <logfile>
  -l, --log-info <logfile>    log only passive infos to this <logfile>
  -m, --log-msg <logfile>     log all the messages to this <logfile>
  -c, --compress              use gzip compression on log files

Visualization options:
  -d, --dns                   resolves ip addresses into hostnames
  -V, --visual <format>       set the visualization format
  -e, --regex <regex>         visualize only packets matching this regex
  -E, --ext-headers           print extended header for every pck
  -Q, --superquiet            do not display user and password

LUA options:
      --lua-script <script1>,[<script2>,...]     comma-separted list of LUA scripts
      --lua-args n1=v1,[n2=v2,...]               comma-separated arguments to LUA script(s)

General options:
  -i, --iface <iface>         use this network interface
  -I, --liface                show all the network interfaces
  -Y, --secondary <ifaces>    list of secondary network interfaces
  -n, --netmask <netmask>     force this <netmask> on iface
  -A, --address <address>     force this local <address> on iface
  -P, --plugin <plugin>       launch this <plugin> - multiple occurance allowed
      --plugin-list <plugin1>,[<plugin2>,...]       comma-separated list of plugins
  -F, --filter <file>         load the filter <file> (content filter)
  -z, --silent                do not perform the initial ARP scan
  -6, --ip6scan               send ICMPv6 probes to discover IPv6 nodes on the link
  -j, --load-hosts <file>     load the hosts list from <file>
  -k, --save-hosts <file>     save the hosts list to <file>
  -W, --wifi-key <wkey>       use this key to decrypt wifi packets (wep or wpa)
  -a, --config <config>       use the alternative config file <config>

Standard options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


etterfilter
Filter compiler for ettercap content filtering engine
root@kali:~# etterfilter -h

Usage: etterfilter [OPTIONS] filterfile

General Options:
  -o, --output <file>         output file (default is filter.ef)
  -t, --test <file>           test the file (debug mode)
  -d, --debug                 print some debug info while compiling
  -w, --suppress-warnings     ignore warnings during compilation

Standard Options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


etterfilter 0.8.4 copyright 2001-2026 Ettercap Development Team


etterlog
Log analyzer for ettercap log files
root@kali:~# etterlog -h

Usage: etterlog [OPTIONS] logfile

General Options:
  -a, --analyze               analyze a log file and return useful infos
  -c, --connections           display the table of connections
  -f, --filter <TARGET>       print packets only from this target
  -t, --proto <proto>         display only this proto (default is all)
  -F, --filcon <CONN>         print packets only from this connection
  -s, --only-source           print packets only from the source
  -d, --only-dest             print packets only from the destination
  -r, --reverse               reverse the target/connection matching
  -n, --no-headers            skip header information between packets
  -m, --show-mac              show mac addresses in the headers
  -k, --color                 colorize the output
  -l, --only-local            show only local hosts parsing info files
  -L, --only-remote           show only remote hosts parsing info files

Search Options:
  -e, --regex <regex>         display only packets that match the regex
  -u, --user <user>           search for info about the user <user>
  -p, --passwords             print only accounts information
  -i, --show-client           show client address in the password profiles
  -I, --client <ip>           search for pass from a specific client

Editing Options:
  -C, --concat                concatenate more files into one single file
  -o, --outfile <file>        the file used as output for concatenation
  -D, --decode                used to extract files from connections

Visualization Method:
  -B, --binary                print packets as they are
  -X, --hex                   print packets in hex mode
  -A, --ascii                 print packets in ascii mode (default)
  -T, --text                  print packets in text mode
  -E, --ebcdic                print packets in ebcdic mode
  -H, --html                  print packets in html mode
  -U, --utf8 <encoding>       print packets in uft-8 using the <encoding>
  -Z, --zero                  do not print packets, only headers
  -x, --xml                   print host infos in xml format

Standard Options:
  -v, --version               prints the version and exit
  -h, --help                  this help screen


etterlog 0.8.4 copyright 2001-2026 Ettercap Development Team


Updated on: 2026-Mar-02

 Edit this page

ethtool
evil-winrm


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