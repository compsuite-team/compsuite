import os
import re
import subprocess as sub

from utils import findIncompatibilityById
from macros import REPO_DIR

def showInfomation(id):
    incomp = findIncompatibilityById(id)

    print('===> Display Incompatibility Information --- id', id)
    client, sha, url, lib, old, new, test = incomp['client'], incomp['sha'], incomp['url'], incomp['lib'], incomp['old'], incomp['new'], incomp['test']
    print(f"client: {client}, \nsha: {sha}, \nurl: {url}, \nlib: {lib}, \nold version: {old}, \nnew version: {new}, \ntest: {test}")


def downloadTargetClient(id):
    k = findIncompatibilityById(id)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Download Target Client --- id', id)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        sub.run('git clone ' + url, shell=True)
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout ' + sha, shell=True)


def compileTargetClient(id):
    k = findIncompatibilityById(id)
    client= k['client']

    print('===> Compile Target Client --- id', id)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)

    sub.run('mvn install -DskipTests -fn', shell=True)


def TestTargetClient(id):
    k = findIncompatibilityById(id)
    client, lib, test = k['client'], k['lib'], k['test']
    
    print('===> Test Target Client --- id', id)
    print('Current library: ', lib)
    
    CURRENT_CLIENT = REPO_DIR + '/' + client
    checkLibVersion(lib, CURRENT_CLIENT)
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    print('===>' * 10)

    sub.run('mvn test -D test=' + test, shell=True)


def updateToNewVersion(id):
    k = findIncompatibilityById(id)

    print('===> Update Library To New Version --- id', id)
    client, lib, new, test = k['client'], k['lib'], k['new'], k['test']

    

    CURRENT_CLIENT = REPO_DIR + '/' + client
    changeLibVersion(lib, new, CURRENT_CLIENT)
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')

    
def checkoutBefore(id):
    k = findIncompatibilityById(id)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to Before Version --- id', id)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout before', shell=True)

def checkoutAfter(id):
    k = findIncompatibilityById(id)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to After Version --- id', id)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout after', shell=True)

def checkDiff(id):
    k = findIncompatibilityById(id)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to After Version --- id', id)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git diff before after', shell=True)


def findInfo(id):
    pass


def showIncompatibility(id):
    showInfomation(id)
    downloadTargetClient(id)
    compileTargetClient(id)
    TestTargetClient(id)
    updateToNewVersion(id)
    TestTargetClient(id)






# ========= Auxiliary functions ==========
def checkLibVersion(lib, client_dir):
    for dir_path, subpaths, files in os.walk(client_dir):
        for f in files:
            if f == 'pom.xml':
                pom_file = dir_path + '/' + f
                checkLibVersionOfOnePomFile(lib, pom_file)

def checkLibVersionOfOnePomFile(lib, pom_file):
    fr = open(pom_file, 'r')
    lines = fr.readlines()
    fr.close()
    group_id = lib.split(':')[0]
    artifact_id = lib.split(':')[1]
    for i in range(len(lines)):
        if '<groupId>' + group_id + '</groupId>' in lines[i]:
            if '<artifactId>' + artifact_id + '</artifactId>' in lines[i + 1]:
                version = re.findall('\<version\>(.*?)\<\/version\>', lines[i + 2])
                print("library version is :", version[0])



def changeLibVersion(lib, version, client_dir):
    for dir_path, subpaths, files in os.walk(client_dir):
        for f in files:
            if f == 'pom.xml':
                pom_file = dir_path + '/' + f
                changeLibVersionOfOnePomFile(lib, version, pom_file)

def changeLibVersionOfOnePomFile(lib, version, pom_file):
    fr = open(pom_file, 'r')
    lines = fr.readlines()
    fr.close()
    group_id = lib.split(':')[0]
    artifact_id = lib.split(':')[1]
    for i in range(len(lines)):
        if '<groupId>' + group_id + '</groupId>' in lines[i]:
            if '<artifactId>' + artifact_id + '</artifactId>' in lines[i + 1]:
                lines[i + 2] = re.sub('\<version\>.*\<\/version\>',
                                      '<version>' + version + '</version>',
                                      lines[i + 2])
                print('Updated library version: ', version)
    fw = open(pom_file, 'w')
    fw.write(''.join(lines))
    fw.close()
    