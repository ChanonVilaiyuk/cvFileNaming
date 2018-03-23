# v.0.0.1 polytag switcher
_title = 'cv File Naming Browser'
_version = 'v.0.2.0'
_des = 'beta'
uiName = 'EasySaveUI'

import os 
import sys 
from collections import OrderedDict
moduleDir = os.path.dirname(sys.modules[__name__].__file__)

from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools
from shiboken2 import wrapInstance 

import utils
reload(utils)
iconDir = '%s/icons' % moduleDir
iconData = utils.json_loader('%s/config.json' % iconDir)
versionConfig = utils.json_loader('%s/version_config.json' % moduleDir)

class Var: 
    browsePath = 'browsePath'
    e1CheckBox = 'e1CheckBox'
    e2CheckBox = 'e2CheckBox'
    e3CheckBox = 'e3CheckBox'
    c1CheckBox = 'c1CheckBox'
    c2CheckBox = 'c2CheckBox'
    e1LineEdit = 'e1LineEdit'
    e2LineEdit = 'e2LineEdit'
    e3LineEdit = 'e3LineEdit'
    c1LineEdit = 'c1LineEdit'
    c2LineEdit = 'c2LineEdit'
    vLineEdit = 'vLineEdit'
    dataName = 'cvSaveBackupPlusData'

    # icon config keyword
    ext = 'ext' 
    dir = 'dir'

    # version config key word
    prefix = 'prefix'
    padding = 'padding'

    # data type 
    folder = 'dir'
    file = 'file'
    back = 'back'

    # icons 
    forwardIcon = 'forward_icon.png'
    backIcon = 'back_icon.png'
    revIcon = 'rev_icon.png'


