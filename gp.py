#!/usr/bin/env python
#

import sys
import argparse
import logging
import os
import re
import datetime
import finder
import pathlib


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    src = args.src
    dest = args.dest if args.dest else src
    dt_pattern = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
    media_finder = finder.Finder(src)

    if args.ge:
        dt_matched = dt_pattern.match(args.ge)
        if dt_matched:
            media_finder.ge(datetime.datetime(int(dt_matched.group(1)),
                                              int(dt_matched.group(2)),
                                              int(dt_matched.group(3))))
        else:
            print('--ge value is invalid')
            return

    if args.gt:
        dt_matched = dt_pattern.match(args.gt)
        if dt_matched:
            media_finder.gt(datetime.datetime(int(dt_matched.group(1)),
                                              int(dt_matched.group(2)),
                                              int(dt_matched.group(3))))
        else:
            print('--gt value is invalid')
            return

    for (name, dir_name) in media_finder.scan():
        file_src = os.path.join(src, name)
        dir_dest = os.path.join(dest, dir_name)
        file_dest = os.path.join(dir_dest, name)

        pathlib.Path(dir_dest).mkdir(parents=True, exist_ok=True)
        os.rename(file_src, file_dest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Group photos into folders by date.')
    parser.add_argument('--src',
                        help='Source directory of the photos')
    parser.add_argument('--dest',
                        help='Destination directory of the folders')
    parser.add_argument('--group-by',
                        help='Group by criteria, ex. name, date, etc.')
    parser.add_argument('--gt',
                        help='Greater than this date')
    parser.add_argument('--ge',
                        help='Greater or equal than this date')
    parser.add_argument('-v',
                        '--verbose',
                        help='increase output verbosity',
                        action='store_true')

    args = parser.parse_args()

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    main(args, loglevel)
