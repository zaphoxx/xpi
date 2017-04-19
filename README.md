# xpi
xpi - tool for xpath injection (very rudimentary and basic)


S:\DEV\archive\scripts>python xpi.py -h

        @@@  @@@ @@@@@@@  @@@
        @@!  !@@ @@!  @@@ @@!
         !@@!@!  @!@@!@!  !!@
         !: :!!  !!:      !!:
        :::  :::  :       :     Debug Rabbit

[+] xpi 0.1a (zaphoxx) by not disclosed yet

[Status] parse input parameters
usage: xpi.py [-h] -r [-x EXCLUDE] [--useCookie]

optional arguments:
  -h, --help            show this help message and exit
  -r, --request         sample header request file
  -x EXCLUDE, --exclude parameters to exclude from condition
  --useCookie           switch to cookie injection

see example below:


S:\DEV\archive\scripts>python xpi.py -r "exampleheader.txt"

        @@@  @@@ @@@@@@@  @@@
        @@!  !@@ @@!  @@@ @@!
         !@@!@!  @!@@!@!  !!@
         !: :!!  !!:      !!:
        :::  :::  :       :     Debug Rabbit

[+] xpi 0.1a (zaphoxx) by not disclosed yet

[Status] parse input parameters
[+] -----------------------------------------
[+] header request fields from header file:
        [REQUEST] GET /php/search.php HTTP/1.1
[!!!] Did not find any RequestParameters in provided Header
        [+] Host: www.fishyfishy.con
        [+] User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
        [+] Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        [+] Accept-Language: en-US,en;q=0.5
        [+] Accept-Encoding: gzip, deflate
        [+] Cookie: username=zaphoxx;passwd=sosecret
                [Cookie] username = zaphoxx
                [Cookie] passwd = sosecret
        [+] DNT: 1
        [+] Connection: keep-alive
[STATUS] Connect to target 'www.fishyfishy.con'
[STATUS] Connect to target 'www.fishyfishy.con'

