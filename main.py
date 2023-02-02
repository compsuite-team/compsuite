import argparse
import sys

from method import *
# from discovery.discovery import runKnowledgeDiscovery

from macros import *



def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='The Subject ID', required=False)
    parser.add_argument('--info', help='Information', action='store_true', required=False)
    parser.add_argument('--download', help='Download Default Version Client', action='store_true', required=False)
    parser.add_argument('--compile', help='Compile Target Client', action='store_true', required=False)
    parser.add_argument('--test', help='Test Target Method', action='store_true', required=False)
    parser.add_argument('--update', help='Update To New Version', action='store_true', required=False)
    parser.add_argument('--incompat', help='Incompat', action='store_true', required=False)
    parser.add_argument('--before', help='Checkout Before Version', action='store_true', required=False)
    parser.add_argument('--after', help='Checkout After Version', action='store_true', required=False)
    parser.add_argument('--diff', help='Different Between Two Versions', action='store_true', required=False)


    if len(argv) == 0:
        parser.print_help()
        exit(1)
    opts = parser.parse_args(argv)
    return opts

if __name__ == '__main__':
    opts = parseArgs(sys.argv[1:])

    if not os.path.exists(REPO_DIR):
        os.makedirs(REPO_DIR)

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

        if opts.test:
            TestTargetClient(opts.id)
            exit(0)

        if opts.update:
            updateToNewVersion(opts.id)
            exit(0)

        if opts.incompat:
            showIncompatibility(opts.id)
            exit(0)

        if opts.before:
            checkoutBefore(opts.id)
            exit(0)
        
        if opts.after:
            checkoutAfter(opts.id)
            exit(0)

        if opts.diff:
            checkDiff(opts.id)
            exit(0)

    # if opts.discover:
    #     if opts.id:
    #         runKnowledgeDiscoveryOnOneTest(opts.id)
    #     else:
    #         runKnowledgeDiscovery()
    #     exit(0)
    # if opts.merge:
    #     mergeKnowledge()
    #     exit(0)
    # if opts.check:
    #     if opts.id:
    #         runCheckOnOneCallSite(opts.id)
    #     exit(0)
    # if opts.score:
    #     genNumbersTexFile()
    #     genTableTexFile()
    #     exit(0)

