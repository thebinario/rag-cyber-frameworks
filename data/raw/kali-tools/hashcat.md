hashcat | Kali Linux Tools
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


hashcat


version: 7.1.2 arch: kfreebsd-any amd64 arm64 armhf i386 all hashcat Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
default
everything
large

Tools:802-11
passwords
wireless


Tool Documentation
Packages & Binaries

hashcathashcat


hashcat-data
Learn more with OffSec
pen-200
LIGHT

DARK
Tool Documentation:
hashcat Usage Examples
Run a benchmark test on all supported hash types to determine cracking speed:
root@kali:~# hashcat -b
hashcat (v5.0.0) starting in benchmark mode...

Benchmarking uses hand-optimized kernel code by default.
You can use it in your cracking session by setting the -O option.
Note: Using optimized kernel code limits the maximum supported password length.
To disable the optimized kernel code in benchmark mode, use the -w option.

* Device #1: Not a native Intel OpenCL runtime. Expect massive speed loss.
             You can use --force to override, but do not report related errors.
OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz, skipped.

OpenCL Platform #2: Intel(R) Corporation
========================================
* Device #2: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz, 986/3946 MB allocatable, 2MCU

Benchmark relevant options:
===========================
* --optimized-kernel-enable

Hashmode: 0 - MD5

Speed.#2.........:   134.9 MH/s (15.41ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8

Hashmode: 100 - SHA1

Speed.#2.........: 98899.4 kH/s (21.04ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8

Hashmode: 1400 - SHA2-256

Speed.#2.........: 42768.3 kH/s (48.86ms) @ Accel:1024 Loops:1024 Thr:1 Vec:8
[...]
Use md5crypt mode (-m 500) to cracking the sample hash (example500.hash) with the provided wordlist (/usr/share/wordlists/sqlmap.txt):
root@kali:~# hashcat -m 500 example500.hash /usr/share/wordlists/sqlmap.txt
hashcat (v5.0.0) starting...

* Device #1: Not a native Intel OpenCL runtime. Expect massive speed loss.
             You can use --force to override, but do not report related errors.
OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz, skipped.

OpenCL Platform #2: Intel(R) Corporation
========================================
* Device #2: Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz, 986/3946 MB allocatable, 2MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers:
* Zero-Byte
* Single-Hash
* Single-Salt

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

ATTENTION! Pure (unoptimized) OpenCL kernels selected.
This enables cracking passwords and salts > length 32 but for the price of drastically reduced performance.
If you want to switch to optimized OpenCL kernels, append -O to your commandline.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

* Device #2: build_opts '-cl-std=CL1.2 -I OpenCL -I /usr/share/hashcat/OpenCL -D VENDOR_ID=8 -D CUDA_ARCH=0 -D AMD_ROCM=0 -D VECT_SIZE=8 -D DEVICE_TYPE=2 -D DGST_R0=0 -D DGST_R1=1 -D DGST_R2=2 -D DGST_R3=3 -D DGST_ELEM=4 -D KERN_TYPE=500 -D _unroll'
Dictionary cache hit:
* Filename..: /usr/share/wordlists/sqlmap.txt
* Passwords.: 1406529
* Bytes.....: 12790573
* Keyspace..: 1406529

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit => s

