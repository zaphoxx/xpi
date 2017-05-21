# xpi (discontinued)
xpi - tool for xpath injection (very rudimentary and basic) to extract the password.

\xpi-master>python xpi.py --help
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        @@@  @@@ @@@@@@@  @@@
        @@!  !@@ @@!  @@@ @@!
         !@@!@!  @!@@!@!  !!@
         !: :!!  !!:      !!:
        :::  :::  :       :     Debug Rabbit

[+] xpi 0.1a (zaphoxx) by not disclosed yet
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
usage: xpi.py [-h] -r [-x EXCLUDE] [--useCookie] [--test] [-v] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  -r, --request     sample header request file
  -x EXCLUDE, --exclude EXCLUDE
                        parameters to exclude from condition
  --useCookie           switch to cookie injection
  --test                test header and connection
  -v                    show additional information
  --debug               show debug information

You need a valid header request file to run the script (see example file). also you need to exclude all parameters that are not part of the condition. Currently the parameter for modification still needs to manually changed in the py script itself. (at the moment the default value is "passwd").