class SaveBackupPlus(QtWidgets.QMainWindow):
    """SaveBackupPlus"""
    def __init__(self, parent=None):
        super(SaveBackupPlus, self).__init__(parent)
        
        # load ui 
        uiFile = '%s/ui.ui' % moduleDir
        self.ui = utils.load_ui(uiFile, parent=parent)
        self.ui.show()
        self.ui.setWindowTitle('%s %s-%s' % (_title, _version, _des))

        # format
        self.format = {'ma': 'mayaAscii', 'mb': 'mayaBinary'}

        # cache 
        self.pathCaches = []
        self.cacheCount = 0

        self.init_functions()
        self.init_signals()

    def init_signals(self): 
        """ init signals """
        # browse button
        self.ui.browse_pushButton.clicked.connect(self.browse_dir)

        # custom element signals 
        self.ui.e1_checkBox.stateChanged.connect(self.generate_name)
        self.ui.e2_checkBox.stateChanged.connect(self.generate_name)
        self.ui.e3_checkBox.stateChanged.connect(self.generate_name)
        self.ui.custom1_checkBox.stateChanged.connect(self.generate_name)
        self.ui.custom2_checkBox.stateChanged.connect(self.generate_name)
        self.ui.version_checkBox.stateChanged.connect(self.generate_name)

        self.ui.e1_lineEdit.returnPressed.connect(self.generate_name)
        self.ui.e2_lineEdit.returnPressed.connect(self.generate_name)
        self.ui.e3_lineEdit.returnPressed.connect(self.generate_name)
        self.ui.customText1_lineEdit.returnPressed.connect(self.generate_name)
        self.ui.customText2_lineEdit.returnPressed.connect(self.generate_name)
        self.ui.version_lineEdit.returnPressed.connect(self.generate_name)

        # path edit 
        self.ui.path_lineEdit.returnPressed.connect(self.display_files)
        # format 
        self.ui.format_comboBox.currentIndexChanged.connect(self.generate_name)

        # open file 
        self.ui.open_pushButton.clicked.connect(self.open_file)
        # save file 
        self.ui.save_pushButton.clicked.connect(self.save_file)

        # naviate
        self.ui.listWidget.itemDoubleClicked.connect(self.navigate)

        # back / forward 
        self.ui.back_pushButton.clicked.connect(self.navigate_back)
        self.ui.forward_pushButton.clicked.connect(self.navigate_forward)



    def init_functions(self): 
        self.set_ui()
        self.set_format()
        self.restore_setting()
        self.display_files()
        self.add_cache(self.get_path())
        self.generate_name()


    def browse_dir(self): 
        data = utils.get_data(Var.dataName)
        lastSavePath = data.get(Var.browsePath, 'C:/')
        path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select a folder:', lastSavePath)
        
        if path: 
            self.browse(path)
            self.save_setting()


    def browse(self, path): 
        self.ui.path_lineEdit.setText(path)
        self.display_files()
        self.add_cache(path)

    def browse_cache(self, path): 
        self.ui.path_lineEdit.setText(path)
        self.display_files()



    def save_setting(self): 
        """ save user options setting """ 
        # save to customVar 
        data = utils.get_data(Var.dataName)
        # path 
        path = self.get_path()
        data.update({Var.browsePath: path})

        # element setting 
        e1CheckBox = self.ui.e1_checkBox.isChecked()
        e2CheckBox = self.ui.e2_checkBox.isChecked()
        e3CheckBox = self.ui.e3_checkBox.isChecked()
        c1CheckBox = self.ui.custom1_checkBox.isChecked()
        c2CheckBox = self.ui.custom2_checkBox.isChecked()

        # level setting 
        e1LineEdit = str(self.ui.e1_lineEdit.text())
        e2LineEdit = str(self.ui.e2_lineEdit.text())
        e3LineEdit = str(self.ui.e3_lineEdit.text())
        c1LineEdit = str(self.ui.customText1_lineEdit.text())
        c2LineEdit = str(self.ui.customText2_lineEdit.text())

        # add to data 
        data[Var.e1CheckBox] = e1CheckBox
        data[Var.e2CheckBox] = e2CheckBox
        data[Var.e3CheckBox] = e3CheckBox
        data[Var.c1CheckBox] = c1CheckBox
        data[Var.c2CheckBox] = c2CheckBox
        data[Var.e1LineEdit] = e1LineEdit
        data[Var.e2LineEdit] = e2LineEdit
        data[Var.e3LineEdit] = e3LineEdit
        data[Var.c1LineEdit] = c1LineEdit
        data[Var.c2LineEdit] = c2LineEdit

        utils.save_data(Var.dataName, data)
        return True

    def set_ui(self): 
        """ set ui icons """
        self.ui.forward_pushButton.setIcon(QtGui.QIcon('%s/%s' % (iconDir, Var.forwardIcon)))
        self.ui.back_pushButton.setIcon(QtGui.QIcon('%s/%s' % (iconDir, Var.backIcon)))


    def set_format(self): 
        """ set file format """ 
        self.ui.format_comboBox.clear()

        for i, format in enumerate(self.format): 
            self.ui.format_comboBox.addItem(format)
            self.ui.format_comboBox.setItemData(i, self.format[format], QtCore.Qt.UserRole)


    def restore_setting(self): 
        data = utils.get_data(Var.dataName)

        # path 
        lastSavePath = data.get(Var.browsePath, 'C:/')
        self.ui.path_lineEdit.setText(lastSavePath)

        # checkBox
        self.ui.e1_checkBox.setChecked(data.get(Var.e1CheckBox, True))
        self.ui.e2_checkBox.setChecked(data.get(Var.e2CheckBox, True))
        self.ui.e3_checkBox.setChecked(data.get(Var.e3CheckBox, True))
        self.ui.custom1_checkBox.setChecked(data.get(Var.c1CheckBox, True))
        self.ui.custom2_checkBox.setChecked(data.get(Var.c2CheckBox, True))

        self.ui.e1_lineEdit.setText(data.get(Var.e1LineEdit, '-3'))
        self.ui.e2_lineEdit.setText(data.get(Var.e2LineEdit, '-2'))
        self.ui.e3_lineEdit.setText(data.get(Var.e3LineEdit, '-1'))
        self.ui.customText1_lineEdit.setText(data.get(Var.c1LineEdit, 'custom'))
        self.ui.customText2_lineEdit.setText(data.get(Var.c2LineEdit, ''))



    def display_files(self): 
        """ display files in listWidget """ 
        path = self.get_path()
        path = path[:-1] if path[-1] == '/' else path
        
        if path and os.path.exists(path): 
            dirs = sorted(utils.list_folder(path))
            files = sorted(utils.list_file(path))
            self.ui.listWidget.clear()
            
            # add back 
            self.add_back_item(path)
            
            for folder in dirs: 
                data = [Var.folder, '%s/%s' % (path, folder)]
                self.add_item(folder, data, Var.folder)

            for filename in files: 
                data = [Var.file, '%s/%s' % (path, filename)]
                self.add_item(filename, data, Var.file)

            self.calculate_version(files)


    def add_item(self, text, data, type): 
        item = QtWidgets.QListWidgetItem(self.ui.listWidget)
        item.setText(text)
        item.setData(QtCore.Qt.UserRole, data)
        defaultIcon = iconData.get(Var.ext).get('.*')

        if type == Var.folder: 
            iconPath = '%s/%s' % (iconDir, iconData.get(Var.dir))
        
        if type == Var.file: 
            ext = os.path.splitext(text)[-1]
            iconPath = '%s/%s' % (iconDir, iconData.get(Var.ext).get(ext, defaultIcon))

        if type == Var.back: 
            iconPath = '%s/%s' % (iconDir, Var.revIcon)

        if iconPath: 
            iconWidget = QtGui.QIcon()
            iconWidget.addPixmap(QtGui.QPixmap(iconPath),QtGui.QIcon.Normal,QtGui.QIcon.Off)
            item.setIcon(iconWidget)


    def add_back_item(self, path): 
        display = '...'
        data = [Var.back, os.path.split(path)[0]]
        self.add_item(display, data, Var.back)


    def generate_name(self): 
        """ generate file name """ 
        elems = []
        text1 = self.get_elements(self.ui.e1_checkBox, self.ui.e1_lineEdit)
        text2 = self.get_elements(self.ui.e2_checkBox, self.ui.e2_lineEdit)
        text3 = self.get_elements(self.ui.e3_checkBox, self.ui.e3_lineEdit)
        text4 = self.get_custom(self.ui.custom1_checkBox, self.ui.customText1_lineEdit)
        versionText = self.get_custom(self.ui.version_checkBox, self.ui.version_lineEdit)
        text5 = self.get_custom(self.ui.custom2_checkBox, self.ui.customText2_lineEdit)
        format = str(self.ui.format_comboBox.currentText())

        if text1: 
            elems.append(text1)
        if text2: 
            elems.append(text2)
        if text3: 
            elems.append(text3)
        if text4: 
            elems.append(text4)
        if versionText: 
            elems.append(versionText)
        if text5: 
            elems.append(text5)

        if elems: 
            name = ('_').join(elems)
            nameExt = '%s.%s' % (name, format)
            self.ui.name_lineEdit.setText(nameExt)

        self.save_setting()


    def save_file(self): 
        """ save file """ 
        path = self.get_path()
        filename = str(self.ui.name_lineEdit.text())
        filePath = '%s/%s' % (path, filename)
        format = self.ui.format_comboBox.itemData(self.ui.format_comboBox.currentIndex(), QtCore.Qt.UserRole)
        utils.save_file(filePath, format)

        self.display_files()


    def open_file(self): 
        """ open file """
        item = self.ui.listWidget.currentItem()
        type, path = item.data(QtCore.Qt.UserRole)

        if type == Var.file: 
            if path and os.path.exists(path) and os.path.splitext(path)[-1][1:] in self.format: 
                return utils.open_file(path)


    def calculate_version(self, files): 
        """ calculate next version """
        prefix = versionConfig.get(Var.prefix, 'v')
        padding = versionConfig.get(Var.padding, 3)
        nextVersion = utils.calculate_version(files, prefix=prefix, padding=padding)
        self.ui.version_lineEdit.setText(nextVersion)
        self.generate_name()
        

    def get_elements(self, checkBox, lineEdit): 
        if checkBox.isChecked(): 
            index = lineEdit.text()
            if index: 
                text = self.get_path_elements(int(index))
                return text

    def get_custom(self, checkBox, lineEdit): 
        if checkBox.isChecked(): 
            text = str(lineEdit.text())
            return text


    def get_path_elements(self, index): 
        path = self.get_path()
        elems = path.split('/')

        if index > 0 and index < len(elems) or index < 0 and index*-1 < len(elems): 
            return elems[index]

    def get_path(self): 
        return str(self.ui.path_lineEdit.text()).replace('\\', '/')

    def navigate(self): 
        """ navigate folder """ 
        item = self.ui.listWidget.currentItem()
        type, path = item.data(QtCore.Qt.UserRole)

        if not type == Var.file: 
            self.browse(path)


    def add_cache(self, inputPath): 
        self.pathCaches = self.pathCaches[:self.cacheCount]
        self.pathCaches.append(inputPath)
        self.cacheCount = len(self.pathCaches)



    def navigate_back(self): 
        index = self.cacheCount - 1

        if index >= 1: 
            self.cacheCount = index
            self.browse_cache(self.pathCaches[index-1])

            self.ui.forward_pushButton.setEnabled(True)
            if index == 1: 
                self.ui.back_pushButton.setEnabled(False)


    def navigate_forward(self): 
        index = self.cacheCount + 1

        if index <= len(self.pathCaches):
            self.cacheCount = index
            self.browse_cache(self.pathCaches[index-1])

            self.ui.back_pushButton.setEnabled(True)
            if index == len(self.pathCaches): 
                self.ui.forward_pushButton.setEnabled(False)


def show():
    utils.deleteUI(uiName)
    myApp = SaveBackupPlus(utils.getMayaWindow())
    return myApp