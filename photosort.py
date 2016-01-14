#!/usr/bin/env python

import sys
import os
import argparse
import exifread
import jdatetime
from termcolor import colored, cprint


def senderror(errormsg, status=1):
    sys.stderr.write(colored('ERORR: %s\n' % (errormsg), 'red', attrs=['bold']))
    sys.exit(status)

parser = argparse.ArgumentParser(prog='sort.py', usage='%(prog)s -o DIR [FILES...]', description='Sort images based on date value in EXIF data.')
parser.add_argument("files", nargs='+', help="list of files to be processed")
parser.add_argument("-o", "--out", required=True, help="output directory")
parser.add_argument("-n", "--noact", required=False, action="store_true", help="no action, just simulate")
args = parser.parse_args()

# Check output directory exists
if not os.path.isdir(args.out):
    senderror('%s: No such file or directory' % (args.out))

# Check output directory is writable
if not os.access(args.out, os.W_OK):
    senderror('%s: Permission denied' % (args.out))

for file in args.files:

    try:
        f = open(file, 'rb')
    except IOError, Argument:
        print colored('%s: %s' % (file, Argument.strerror), 'red')
        continue
    else:
        tags = exifread.process_file(f)
        if not len(tags):
            print colored('%s: %s' % (file, 'No EXIF data found'), 'red')
            continue
        else:
            tag = 'EXIF DateTimeOriginal'
            if tag not in tags.keys():
                print colored('%s: %s' % (file, 'Tag not found in EXIF'), 'red')
                continue

            rawdate = str(tags[tag]).split()[0].split(':')
            jdate = jdatetime.date.fromgregorian(day=int(rawdate[2]),month=int(rawdate[1]),year=int(rawdate[0]))
            dirname = "%s/%s/%s/%s" % (args.out, jdate.year, '%.2d' % jdate.month, '%.2d' % jdate.day)
            if os.path.isfile('%s/%s' % (dirname,file.split('/')[-1])):
                print colored(('%s: %s' % (file, jdate)).ljust(80, '.') + '[ DU ]', 'red')
                continue

            if not os.access(file, os.R_OK):
                print colored(('%s: %s' % (file, jdate)).ljust(80, '.') + '[ NR ]', 'red')
                continue

            if not args.noact:
                os.system('mkdir -p %s' % (dirname))
                os.system('cp "%s" "%s"' % (file, dirname))

            print colored(('%s: %s' % (file, jdate)).ljust(80, '.') + '[ OK ]', 'cyan')

#
# for tag in tags.keys():
#    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#        print "Key: %s, value %s" % (tag, tags[tag])

