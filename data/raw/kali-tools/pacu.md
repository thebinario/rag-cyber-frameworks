pacu | Kali Linux Tools
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


pacu


version: 1.6.0 arch: all pacu Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
everything


Packages & Binaries

pacupacu
Learn more with OffSec
pen-200
LIGHT

DARK
Packages and Binaries:
pacu
Open Source AWS Exploitation Framework
This package contains an open-source AWS exploitation framework, designed for
offensive security testing against cloud environments. Created and maintained
by Rhino Security Labs, Pacu allows penetration testers to exploit
configuration flaws within an AWS account, using modules to easily expand its
functionality. Current modules enable a range of attacks, including user
privilege escalation, backdooring of IAM users, attacking vulnerable Lambda
functions, and much more.
Installed size: 13.33 MB
How to install: sudo apt install pacu
Dependencies:awscli
python3
python3-boto3
python3-botocore
python3-colorama
python3-dsnap
python3-freezegun
python3-jq
python3-policyuniverse
python3-pycognito
python3-qrcode
python3-requests
python3-sqlalchemy
python3-sqlalchemy-utils
python3-toml
python3-typing-extensions
python3-urllib3
python3-yaml

pacu
root@kali:~# pacu -h
usage: pacu [-h] [--session ] [--activate-session] [--new-session ]
            [--set-keys ] [--import-keys ] [--module-name ] [--data ]
            [--module-args ] [--list-modules] [--pacu-help] [--module-info]
            [--exec] [--set-regions  [ ...]] [--whoami] [--version] [-q]

options:
  -h, --help            show this help message and exit
  --session             <session name>
  --activate-session    activate session, use session arg to set session name
  --new-session         <session name>
  --set-keys            alias, access id, secret key, token
  --import-keys         AWS profile name to import keys from
  --module-name         <module name>
  --data                <service name/all>
  --module-args         <--module-args='--regions us-east-1,us-east-1'>
  --list-modules        List arguments
  --pacu-help           List the Pacu help window
  --module-info         Get information on a specific module, use --module-
                        name
  --exec                exec module
  --set-regions  [ ...]
                        <region1 region2 ...> or <all> for all
  --whoami              Display information on current IAM user
  --version             Display Pacu version
  -q, --quiet           Do not print the banner on startup


Learn more with OffSec
Want to learn more about pacu? get access to in-depth training and hands-on labs:
PEN-200: 25. Enumerating AWS Cloud Infrastructure
PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

pack2
padbuster


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