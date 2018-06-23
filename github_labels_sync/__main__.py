import sys

from github_labels_sync import cli

if __name__ == '__main__':
    argv = sys.argv[:]
    argv[0] = 'python3 -m github_label_sync'
    try:
        sys.exit(cli.main(sys.argv) or 0)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
