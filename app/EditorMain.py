from PyQt5.QtGui import QFont,QFontDatabase
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtWidgets import QApplication, QFileDialog
from qfluentwidgets import FluentWindow, setTheme,Theme,StateToolTip,InfoBar,InfoBarPosition,NavigationItemPosition,SwitchButton
from qfluentwidgets import FluentIcon as FIF
import sys
from pathlib import Path
from EditorWidgets import EditInterface,DragDropWindow,DialogInterface, SettingsInterface
from jsonEditor import JSONHandler,UserSettings

current_path = Path(__file__)
parent_dir = str(current_path.parent.parent)


class Window(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.resize(1200,1000)

        self.save_path = ""
        self.file = None
        self.settings = UserSettings()
        self.selected_catalog = {}
        self.selected_item = {}
        self.input_fields = {}
        self.item_unsaved = False
        # self.auto_save_enabled = False
        # self.auto_save_time = 180000
        self.load_settings()

        self.homeInterface = DragDropWindow('Home Interface', parent_dir + '/UI/Home.ui',self)


        self.editInterface = EditInterface('Edit Interface',self)
        self.dialogInterface = DialogInterface('Dialog Interface', self)

        self.settingInterface = SettingsInterface('Setting Interface', self)


        self.homeInterface.fileDropped.connect(self.drop_file)
            
        self.initNavigation()
        self.initWindow()
        self.stackedWidget.currentChanged.connect(self.active_interface_change)
        self.active_interface = self.homeInterface
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_save)  

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.editInterface, FIF.EDIT, '默认编辑器')
        self.addSubInterface(self.dialogInterface, FIF.MESSAGE, '对话编辑器',NavigationItemPosition.SCROLL)
        self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', NavigationItemPosition.BOTTOM)
        self.interfaces = [self.homeInterface,self.editInterface,self.dialogInterface,self.settingInterface]
        

    def initWindow(self):
        self.setWindowTitle("json编辑器")
        self.resize(900, 700)
        # self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.stateTooltip = None

    def load_settings(self):
        self.auto_save_enabled = self.settings.get_setting('auto save')
        self.auto_save_time = self.settings.get_setting('auto save time')

    # region file
    def create_new_file(self):
        """新建空文件"""
        self.file = JSONHandler(path="NewJSON.json")
        self.load_file()
        return
    def create_new_dialog(self):
        """新建新对话文件"""
        self.file = JSONHandler(path="NewDialog.json")
        self.file.data = self.settings.data.get('new dialog')
        self.load_file()
        return
    def open_file(self):
        """从文件夹打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开json文件", "", "json文件 (*.json)")
        if file_path:
            self.file = JSONHandler(path=file_path)
            self.save_path = file_path
            self.load_file()   
    def drop_file(self,path):
        """拖放打开文件"""
        if path:
            self.file = JSONHandler(path=path)
            self.save_path = path
            self.load_file()
        else:
            print("未知路径："+path)
    def save_file(self):
        """存储文件到本地"""
        if self.file == None:
            return
        self.save_progress()
        # if self.editInterface.item_unsaved:
        #     self.editInterface.save_item()
        try:
            self.active_interface.save_all()
        except AttributeError:
            pass
        if self.save_path == "":
            file_path, _ = QFileDialog.getSaveFileName(self, "保存json文件", "", "json文件 (*.json)")
            if file_path:
                self.file.save_json(path=file_path)
                self.save_path = file_path
        else:
            self.file.save_json(path=self.save_path)
        self.settings.save_recent_path(self.save_path)
        self.homeInterface.initSubMenu()
        QTimer.singleShot(500, self.save_complete)
        if self.auto_save_enabled:
            self.timer.start(self.auto_save_time)  
        # asyncio.run(self.save_complete())
        # self.save_complete()
    def save_file_as(self):
        """文件另存为"""
        if self.file == None:
            return
        self.save_progress()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存json文件", "", "json文件 (*.json)")
        if file_path:
            self.file.save_json(path=file_path)
            self.save_path = file_path
        self.save_any_complete()
        self.settings.save_recent_path(self.save_path)
        self.homeInterface.initSubMenu()
        QTimer.singleShot(500, self.save_complete)
        if self.auto_save_enabled:
            self.timer.start(self.auto_save_time)  
    def load_file(self):
        """载入文件数据"""
        print("载入文件 "+self.save_path)
        if self.save_path:
            self.settings.save_recent_path(self.save_path)
            self.homeInterface.initSubMenu()

        if 'dialog' in self.file.data.keys():
            self.dialogInterface.file = self.file
            self.dialogInterface.load_file()
            self.switchTo(self.dialogInterface)
            self.editInterface.setEnabled(False)
        else:
            self.editInterface.file = self.file
            self.editInterface.load_file()
            self.switchTo(self.editInterface)
            self.dialogInterface.setEnabled(False)
        if self.auto_save_enabled:
            self.timer.start(self.auto_save_time)

    def save_backup(self):
        """恢复打开时的备份"""
        if self.file == None:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "保存json文件", "", "json文件 (*.json)")
        if file_path:
            if self.file.backup:
                self.file.save_backup(path=file_path)
                self.save_any_complete()
                self.settings.save_recent_path(self.save_path)
                self.homeInterface.initSubMenu()

    def auto_save(self):
        """自动保存"""
        if isinstance(self.active_interface, DragDropWindow) or self.file is not self.active_interface.file:
            QTimer.singleShot(60000, self.auto_save)
            return
        if self.save_path:
            self.save_file()
            return
        InfoBar.warning(
            title='文件未保存',
            content='请创建路径',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=-1,    
            parent=self
        )
    def enable_auto_save(self,enable):
        self.auto_save_enabled = enable
        self.settings.set_setting('auto save',enable)
        if self.auto_save_enabled:
            self.timer.start(self.auto_save_time)
            print('自动保存启用')
        else:
            if self.timer.isActive():
                self.timer.stop() 
    def change_save_time(self,t:int):
        self.auto_save_time = t*1000
        self.settings.set_setting('auto save time',self.auto_save_time)
    def save_progress(self):
        """存储进度条"""
        # if self.stateTooltip:
        #     self.stateTooltip.setState(False)
        # else:
        self.stateTooltip = StateToolTip('文件保存中', " ",self.active_interface)
        self.stateTooltip.move(self.active_interface.width()-150, 0)
        self.stateTooltip.show()
    def hide_progress(self):
        self.stateTooltip.hide()
        try:
            self.active_interface.file_saved()
        except AttributeError:
            pass
    def save_any_complete(self):
        InfoBar.success(
            title='',
            content="已保存",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
    def save_complete(self):
        self.stateTooltip.setContent('已保存')
        self.stateTooltip.setState(True)
        QTimer.singleShot(1000, self.hide_progress)
    # endregion
    
    def active_interface_change(self,index):
        """切换活跃界面"""
        self.active_interface = self.interfaces[index]

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    font_db = QFontDatabase()
    font_id = font_db.addApplicationFont(parent_dir + "/fonts/VonwaonBitmap-16px.ttf")
    font_family = font_db.applicationFontFamilies(font_id)[0]
    w = Window()
    w.show()
    app.exec()