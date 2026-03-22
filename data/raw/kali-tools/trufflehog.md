trufflehog | Kali Linux Tools
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


trufflehog


version: 3.93.8 arch: amd64 arm64 trufflehog Homepage| Package Tracker| Source Code Repository
 Edit this page
Metapackages
everything


Packages & Binaries

trufflehogtrufflehog

LIGHT

DARK
Packages and Binaries:
trufflehog
Searches through git repositories for secrets
This package contains a utitlity to search through git repositories for
secrets, digging deep into commit history and branches. This is effective at
finding secrets accidentally committed.
Installed size: 116.26 MB
How to install: sudo apt install trufflehog
Dependencies:libc6

trufflehog
root@kali:~# trufflehog -h
usage: TruffleHog [<flags>] <command> [<args> ...]

TruffleHog is a tool for finding credentials.


Flags:
  -h, --[no-]help                Show context-sensitive help (also try
                                 --help-long and --help-man).
      --log-level=0              Logging verbosity on a scale of 0 (info) to 5
                                 (trace). Can be disabled with "-1".
      --[no-]profile             Enables profiling and sets a pprof and fgprof
                                 server on :18066.
  -j, --[no-]json                Output in JSON format.
      --[no-]json-legacy         Use the pre-v3.0 JSON format. Only works with
                                 git, gitlab, and github sources.
      --[no-]github-actions      Output in GitHub Actions format.
      --concurrency=6            Number of concurrent workers.
      --[no-]no-verification     Don't verify the results.
      --results=RESULTS          Specifies which type(s) of results to output:
                                 verified (confirmed valid by API),
                                 unknown (verification failed due to error),
                                 unverified (detected but not verified),
                                 filtered_unverified (unverified but would
                                 have been filtered out). Defaults to
                                 verified,unverified,unknown.
      --[no-]no-color            Disable colorized output
      --[no-]allow-verification-overlap
                                 Allow verification of similar credentials
                                 across detectors
      --[no-]filter-unverified   Only output first unverified result per
                                 chunk per detector if there are more than one
                                 results.
      --filter-entropy=FILTER-ENTROPY
                                 Filter unverified results with Shannon entropy.
                                 Start with 3.0.
      --max-decode-depth=5       Maximum depth of iterative decoding.
                                 Each decoder's output is fed back through all
                                 decoders, up to this limit. 1 = single pass, 2+
                                 = chained decoding (e.g., base64 inside utf16).
      --config=CONFIG            Path to configuration file.
      --[no-]print-avg-detector-time
                                 Print the average time spent on each detector.
      --[no-]no-update           Don't check for updates.
      --[no-]fail                Exit with code 183 if results are found.
      --[no-]fail-on-scan-errors
                                 Exit with non-zero error code if an error
                                 occurs during the scan.
      --verifier=VERIFIER ...    Set custom verification endpoints.
      --[no-]custom-verifiers-only
                                 Only use custom verification endpoints.
      --detector-timeout=DETECTOR-TIMEOUT
                                 Maximum time to spend scanning chunks per
                                 detector (e.g., 30s).
      --archive-max-size=ARCHIVE-MAX-SIZE
                                 Maximum size of archive to scan. (Byte units
                                 eg. 512B, 2KB, 4MB)
      --archive-max-depth=ARCHIVE-MAX-DEPTH
                                 Maximum depth of archive to scan.
      --archive-timeout=ARCHIVE-TIMEOUT
                                 Maximum time to spend extracting an archive.
      --include-detectors="all"  Comma separated list of detector types to
                                 include. Protobuf name or IDs may be used,
                                 as well as ranges.
      --exclude-detectors=EXCLUDE-DETECTORS
                                 Comma separated list of detector types to
                                 exclude. Protobuf name or IDs may be used,
                                 as well as ranges. IDs defined here take
                                 precedence over the include list.
      --[no-]no-verification-cache
                                 Disable verification caching
      --[no-]force-skip-binaries
                                 Force skipping binaries.
      --[no-]force-skip-archives
                                 Force skipping archives.
      --[no-]skip-additional-refs
                                 Skip additional references.
      --user-agent-suffix=USER-AGENT-SUFFIX
                                 Suffix to add to User-Agent.
      --[no-]version             Show application version.

Commands:
help [<command>...]
    Show help.

git [<flags>] <uri>
    Find credentials in git repositories.

github [<flags>]
    Find credentials in GitHub repositories.

github-experimental --repo=REPO [<flags>]
    Run an experimental GitHub scan. Must specify at least one experimental
    sub-module to run: object-discovery.

gitlab --token=TOKEN [<flags>]
    Find credentials in GitLab repositories.

filesystem [<flags>] [<path>...]
    Find credentials in a filesystem.

s3 [<flags>]
    Find credentials in S3 buckets.

gcs [<flags>]
    Find credentials in GCS buckets.

syslog --format=FORMAT [<flags>]
    Scan syslog

circleci --token=TOKEN
    Scan CircleCI

docker [<flags>]
    Scan Docker Image

travisci --token=TOKEN
    Scan TravisCI

postman [<flags>]
    Scan Postman

elasticsearch [<flags>]
    Scan Elasticsearch

jenkins --url=URL [<flags>]
    Scan Jenkins

huggingface [<flags>]
    Find credentials in HuggingFace datasets, models and spaces.

stdin
    Find credentials from stdin.

multi-scan
    Find credentials in multiple sources defined in configuration.

json-enumerator [<path>...]
    Find credentials from a JSON enumerator input.

analyze
    Analyze API keys for fine-grained permissions information.


Updated on: 2026-Mar-13

 Edit this page

tlssled
twofi


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