import argparse
import sys

from methods import *
from macros import *


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    # parser.add_argument('--id', help='The Subject ID', required=False)
    parser.add_argument('--info', help='Information', required=False)
    parser.add_argument('--download', help='Download Default Version Client', required=False)
    parser.add_argument('--compile', help='Compile Target Client', required=False)
    parser.add_argument('--testold', help='Test Target Method', required=False)
    parser.add_argument('--testnew', help='Test Target Method', required=False)
    parser.add_argument('--incompat', help='Incompat', required=False)
    # parser.add_argument('--diff', help='Difference between old and new version', action='store_true', required=False)
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

    if opts.info:
        showInfomation(opts.info)
        exit(0)

    if opts.download:
        downloadTargetClient(opts.download)
        exit(0)

    if opts.compile:
        compileTargetClient(opts.compile)
        exit(0)

    if opts.testold:
        testTargetClientOld(opts.testold)
        exit(0)
    
    if opts.testnew:
        testTargetClientNew(opts.testnew)
        exit(0)
    
    if opts.incompat:
        downloadTargetClient(opts.incompat)
        compileTargetClient(opts.incompat)
        testTargetClientOldToNew(opts.incompat)
        exit(0)



    # if opts.id:
    #     if opts.info:
    #         showInfomation(opts.id)
    #         exit(0)

    #     if opts.download:
    #         downloadTargetClient(opts.id)
    #         exit(0)

    #     if opts.compile:
    #         compileTargetClient(opts.id)
    #         exit(0)

    #     if opts.testold:
    #         TestTargetClientOld(opts.id)
    #         exit(0)
        
    #     if opts.testnew:
    #         TestTargetClientNew(opts.id)
    #         exit(0)

    #     if opts.incompat:
    #         downloadTargetClient(opts.id)
    #         compileTargetClient(opts.id)
    #         TestTargetClientOld(opts.id)
    #         TestTargetClientNew(opts.id)
    #         # showIncompatibility(opts.id)
    #         exit(0)

    #     # if opts.diff:
    #     #     pass

    #     if opts.find:
    #         findInfo(opts.id)
    #         exit(0)
