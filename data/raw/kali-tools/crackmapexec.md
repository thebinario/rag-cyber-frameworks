crackmapexec | Kali Linux Tools
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


crackmapexec


version: 5.4.0 arch: all crackmapexec Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
everything


Packages & Binaries

crackmapexeccmedb
crackmapexec
Learn more with OffSec
pen-200
LIGHT

DARK
Packages and Binaries:
crackmapexec
Swiss army knife for pentesting networks
This package is a swiss army knife for pentesting Windows/Active Directory
environments.
From enumerating logged on users and spidering SMB shares to executing psexec
style attacks, auto-injecting Mimikatz/Shellcode/DLL’s into memory using
Powershell, dumping the NTDS.dit and more.
The biggest improvements over the above tools are:
Pure Python script, no external tools required
Fully concurrent threading
Uses ONLY native WinAPI calls for discovering sessions, users, dumping
SAM hashes etc…
Opsec safe (no binaries are uploaded to dump clear-text credentials, inject
shellcode etc…)
Additionally, a database is used to store used/dumped credentals. It also
automatically correlates Admin credentials to hosts and vice-versa allowing you
to easily keep track of credential sets and gain additional situational
awareness in large environments.
Installed size: 2.29 MB
How to install: sudo apt install crackmapexec
Dependencies:python3
python3-aardwolf
python3-aioconsole
python3-bs4
python3-dsinternals
python3-impacket
python3-lsassy
python3-masky
python3-msgpack
python3-neo4j
python3-paramiko
python3-pylnk3
python3-pypsrp
python3-pywerview
python3-requests
python3-termcolor
python3-terminaltables3
python3-unicrypto
python3-xmltodict

cmedb
root@kali:~# cmedb -h
[-] Unable to find config file
crackmapexec
root@kali:~# crackmapexec -h
usage: crackmapexec [-h] [-t THREADS] [--timeout TIMEOUT] [--jitter INTERVAL]
                    [--darrell] [--verbose]
                    {mssql,winrm,rdp,ldap,smb,ssh,ftp} ...

      ______ .______           ___        ______  __  ___ .___  ___.      ___      .______    _______ ___   ___  _______   ______
     /      ||   _  \         /   \      /      ||  |/  / |   \/   |     /   \     |   _  \  |   ____|\  \ /  / |   ____| /      |
    |  ,----'|  |_)  |       /  ^  \    |  ,----'|  '  /  |  \  /  |    /  ^  \    |  |_)  | |  |__    \  V  /  |  |__   |  ,----'
    |  |     |      /       /  /_\  \   |  |     |    <   |  |\/|  |   /  /_\  \   |   ___/  |   __|    >   <   |   __|  |  |
    |  `----.|  |\  \----. /  _____  \  |  `----.|  .  \  |  |  |  |  /  _____  \  |  |      |  |____  /  .  \  |  |____ |  `----.
     \______|| _| `._____|/__/     \__\  \______||__|\__\ |__|  |__| /__/     \__\ | _|      |_______|/__/ \__\ |_______| \______|

                                                A swiss army knife for pentesting networks
                                    Forged by @byt3bl33d3r and @mpgn_x64 using the powah of dank memes

                                           Exclusive release for Porchetta Industries users
                                                       https://porchetta.industries/

                                                   Version : 5.4.0
                                                   Codename: Indestructible G0thm0g

options:
  -h, --help            show this help message and exit
  -t THREADS            set how many concurrent threads to use (default: 100)
  --timeout TIMEOUT     max timeout in seconds of each thread (default: None)
  --jitter INTERVAL     sets a random delay between each connection (default: None)
  --darrell             give Darrell a hand
  --verbose             enable verbose output

protocols:
  available protocols

  {mssql,winrm,rdp,ldap,smb,ssh,ftp}
    mssql               own stuff using MSSQL
    winrm               own stuff using WINRM
    rdp                 own stuff using RDP
    ldap                own stuff using LDAP
    smb                 own stuff using SMB
    ssh                 own stuff using SSH
    ftp                 own stuff using FTP


Learn more with OffSec
Want to learn more about crackmapexec? get access to in-depth training and hands-on labs:
PEN-200: 23.2.1. Attacking Active Directory Authentication: Password Attacks
PEN-200 course


Updated on: 2026-Mar-13

 Edit this page

crack
cri-tools


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