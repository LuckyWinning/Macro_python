# Macro_python
Add and xml file and highlight the important information

The code works similar to a command in terminal. It has flags for different situations, this could be seen in the menu with the flag -h -> 

C:\>python macro_english.py -h
usage: macro_english.py [-h] [-a ALERTS] [-c CATALOGUE] [-l LIST] [-o OUTPUT]
                        xml

Add the name of the xml file

positional arguments:
  xml                   Name of the file (in xml)

optional arguments:
  -h, --help            show this help message and exit
  -a ALERTS, --alerts ALERTS
                        Give the name of the file "bines" that have been
                        alerted alredy, in .txt format(default =
                        bines_alerted.txt)
  -c CATALOGUE, --catalogue CATALOGUE
                        Give the name of the file catalogue of "bines", in
                        .txt this file contains all of the "bines" (default =
                        catalogue.txt)
  -l LIST, --list LIST  Provide the whitelist file, in the correct format
                        (default = whitelist.txt)
  -o OUTPUT, --output OUTPUT
                        Specified if the output file will have a name (default
                        = output.txt)
                        
