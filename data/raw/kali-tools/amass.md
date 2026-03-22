amass | Kali Linux Tools
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


amass


version: 5.0.1 arch: any amass Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:identify


Packages & Binaries

amassamass

LIGHT

DARK
Packages and Binaries:
amass
In-depth DNS Enumeration and Network Mapping
This package contains a tool to help information security professionals
perform network mapping of attack surfaces and perform external asset
discovery using open source information gathering and active reconnaissance
techniques.
Information Gathering Techniques Used:
- DNS: Basic enumeration, Brute forcing (upon request), Reverse DNS
sweeping, Subdomain name alterations/permutations, Zone transfers (upon
request)
- Scraping: Ask, Baidu, Bing, DNSDumpster, DNSTable, Dogpile, Exalead,
Google, HackerOne, IPv4Info, Netcraft, PTRArchive, Riddler, SiteDossier,
ViewDNS, Yahoo
- Certificates: Active pulls (upon request), Censys, CertSpotter, Crtsh,
Entrust, GoogleCT
- APIs: AlienVault, BinaryEdge, BufferOver, CIRCL, CommonCrawl, DNSDB,
HackerTarget, Mnemonic, NetworksDB, PassiveTotal, RADb, Robtex,
SecurityTrails, ShadowServer, Shodan, Spyse (CertDB & FindSubdomains),
Sublist3rAPI, TeamCymru, ThreatCrowd, Twitter, Umbrella, URLScan,
VirusTotal
- Web Archives: ArchiveIt, ArchiveToday, Arquivo, LoCArchive,
OpenUKArchive, UKGovArchive, Wayback
This package contains the command amass.
Installed size: 30.26 MB
How to install: sudo apt install amass
Dependencies:libc6
libpostal1
sudo

amass
root@kali:~# amass -h
ERR   Could not find parser model file of known type
   at address_parser_load (address_parser.c:215) errno: No such file or directory
ERR   Error loading address parser module, dir=(null)
   at libpostal_setup_parser_datadir (libpostal.c:447) errno: No such file or directory

        .+++:.            :                             .+++.
      +W@@@@@@8        &+W@#               o8W8:      +W@@@@@@#.   oW@@@W#+
     &@#+   .o@##.    .@@@[email protected]@@o       :@@#&W8o    .@#:  .:oW+  .@#+++&#&
    +@&        &@&     #@8 +@W@&8@+     :@W.   +@8   +@:          .@8
    8@          @@     8@o  8@8  WW    .@W      W@+  .@W.          o@#:
    WW          &@o    &@:  o@+  o@+   #@.      8@o   +W@#+.        +W@8:
    #@          :@W    &@+  &@+   @8  :@o       o@o     oW@@W+        oW@8
    o@+          @@&   &@+  &@+   #@  &@.      .W@W       .+#@&         o@W.
     WW         +@W@8. &@+  :&    o@+ #@      :@W&@&         &@:  ..     :@o
     :@W:      o@# +Wo &@+        :W: +@W&o++o@W. &@&  8@#o+&@W.  #@:    o@+
      :W@@WWWW@@8       +              :&W@@@@&    &W  .o#@@W&.   :W@WWW@@&
        +o&&&&+.                                                    +oooo.

                                                                      v5.0.0
                                           OWASP Amass Project - @owaspamass
                         In-depth Attack Surface Mapping and Asset Discovery


Usage: amass [assoc|engine|enum|subs|track|viz] [options]

  -h	Show the program usage message
  -help
    	Show the program usage message
  -version
    	Print the Amass version number

Subcommands:

	assoc	Query the OAM along the walk defined by the triples
	engine	Run the Amass collection engine to populate the OAM database
	enum 	Interface with the engine that performs enumerations
	subs 	Analyze and present discovered subdomains and associated data
	track	Analyze OAM data to identify newly discovered assets
	viz  	Analyze OAM data to generate graph visualizations


Updated on: 2025-Dec-09

 Edit this page

altdns
android-sdk-meta


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