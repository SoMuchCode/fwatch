#!/usr/bin/env python
#
# Python 3.6
# Simple program to watch a file for changes and then execute a command
# if the watched file's timestamp changes.
# CLM 20170123
#
# https://stackoverflow.com/questions/182197/how-do-i-watch-a-file-for-changes-using-python#4690739
#
# fwatch.py -o -s 2 -v 1 "/path/name of file to watch" "command to execute"
# -o = use this switch if the program should not restart after file change detected
# -s 2 = how many seconds to sleep
# -v 0 = verbosity (0/1)
# -h = help

try:
    import time, os, sys
except:
    print('Cannot import library.')
    sys.exit(1)

# define some variables
# These are replaced by command line arguments
filename = 'file.txt'
sleeptime = 2
oneoff = 0
verb = 0
# You probably don't want to change these...
argcount = 0
counter = 0
command = 'echo What now?'

# Define our help output
def help():
    if os.name == 'nt':
        print('This program monitors a file for changes to its timestamp and executes a command when the timestamp changes.\n')
        print('fwatch usage:')
        print('fwatch.py /O /S 2 /V 1 "C:\\path\\name of file to watch" "command to execute"')
        print('    /O = use this switch if the program should NOT restart after file change detected')
        print('    /S 2 = how many seconds to sleep [1+]')
        print('    /V 0 = verbosity [0/1]')
        print('    /? = show this help')
        print('NOTE: Switches are optional, but "file name" and "command to execute" are required.')
    else:
        print('This program monitors a file for changes to its timestamp and executes a command when the timestamp changes.\n')
        print('fwatch usage:')
        print('fwatch.py -o -s 2 -v 1 "/path/name of file to watch" "command to execute"')
        print('    -o = use this switch if the program should NOT restart after file change detected')
        print('    -s 2 = how many seconds to sleep [1+]')
        print('    -v 0 = verbosity [0/1]')
        print('    -h = show this help')
        print('NOTE: Switches are optional, but "file name" and "command to execute" are required.')
    # pa pa
    sys.exit(0)

# variable used for 2 part command line args (-v 1 -s 4)
argumentswitch = 0

# Count command line arguments (switches)
for arg in sys.argv:
    argcount += 1

# user supplied no input... We should show the help  :)
if argcount <= 2:
    help()

# Process command line switches (required)
for arg in sys.argv:
    if verb >= 1:   # This can only happen if verb=1 is set above...
        print(counter, arg)
    if arg == '-o' or arg == '/o' or arg == '-O' or arg == '/O':
        oneoff = 1
    if arg == '-h' or arg == '/h' or arg == '-H' or arg == '/H':
        help()
    if arg == '--help' or arg == '/?' or arg == '--HELP' or arg == '--Help':
        help()
    if argumentswitch == 10:    # Verbose
        verb = int(arg)         # we want to define an integer, not a string
        if verb < 0:
            verb = 0
        if verb > 3:
            verb = 3
        argumentswitch = 0
    if argumentswitch == 5:     # Sleep Time
        sleeptime = int(arg)
        if sleeptime < 1:
            sleeptime = 2
        argumentswitch = 0
    if arg == '-v' or arg == '-V' or arg == '/v' or arg == '/V':
        argumentswitch = 10
    if arg == '-s' or arg == '/s' or arg == '-S' or arg == '/S':
        argumentswitch = 5
    if argcount == counter:
        # next to last argument, should be file to watch...
        if verb >= 1:
            print('File to watch:', arg)
        filename = arg
    if argcount == counter + 1:
        # last argument, should be command to execute, I hope they used quotes
        command = arg
        if verb >= 1:
            print('Command to execute:', arg)
    counter += 1


# Check the timestamp of the file we are watching
try:
    file_time_stored = os.stat(filename).st_mtime
    if verb >= 1:
        print('File to watch:', filename)
        print('File to watch timestamp:', file_time_stored)
except:
    if verb >= 1:
        print('Cannot find specified file:',filename)
    else:
        print('Cannot find specified file.')
    sys.exit(1)

# Main program loop
try:
    while True:
        file_time_current = os.stat(filename).st_mtime
        if file_time_stored != file_time_current:
            # Do something, file has changed
            if verb >= 1:
                print(filename, 'timestamp has changed.')
                print(file_time_current)
            else:
                print('File has changed.')
            # execute command
            try:
                os.system(command)
            except:
                print('Command malformed or illegal.')
                # pa pa
                print('Exiting...')
                sys.exit(1)
            if oneoff == 0:
                time.sleep(sleeptime)   # give above code a moment to complete
                file_time_stored = os.stat(filename).st_mtime   # reset the filewatcher
            else:
                # pa pa
                print('Exiting...')
                sys.exit(0)
        time.sleep(sleeptime)
except KeyboardInterrupt as errorCaught:      # CTRL C probably pressed
    print('Ctrl-C caught')
    print('Exiting...')
    sys.exit(0)
except Exception as errorCaught:                # Some other error
    print('Error:',str(errorCaught))
    print('Exiting...')
    sys.exit(0)

# we shouldn't be here...
# pa pa
if verb >= 1:
    print('This line should never execute, problem detected...')
print('Exiting...')
sys.exit(1)

    