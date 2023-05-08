import argparse
import sys

from methods import *
from macros import *


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='The Subject ID', required=False)
    parser.add_argument('--info', help='Information', action='store_true', required=False)
    parser.add_argument('--download', help='Download Default Version Client', action='store_true', required=False)
    parser.add_argument('--compile', help='Compile Target Client', action='store_true', required=False)
    parser.add_argument('--testold', help='Test Target Method', action='store_true', required=False)
    parser.add_argument('--testnew', help='Test Target Method', action='store_true', required=False)
    parser.add_argument('--update', help='Update To New Version', action='store_true', required=False)
    parser.add_argument('--incompat', help='Incompat', action='store_true', required=False)
    parser.add_argument('--find', help='Find Infomation', action='store_true', required=False)
    

    if len(argv) == 0:
        parser.print_help()
        exit(1)
    opts = parser.parse_args(argv)
    return opts


if __name__ == '__main__':
    opts = parseArgs(sys.argv[1:])

    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    if opts.id:
        if opts.info:
            showInfomation(opts.id)
            exit(0)

        if opts.download:
            downloadTargetClient(opts.id)
            exit(0)

        if opts.compile:
            compileTargetClient(opts.id)
            exit(0)

        if opts.testold:
            TestTargetClientOld(opts.id)
            exit(0)
        
        if opts.testnew:
            TestTargetClientNew(opts.id)
            exit(0)

        if opts.update:
            updateToNewVersion(opts.id)
            exit(0)

        if opts.incompat:
            downloadTargetClient(opts.id)
            compileTargetClient(opts.id)
            TestTargetClientOld(opts.id)
            TestTargetClientNew(opts.id)
            # showIncompatibility(opts.id)
            exit(0)

        if opts.find:
            findInfo(opts.id)
            exit(0)