Session..........: hashcat
Status...........: Running
Hash.Type........: md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)
Hash.Target......: $1$uOM6WNc4$r3ZGeSB11q6UUSILqek3J1
Time.Started.....: Sat Nov 24 22:37:25 2018 (26 secs)
Time.Estimated...: Sat Nov 24 22:40:46 2018 (2 mins, 55 secs)
Guess.Base.......: File (/usr/share/wordlists/sqlmap.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#2.........:     6969 H/s (9.09ms) @ Accel:256 Loops:125 Thr:1 Vec:8
Recovered........: 0/1 (0.00%) Digests, 0/1 (0.00%) Salts
Progress.........: 183808/1406529 (13.07%)
Rejected.........: 0/183808 (0.00%)
Restore.Point....: 183808/1406529 (13.07%)
Restore.Sub.#2...: Salt:0 Amplifier:0-1 Iteration:375-500
Candidates.#2....: 6104484 -> 61758102mt

[s]tatus [p]ause [b]ypass [c]heckpoint [q]uit =>
Packages and Binaries:
hashcat
World’s fastest and most advanced password recovery utility
Hashcat supports five unique modes of attack for over 300 highly-optimized
hashing algorithms. hashcat currently supports CPUs, GPUs, and other
hardware accelerators on Linux, and has facilities to help enable
distributed password cracking.
Examples of hashcat supported hashing algorithms are:
MD5, HMAC-MD5, SHA1, HMAC-SHA1, MySQL323, MySQL4.1/MySQL5, phpass,
MD5(Wordpress), MD5(phpBB3), MD5(Joomla), md5crypt, MD5(Unix),
FreeBSD MD5, Cisco-IOS, MD4, NTLM, Domain Cached Credentials (DCC),
MS Cache, SHA256, HMAC-SHA256, md5apr1, MD5(APR), Apache MD5, SHA512,
HMAC-SHA512, Cisco-PIX, Cisco-ASA, WPA/WPA2, Double MD5, bcrypt,
Blowfish(OpenBSD), MD5(Sun), Double SHA1, SHA-3(Keccak), Half MD5,
Password Safe SHA-256, IKE-PSK MD5, IKE-PSK SHA1,
NetNTLMv1-VANILLA/NetNTLMv1-ESS, NetNTLMv2, Cisco-IOS SHA256,
Android PIN, AIX {smd5}, AIX {ssha256}, AIX {ssha512}, AIX {ssha1},
GOST, GOST R 34, Fortigate (FortiOS), OS X v10.8+, GRUB 2, IPMI2, RAKP,
HMAC-SHA1, sha256crypt, SHA256(Unix), Drupal7, WBB3, scrypt, Cisco $8$,
Cisco $9$, Radmin2, Django (PBKDF2-SHA256), Cram MD5, SAP, iSSHA-1,
PrestaShop, PostgreSQL, Challenge-Response Authentication (MD5),
MySQL Challenge-Response, Authentication (SHA1),
SIP digest authentication (MD5), Plaintext, Joomla < 2.5.18, PostgreSQL,
osCommerce, xt:Commerce, Skype, nsldap, Netscape, LDAP, nsldaps,
SSHA-1(Base64), Oracle S: Type (Oracle 11+), SMF > v1.1, OS X v10.4,
v10.5, v10.6, EPi, Django (SHA-1), MSSQL(2000), MSSQL(2005),
PeopleSoft, EPiServer 6.x < v4, hMailServer, SSHA-512(Base64),
LDAP {SSHA512}, OS X v10.7, MSSQL(2012 & 2014), vBulletin < v3.8.5,
PHPS, vBulletin > v3.8.5, IPB2+, MyBB1.2+, Mediawiki B type,
WebEdition CMS, Redmine.
Hashcat offers multiple attack modes for obtaining effective and
complex coverage over a hash’s keyspace. These modes are:
Brute-Force attack
Combinator attack
Dictionary attack
Fingerprint attack
Hybrid attack
Mask attack
Permutation attack
Rule-based attack
Table-Lookup attack
Toggle-Case attack
PRINCE attack
Installed size: 119.52 MB
How to install: sudo apt install hashcat
Dependencies:hashcat-data
libc6
libminizip1t64
libxxhash0
pocl-opencl-icd | opencl-icd
zlib1g

hashcat
Advanced CPU-based password recovery utility
root@kali:~# hashcat -h
hashcat (v7.1.2) starting in help mode

Usage: hashcat [options]... hash|hashfile|hccapxfile [dictionary|mask|directory]...

- [ Options ] -

 Options Short / Long           | Type | Description                                          | Example
================================+======+======================================================+=======================
 -m, --hash-type                | Num  | Hash-type, references below (otherwise autodetect)   | -m 1000
 -a, --attack-mode              | Num  | Attack-mode, see references below                    | -a 3
 -V, --version                  |      | Print version                                        |
 -h, --help                     |      | Print help. Use -hh to show all supported hash-modes | -h or -hh
     --quiet                    |      | Suppress output                                      |
     --hex-charset              |      | Assume charset is given in hex                       |
     --hex-salt                 |      | Assume salt is given in hex                          |
     --hex-wordlist             |      | Assume words in wordlist are given in hex            |
     --force                    |      | Ignore warnings                                      |
     --deprecated-check-disable |      | Enable deprecated plugins                            |
     --status                   |      | Enable automatic update of the status screen         |
     --status-json              |      | Enable JSON format for status output                 |
     --status-timer             | Num  | Sets seconds between status screen updates to X      | --status-timer=1
     --stdin-timeout-abort      | Num  | Abort if there is no input from stdin for X seconds  | --stdin-timeout-abort=300
     --machine-readable         |      | Display the status view in a machine-readable format |
     --keep-guessing            |      | Keep guessing the hash after it has been cracked     |
     --self-test-disable        |      | Disable self-test functionality on startup           |
     --loopback                 |      | Add new plains to induct directory                   |
     --markov-hcstat2           | File | Specify hcstat2 file to use                          | --markov-hcstat2=my.hcstat2
     --markov-disable           |      | Disables markov-chains, emulates classic brute-force |
     --markov-classic           |      | Enables classic markov-chains, no per-position       |
     --markov-inverse           |      | Enables inverse markov-chains, no per-position       |
 -t, --markov-threshold         | Num  | Threshold X when to stop accepting new markov-chains | -t 50
     --metal-compiler-runtime   | Num  | Abort Metal kernel build after X seconds of runtime  | --metal-compiler-runtime=180
     --runtime                  | Num  | Abort session after X seconds of runtime             | --runtime=10
     --session                  | Str  | Define specific session name                         | --session=mysession
     --restore                  |      | Restore session from --session                       |
     --restore-disable          |      | Do not write restore file                            |
     --restore-file-path        | File | Specific path to restore file                        | --restore-file-path=x.restore
 -o, --outfile                  | File | Define outfile for recovered hash                    | -o outfile.txt
     --outfile-format           | Str  | Outfile format to use, separated with commas         | --outfile-format=1,3
     --outfile-json             |      | Force JSON format in outfile format                  |
     --outfile-autohex-disable  |      | Disable the use of $HEX[] in output plains           |
     --outfile-check-timer      | Num  | Sets seconds between outfile checks to X             | --outfile-check-timer=30
     --wordlist-autohex-disable |      | Disable the conversion of $HEX[] from the wordlist   |
 -p, --separator                | Char | Separator char for hashlists and outfile             | -p :
     --stdout                   |      | Do not crack a hash, instead print candidates only   |
     --show                     |      | Compare hashlist with potfile; show cracked hashes   |
     --left                     |      | Compare hashlist with potfile; show uncracked hashes |
     --username                 |      | Enable ignoring of usernames in hashfile             |
     --dynamic-x                |      | Ignore $dynamic_X$ prefix in hashes                  |
     --remove                   |      | Enable removal of hashes once they are cracked       |
     --remove-timer             | Num  | Update input hash file each X seconds                | --remove-timer=30
     --potfile-disable          |      | Do not write potfile                                 |
     --potfile-path             | File | Specific path to potfile                             | --potfile-path=my.pot
     --encoding-from            | Code | Force internal wordlist encoding from X              | --encoding-from=iso-8859-15
     --encoding-to              | Code | Force internal wordlist encoding to X                | --encoding-to=utf-32le
     --debug-mode               | Num  | Defines the debug mode (hybrid only by using rules)  | --debug-mode=4
     --debug-file               | File | Output file for debugging rules                      | --debug-file=good.log
     --induction-dir            | Dir  | Specify the induction directory to use for loopback  | --induction=inducts
     --outfile-check-dir        | Dir  | Specify the directory to monitor 3rd party outfiles  | --outfile-check-dir=x
     --logfile-disable          |      | Disable the logfile                                  |
     --hccapx-message-pair      | Num  | Load only message pairs from hccapx matching X       | --hccapx-message-pair=2
     --nonce-error-corrections  | Num  | The BF size range to replace AP's nonce last bytes   | --nonce-error-corrections=16
     --keyboard-layout-mapping  | File | Keyboard layout mapping table for special hash-modes | --keyb=german.hckmap
     --truecrypt-keyfiles       | File | Keyfiles to use, separated with commas               | --truecrypt-keyf=x.png
     --veracrypt-keyfiles       | File | Keyfiles to use, separated with commas               | --veracrypt-keyf=x.txt
     --veracrypt-pim-start      | Num  | VeraCrypt personal iterations multiplier start       | --veracrypt-pim-start=450
     --veracrypt-pim-stop       | Num  | VeraCrypt personal iterations multiplier stop        | --veracrypt-pim-stop=500
 -b, --benchmark                |      | Run benchmark of selected hash-modes                 |
     --benchmark-all            |      | Run benchmark of all hash-modes (requires -b)        |
     --benchmark-min            |      | Set benchmark min hash-mode (requires -b)            | --benchmark-min=100
     --benchmark-max            |      | Set benchmark max hash-mode (requires -b)            | --benchmark-max=1000
     --speed-only               |      | Return expected speed of the attack, then quit       |
     --progress-only            |      | Return ideal progress step size and time to process  |
 -c, --segment-size             | Num  | Sets size in MB to cache from the wordfile to X      | -c 32
     --bitmap-min               | Num  | Sets minimum bits allowed for bitmaps to X           | --bitmap-min=24
     --bitmap-max               | Num  | Sets maximum bits allowed for bitmaps to X           | --bitmap-max=24
     --bridge-parameter1        | Str  | Sets the generic parameter 1 for a Bridge            |
     --bridge-parameter2        | Str  | Sets the generic parameter 2 for a Bridge            |
     --bridge-parameter3        | Str  | Sets the generic parameter 3 for a Bridge            |
     --bridge-parameter4        | Str  | Sets the generic parameter 4 for a Bridge            |
     --cpu-affinity             | Str  | Locks to CPU devices, separated with commas          | --cpu-affinity=1,2,3
     --hook-threads             | Num  | Sets number of threads for a hook (per compute unit) | --hook-threads=8
 -H, --hash-info                |      | Show information for each hash-mode                  | -H or -HH
     --example-hashes           |      | Alias of --hash-info                                 |
     --backend-ignore-cuda      |      | Do not try to open CUDA interface on startup         |
     --backend-ignore-hip       |      | Do not try to open HIP interface on startup          |
     --backend-ignore-metal     |      | Do not try to open Metal interface on startup        |
     --backend-ignore-opencl    |      | Do not try to open OpenCL interface on startup       |
 -I, --backend-info             |      | Show system/environment/backend API info             | -I or -II
 -d, --backend-devices          | Str  | Backend devices to use, separated with commas        | -d 1
 -Y, --backend-devices-virtmulti| Num  | Spawn X virtual instances on a real device           | -Y 8
 -R, --backend-devices-virthost | Num  | Sets the real device to create virtual instances     | -R 1
     --backend-devices-keepfree | Num  | Keep specified percentage of device memory free      | --backend-devices-keepfree=5
 -D, --opencl-device-types      | Str  | OpenCL device-types to use, separated with commas    | -D 1
 -O, --optimized-kernel-enable  |      | Enable optimized kernels (limits password length)    |
 -M, --multiply-accel-disable   |      | Disable multiply kernel-accel with processor count   |
 -w, --workload-profile         | Num  | Enable a specific workload profile, see pool below   | -w 3
 -n, --kernel-accel             | Num  | Manual workload tuning, set outerloop step size to X | -n 64
 -u, --kernel-loops             | Num  | Manual workload tuning, set innerloop step size to X | -u 256
 -T, --kernel-threads           | Num  | Manual workload tuning, set thread count to X        | -T 64
     --backend-vector-width     | Num  | Manually override backend vector-width to X          | --backend-vector-width=4
     --spin-damp                | Num  | Use CPU for device synchronization, in percent       | --spin-damp=10
     --hwmon-disable            |      | Disable temperature and fanspeed reads and triggers  |
     --hwmon-temp-abort         | Num  | Abort if temperature reaches X degrees Celsius       | --hwmon-temp-abort=100
     --scrypt-tmto              | Num  | Manually override TMTO value for scrypt to X         | --scrypt-tmto=3
 -s, --skip                     | Num  | Skip X words from the start                          | -s 1000000
 -l, --limit                    | Num  | Limit X words from the start + skipped words         | -l 1000000
     --keyspace                 |      | Show keyspace base:mod values and quit               |
     --total-candidates         |      | Show total candidate count (base*mod) and quit       |
 -j, --rule-left                | Rule | Single rule applied to each word from left wordlist  | -j 'c'
 -k, --rule-right               | Rule | Single rule applied to each word from right wordlist | -k '^-'
 -r, --rules-file               | File | Multiple rules applied to each word from wordlists   | -r rules/best64.rule
 -g, --generate-rules           | Num  | Generate X random rules                              | -g 10000
     --generate-rules-func-min  | Num  | Force min X functions per rule                       |
     --generate-rules-func-max  | Num  | Force max X functions per rule                       |
     --generate-rules-func-sel  | Str  | Pool of rule operators valid for random rule engine  | --generate-rules-func-sel=ioTlc
     --generate-rules-seed      | Num  | Force RNG seed set to X                              |
 -1, --custom-charset1          | CS   | User-defined charset ?1                              | -1 ?l?d?u
 -2, --custom-charset2          | CS   | User-defined charset ?2                              | -2 ?l?d?s
 -3, --custom-charset3          | CS   | User-defined charset ?3                              |
 -4, --custom-charset4          | CS   | User-defined charset ?4                              |
 -5, --custom-charset5          | CS   | User-defined charset ?5                              |
 -6, --custom-charset6          | CS   | User-defined charset ?6                              |
 -7, --custom-charset7          | CS   | User-defined charset ?7                              |
 -8, --custom-charset8          | CS   | User-defined charset ?8                              |
     --identify                 |      | Shows all supported algorithms for input hashes      | --identify my.hash
 -i, --increment                |      | Enable mask increment mode                           |
 -ii,--increment-inverse        |      | Increment from right-to-left                         |
     --increment-min            | Num  | Start mask incrementing at X                         | --increment-min=4
     --increment-max            | Num  | Stop mask incrementing at X                          | --increment-max=8
 -S, --slow-candidates          |      | Enable slower (but advanced) candidate generators    |
     --bypass-delay             | Num  | Seconds delay between checking bypass threshold      | --bypass-delay=5
     --bypass-threshold         | Num  | Minimum amount of founds to avoid being bypassed     | --bypass-threshold=5
     --brain-server             |      | Enable brain server                                  |
     --brain-server-timer       | Num  | Update the brain server dump each X seconds (min:60) | --brain-server-timer=300
 -z, --brain-client             |      | Enable brain client, activates -S                    |
     --brain-client-features    | Num  | Define brain client features, see below              | --brain-client-features=3
     --brain-host               | Str  | Brain server host (IP or domain)                     | --brain-host=127.0.0.1
     --brain-port               | Port | Brain server port                                    | --brain-port=13743
     --brain-password           | Str  | Brain server authentication password                 | --brain-password=bZfhCvGUSjRq
     --brain-session            | Hex  | Overrides automatically calculated brain session     | --brain-session=0x2ae611db
     --brain-session-whitelist  | Hex  | Allow given sessions only, separated with commas     | --brain-session-whitelist=0x2ae611db
     --color-cracked            |      | Enables color output for cracked hashes              |

- [ Hash Modes ] -

  please use -hh to show all supported Hash Modes

- [ Brain Client Features ] -

  # | Features
 ===+========
  1 | Send hashed passwords
  2 | Send attack positions
  3 | Send hashed passwords and attack positions

- [ Outfile Formats ] -

  # | Format
 ===+========
  1 | hash[:salt]
  2 | plain
  3 | hex_plain
  4 | crack_pos
  5 | timestamp absolute
  6 | timestamp relative

- [ Rule Debugging Modes ] -

  # | Format
 ===+========
  1 | Finding-Rule
  2 | Original-Word
  3 | Original-Word:Finding-Rule
  4 | Original-Word:Finding-Rule:Processed-Word
  5 | Original-Word:Finding-Rule:Processed-Word:Wordlist

- [ Attack Modes ] -

  # | Mode
 ===+======
  0 | Straight
  1 | Combination
  3 | Brute-force
  6 | Hybrid Wordlist + Mask
  7 | Hybrid Mask + Wordlist
  9 | Association

- [ Built-in Charsets ] -

  ? | Charset
 ===+=========
  l | abcdefghijklmnopqrstuvwxyz [a-z]
  u | ABCDEFGHIJKLMNOPQRSTUVWXYZ [A-Z]
  d | 0123456789                 [0-9]
  h | 0123456789abcdef           [0-9a-f]
  H | 0123456789ABCDEF           [0-9A-F]
  s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
  a | ?l?u?d?s
  b | 0x00 - 0xff

- [ OpenCL Device Types ] -

  # | Device Type
 ===+=============
  1 | CPU
  2 | GPU
  3 | FPGA, DSP, Co-Processor

- [ Workload Profiles ] -

  # | Performance | Runtime | Power Consumption | Desktop Impact
 ===+=============+=========+===================+=================
  1 | Low         |   2 ms  | Low               | Minimal
  2 | Default     |  12 ms  | Economic          | Noticeable
  3 | High        |  96 ms  | High              | Unresponsive
  4 | Nightmare   | 480 ms  | Insane            | Headless

- [ License ] -

  hashcat is licensed under the MIT license
  Copyright and license terms are listed in docs/license.txt

- [ Basic Examples ] -

  Attack-          | Hash- |
  Mode             | Type  | Example command
 ==================+=======+==================================================================
  Wordlist         | $P$   | hashcat -a 0 -m 400 example400.hash example.dict
  Wordlist + Rules | MD5   | hashcat -a 0 -m 0 example0.hash example.dict -r rules/best64.rule
  Brute-Force      | MD5   | hashcat -a 3 -m 0 example0.hash ?a?a?a?a?a?a
  Combinator       | MD5   | hashcat -a 1 -m 0 example0.hash example.dict example.dict
  Association      | $1$   | hashcat -a 9 -m 500 example500.hash 1word.dict -r rules/best64.rule

If you still have no idea what just happened, try the following pages:

* https://hashcat.net/wiki/#howtos_videos_papers_articles_etc_in_the_wild
* https://hashcat.net/faq/

If you think you need help by a real human come to the hashcat Discord:

* https://hashcat.net/discord

hashcat-data
Data files for hashcat advanced password recovery utility
Hashcat is an advanced CPU/GPU-based password recovery utility supporting
seven unique modes of attack for over 100 optimized hashing algorithms.
This package contains the data files for hashcat, including charsets,
rules, salts, tables and Python tools.
Installed size: 31.54 MB
How to install: sudo apt install hashcat-data
Dependencies:python3


Learn more with OffSec
Want to learn more about hashcat? get access to in-depth training and hands-on labs:
PEN-200: 16.2. Password Attacks: Password Cracking Fundamentals
PEN-200 course


Updated on: 2025-Dec-09

 Edit this page

hash-identifier
hashdeep


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