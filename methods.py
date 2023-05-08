import os
import re
import subprocess as sub

from utils import findIncompatibilityById
from macros import REPO_DIR
from macros import LOG_DIR

def showInfomation(id):
    incomp = findIncompatibilityById(id)

    print('===> Display Incompatibility Information --- id', id)
    client, sha, url, lib, old, new, test = incomp['client'], incomp['sha'], incomp['url'], incomp['lib'], incomp['old'], incomp['new'], incomp['test']
    print(f"client: {client}, \nsha: {sha}, \nurl: {url}, \nlib: {lib}, \nold version: {old}, \nnew version: {new}, \ntest: {test}")


def downloadTargetClient(id):
    incomp = findIncompatibilityById(id)
    client, lib, sha, url = incomp['client'], incomp['lib'], incomp['sha'], incomp['url']

    print('===> Download Target Client --- id', id)
    os.chdir(REPO_DIR)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        sub.run(f'git clone {url}', shell=True)
    else:
        print(f'{client} has already downloaded')
    os.chdir(CURRENT_CLIENT)
    branch = lib.replace(':', '--')
    sub.run(f'git checkout {branch}', shell=True)
    sub.run('git checkout .', shell=True)
    print('===> Client Info --- id', id)
    print(f"Client: {client}")
    print(f"Current Branch: {branch}")
    print(f"SHA of Base Version: {sha}")


def compileTargetClient(id):
    incomp = findIncompatibilityById(id)
    client = incomp['client']

    print('===> Compile Target Client --- id', id)
    CURRENT_CLIENT = REPO_DIR + '/' + client
    if not os.path.exists(CURRENT_CLIENT):
        print('Download target client first!')
        exit(0)
    os.chdir(CURRENT_CLIENT)
    REPO_LOG = LOG_DIR + '/' + client
    if not os.path.exists(REPO_LOG):
        os.makedirs(REPO_LOG)
    install_log = REPO_LOG + '/install.log'
    sub.run('mvn install -DskipTests -fn', shell=True, stdout=open(install_log, 'w'), stderr=sub.STDOUT)
    print('===> Client Info --- id', id)
    if isCompiled(install_log):
        print(f"{client} has been compiled successfully!")
    else:
        print(f"Compilation Failure")




def TestTargetClientOld(id):
    incomp = findIncompatibilityById(id)
    client, lib, test, old, submodule, test, test_cmd = incomp['client'], incomp['lib'], incomp['test'], incomp['old'], incomp['submodule'], incomp['test'], incomp['test_cmd']
    
    print('===> Test Target Client --- id', id)
    
    old_tag = lib.replace(':', '--') + '-' + old
    print(old_tag)
    if submodule != 'N/A':
        os.chdir(f'{REPO_DIR}/{client}/{submodule}')
    else:
        os.chdir(f'{REPO_DIR}/{client}')
    sub.run(f'git checkout {old_tag}', shell=True)

    CLIENT_LIB_LOG_DIR = LOG_DIR + '/' + client + '/' + lib
    if not os.path.exists(CLIENT_LIB_LOG_DIR):
        os.makedirs(CLIENT_LIB_LOG_DIR)

    old_test_log = CLIENT_LIB_LOG_DIR + '/' + old + '.log'
    
    if test_cmd != 'N/A':
        sub.run(test_cmd, shell=True, stdout=open(old_test_log, 'w'), stderr=sub.STDOUT)    
    else:
        sub.run(f"mvn test -fn -Drat.ignoreErrors=true -DtrimStackTrace=false -DfailIfNoTests=false -Dtest={test}", shell=True, stdout=open(old_test_log, 'w'), stderr=sub.STDOUT)

    print('===> Test Information --- id', id)
    print(f"Client: {client}")
    print(f"Library: {lib} {old}")
    print(f"Test: {test}")
    print("Result: ")
    with open(old_test_log, 'r') as fo:
        lines = fo.readlines()
        for i in range(len(lines)):
            if '<<< FAILURE!' in lines[i]:
                print(lines[i])
                print(lines[i + 1])
        else:
            print('TEST SUCCESS!')    


def TestTargetClientNew(id):
    incomp = findIncompatibilityById(id)
    client, lib, test, new, submodule, test, test_cmd = incomp['client'], incomp['lib'], incomp['test'], incomp['new'], incomp['submodule'], incomp['test'], incomp['test_cmd']
    
    print('===> Test Target Client --- id', id)
    
    new_tag = lib.replace(':', '--') + '-' + new
    print(new_tag)
    if submodule != 'N/A':
        os.chdir(f'{REPO_DIR}/{client}/{submodule}')
    else:
        os.chdir(f'{REPO_DIR}/{client}')
    sub.run(f'git checkout {new_tag}', shell=True)

    CLIENT_LIB_LOG_DIR = LOG_DIR + '/' + client + '/' + lib
    if not os.path.exists(CLIENT_LIB_LOG_DIR):
        os.makedirs(CLIENT_LIB_LOG_DIR)

    new_test_log = CLIENT_LIB_LOG_DIR + '/' + new + '.log'
    
    if test_cmd != 'N/A':
        sub.run(test_cmd, shell=True, stdout=open(new_test_log, 'w'), stderr=sub.STDOUT)    
    else:
        sub.run(f"mvn test -fn -Drat.ignoreErrors=true -DtrimStackTrace=false -DfailIfNoTests=false -Dtest={test}", shell=True, stdout=open(new_test_log, 'w'), stderr=sub.STDOUT)

    print('===> Test Information --- id', id)
    print(f"Client: {client}")
    print(f"Library: {lib} {new}")
    print(f"Test: {test}")
    print("Result: ")
    with open(new_test_log, 'r') as fo:
        lines = fo.readlines()
        for i in range(len(lines)):
            if '<<< FAILURE!' in lines[i]:
                print(lines[i], lines[i + 1])
                break
        else:
            print('TEST SUCCESS!')  




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
    
def isCompiled(install_log):
    with open(install_log, 'r') as f:
        lines = f.readlines()
    f.close()
    for line in lines:
        if 'BUILD SUCCESS' in line:
            return True
    else:
        return False