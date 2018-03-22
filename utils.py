# utils for tool 
import os 
import sys 
import json 

from PySide2 import QtUiTools, QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as mc 
import maya.OpenMayaUI as mui 

def deleteUI(uiName): 
    if mc.window(uiName, exists=True): 
        mc.deleteUI(uiName)
        deleteUI(uiName)


def getMayaWindow(): 
    """ get maya window """ 
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QWidget)


def load_ui(uiFile, parent): 
    """ Qt Module to load .ui file """ 
    # read .ui directly

    moduleDir = os.path.dirname(uiFile)
    loader = QtUiTools.QUiLoader()
    loader.setWorkingDirectory(moduleDir)

    f = QtCore.QFile(uiFile)
    f.open(QtCore.QFile.ReadOnly)

    myWidget = loader.load(f, parent)
    f.close()

    return myWidget

def list_file(path): 
    return [d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d))]   

def list_folder(path): 
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]  

def open_file(path): 
    return mc.file(path, o=True, f=True)

def save_file(path, format): 
    mc.file(rename=path)
    return mc.file(save=True, type=format)

def get_data(var): 
    data = mc.optionVar(q=var)
    if not data: 
        data = dict()
        save_data(var, data)
        return get_data(var)

    return eval(data)

def save_data(var, data): 
    mc.optionVar(sv=(var, str(data)))


def json_dumper(path, data): 
    if not os.path.exists(os.path.dirname(path)): 
        os.makedirs(os.path.dirname(path))
    with open(path, 'w') as outfile:
        json.dump(data, outfile) 


def json_loader(path): 
    with open(path) as configData: 
        config = json.load(configData)
        return config


def search_for_version(filename, prefix='v', padding=3): 
    versionNumber = [a[0: padding] for a in filename.split(prefix) if a[0: padding].isdigit()]
    return '%s%s' % (prefix, versionNumber[0]) if versionNumber else ''

def increment_version(filename, prefix='v', padding=3): 
    version = search_for_version(filename, prefix=prefix, padding=padding)
    if version: 
        num = version.split(prefix)[-1]
        if num.isdigit(): 
            nextVersion = int(num) + 1
            newVersion = get_version(prefix, padding, nextVersion)
            return newVersion

    else: 
        return get_version(prefix, padding, 1)

def get_version(prefix, padding, version): 
    cmd = '"%0' + str(padding) + 'd" % version' 
    newVersion = '%s%s' % (prefix, eval(cmd))
    return newVersion


def calculate_version(files, prefix='v', padding=3): 
    allVersions = sorted([search_for_version(a).split(prefix)[-1] for a in files if search_for_version(a)])
    intVersions = [int(a) for a in allVersions if a.isdigit()]
    if intVersions: 
        nextVersion = max(intVersions) + 1
        return get_version(prefix=prefix, padding=padding, version=nextVersion)
    else: 
        return get_version(prefix=prefix, padding=padding, version=1)


