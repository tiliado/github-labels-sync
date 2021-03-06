# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

import sys

from github_labels_sync import cli

if __name__ == '__main__':
    argv = sys.argv[:]
    argv[0] = 'gh-label-sync'
    try:
        sys.exit(cli.main(argv) or 0)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
