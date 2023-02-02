import os
import re
import subprocess as sub

from utils import findKnowledgeClientByKid

from macros import REPO_DIR

def showInfomation(kid):
    k = findKnowledgeClientByKid(kid)

    print('===> Display Knowledge Information --- id', kid)
    client, sha, url, lib, old, new, test = k['client'], k['sha'], k['url'], k['lib'], k['old'], k['new'], k['test']
    print(f"client: {client}, \nsha: {sha}, \nurl: {url}, \nlib: {lib}, \nold version: {old}, \nnew version: {new}, \ntest: {test}")


def downloadTargetClient(kid):
    k = findKnowledgeClientByKid(kid)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Download Target Client --- id', kid)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        sub.run('git clone ' + url, shell=True)
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout ' + sha, shell=True)


def compileTargetClient(kid):
    k = findKnowledgeClientByKid(kid)
    client= k['client']

    print('===> Compile Target Client --- id', kid)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)

    sub.run('mvn install -DskipTests -fn', shell=True)


def TestTargetClient(kid):
    k = findKnowledgeClientByKid(kid)
    client, lib, test = k['client'], k['lib'], k['test']
    
    print('===> Test Target Client --- id', kid)
    print('Current library: ', lib)
    
    CURRENT_CLIENT = REPO_DIR + '/' + client
    checkLibVersion(lib, CURRENT_CLIENT)
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    print('===>' * 10)

    sub.run('mvn test -D test=' + test, shell=True)


def updateToNewVersion(kid):
    k = findKnowledgeClientByKid(kid)

    print('===> Update Library To New Version --- id', kid)
    client, lib, new, test = k['client'], k['lib'], k['new'], k['test']

    

    CURRENT_CLIENT = REPO_DIR + '/' + client
    changeLibVersion(lib, new, CURRENT_CLIENT)
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')

    
def checkoutBefore(kid):
    k = findKnowledgeClientByKid(kid)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to Before Version --- id', kid)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout before', shell=True)

def checkoutAfter(kid):
    k = findKnowledgeClientByKid(kid)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to After Version --- id', kid)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git checkout after', shell=True)

def checkDiff(kid):
    k = findKnowledgeClientByKid(kid)

    client, sha, url = k['client'], k['sha'], k['url']

    print('===> Checkout to After Version --- id', kid)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
    os.chdir(CURRENT_CLIENT)
    sub.run('git diff before after', shell=True)




def showIncompatibility(kid):
    showInfomation(kid)
    downloadTargetClient(kid)
    compileTargetClient(kid)
    TestTargetClient(kid)
    updateToNewVersion(kid)
    TestTargetClient(kid)


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
    