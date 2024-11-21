from enum import Enum
from pathlib import Path
import re
import sys
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QSize,Qt,pyqtSignal,QCoreApplication
from PyQt5.QtWidgets import (QDialog,QGroupBox,QFrame,QVBoxLayout, QSizePolicy,QHBoxLayout,QWidget,
                             QStackedWidget,QApplication,QLabel)
from PyQt5.QtGui import QFont,QColor,QPalette
from qfluentwidgets import (LineEdit,Dialog,BodyLabel,ToolButton,Action, CommandBar,LineEditButton,
                            RoundMenu,MenuAnimationType,TransparentToolButton,InfoBadgePosition,
                            TextBrowser,InfoBadge,IconInfoBadge,InfoBar,InfoBarPosition,LineEditMenu,
                            ColorDialog,DropDownButtonBase,ToolTipFilter,ToolTipPosition, 
                            PlainTextEdit,TextEditMenu,DropDownPushButton,ScrollArea,Slider,
                            SettingCardGroup, SwitchSettingCard, SettingCard,ComboBox,
                            ExpandLayout)
from qfluentwidgets import FluentIcon as FIF
from jsonEditor import JSONHandler


current_path = Path(sys.argv[0]).resolve()
parent_dir = str(current_path.parent.parent)
placeholders = JSONHandler(str(current_path.parent)+'\\placeholders.json')


class Format(Enum):
    BOLD = (1,'b')
    ITALIC = (2,'i')
    UNDERLINE = (3,'u')
    STRIKE = (4,'strikethrough',)
    COLOR = (5,'color')
    LINEFEED = (6,'br')

    def __init__(self, value, tag):
        self._value = value
        self.tag = tag
class OptionAlign(Enum):
    Corrupt  = -2
    Selfish  = -1
    Neutral = 0
    Good = 1
    Virtuous = 2

    def __init__(self, value):
        self.color = {
            -2:"#FF0000",
            -1:"#db5123",
            0: "#FFFFFF", 
            1: "#b5bfff", 
            2: "#29ff50"}.get(value)
        self.title = {
            -2:"堕落",
            -1:"自私",
            0: "中立", 
            1: "善良", 
            2: "高尚"}.get(value)
class Comparison(Enum):
    EQUAL = 0
    GREATER = 1
    LESS = 2
    def __init__(self, value):
        self.text = {
            0: '等于', 
            1: '高于', 
            2: '低于'}.get(value)
class Stats(Enum):
    MRL = 0
    STR = 1
    DEX = 2
    DUR = 3
    INT = 4
    PCP = 5
    CHA = 6
    DEF = 7
    HP  = 8
    def __init__(self, value):
        self.text = {
            0:'道德倾向', 
            1:'力量', 
            2:'敏捷',
            3:'耐力',
            4:'智力',
            5:'感知',
            6:'魅力',
            7:'当前防御力',
            8:'当前生命值'
            }.get(value)

class OptionCondition:
    def __init__(self,data:str):
        # arg = list(map(lambda x: int(x), data[:3]))
        self.stats = Stats(int(data[0]))
        self.comp = Comparison(int(data[1]))
        try:
            self.val = int(data[2])
        except ValueError:
            self.val = int(data[2:])
    def to_text(self):
        return QCoreApplication.translate('Stats',self.stats.text)+' '+QCoreApplication.translate('Compare',self.comp.text)+' '+str(self.val)

    def __eq__(self,other):
        if isinstance(other, OptionCondition):
            return self.stats.value == other.stats.value
        return False
    
    def __hash__(self):
        return hash(self.stats.value)

    def __str__(self):
        return str(self.stats.value) + str(self.comp.value) + str(self.val)

class SafeDict(dict):
        def __missing__(self, key):
            return f"{{{key}}}" 
        
def tmp_to_html(tmp_text):
    html_text = re.sub(r'<strikethrough>', '<s>', tmp_text)  # 替换 <s> 为 <strike>
    html_text = re.sub(r'</strikethrough>', '</s>', html_text)  # 替换 </s> 为 </strike>
    html_text = replace_color_tags(html_text)
    return replace_placeholders(html_text)
def replace_color_tags(tmp_text):
    # 匹配 <color> 标签及其颜色值
    color_pattern = r'<color=([#a-fA-F0-9]+)>(.*?)</color>'
    # 替换为 <span> 标签，使用正则中的分组
    result_string = re.sub(color_pattern, r'<span style="color:\1;">\2</span>', tmp_text)
    # print (result_string)
    return result_string
def remove_tag_if_exists(text, tag):
    # 创建正则表达式，用于检测并匹配指定的标签
    pattern = rf"<{tag}[^>]*>(.*?)</{tag}>"
    
    # 检测是否包含指定标签
    if re.search(pattern, text):
        # 如果包含标签，移除标签
        cleaned_text = re.sub(pattern, r"\1", text)
        return cleaned_text, True
    else:
        # 如果不包含标签，返回原文本
        return text, False
def get_tag_color(tmp_text):
    pattern = r'<color=([#a-fA-F0-9]+)>'
    # 查找所有匹配项
    hex_colors = re.findall(pattern, tmp_text)
    # 加上 # 前缀使结果符合颜色代码格式
    # hex_colors = [color for color in hex_colors]
    return hex_colors
def add_tag_to(tmp_text,tag)->str:
    output,has_tag = remove_tag_if_exists(tmp_text,tag)
    if has_tag:
        return output
    return f"<{tag}>{output}</{tag}>"
def remove_all_tags(text):
    clean_text = re.sub(r'<[^>]+>', '', text)
    return replace_placeholders(clean_text)
def dialog_preview_text(name:str,content:str,name_align_right: bool = False):
        name_alignment = "right" if name_align_right else "left"
        return f"""
            <div style="width: 100%; padding: 10px; border: 2px solid #333; border-radius: 8px; background-color: #000000;text-align: {name_alignment};">
                <div style="font-weight: bold; margin-bottom: 8px; font-size: 15pt; ">{name}</div>
                <div style="margin-top: 8px; line-height: 1.5;;font-size: 12pt">
                    {content}
                </div>
            </div>
            """

def add_tag(selected_text, tag:Format)->str:
        """
        添加TMPro富文本标签
        """
        if not selected_text:
            return ''
        wrapped_text = ""
        wrapped_text = add_tag_to(selected_text,tag.tag)
        return wrapped_text

def add_color_tag(selected_text, color:str='#ffffff')->str:
        """
        添加TMPro颜色标签
        """
        if not selected_text:
            return ''
            
        wrapped_text = f"<color={color}>{selected_text}</color>"
        return wrapped_text

def all_conditions_to_text(all_conditions:list):
    out = ''
    if not all_conditions:
        return ''
    for conditions in all_conditions:
        out += condition_to_text(conditions)
        out+='\n'
    return out

def condition_to_text(conditions:str):
    out = ''
    if not conditions:
        return ''
    conds = conditions.split(',')
    i = 1
    for condition in conds:
        out += OptionCondition(condition).to_text()
        if i<len(conds):
            out+=' 且 '
        i+=1
    return out

def replace_placeholders(text, values=None):
    if values is None:
        global placeholders
        values = SafeDict(placeholders.data['placeholders']['names'])
    else:
        values = SafeDict(values)
        
    return text.format_map(values)

class ConfirmDialog(Dialog):
    def __init__(self,title,content):
        super().__init__(title=title,content=content)
        self.contentLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.contentLabel.setStyleSheet( " font-family: '微软雅黑'; font-size: 12pt; ")

class EditMenu:
    """ right click menu for text edition"""
    def __init__(self):
        self.textEdit = RoundMenu(QCoreApplication.translate("menu","文字"), self)
        self.textEdit.setIcon(FIF.EDIT)
        self.textEdit.addActions([
            Action(QCoreApplication.translate("menu","加粗"), self,triggered=lambda:self.add_tag_to(Format.BOLD) ),
            Action(QCoreApplication.translate("menu","斜体"), triggered=lambda:self.add_tag_to(Format.ITALIC) ),
            Action(QCoreApplication.translate("menu","下划线"), triggered=lambda:self.add_tag_to(Format.UNDERLINE)),
            Action(QCoreApplication.translate("menu","删除线"), triggered=lambda:self.add_tag_to(Format.STRIKE)),
            Action(QCoreApplication.translate("menu","颜色"), triggered=self.add_color_tag_to)
        ])

        self.insertText = RoundMenu(QCoreApplication.translate("menu","插入"),self)
        self.insertText.setIcon(FIF.CODE)

        self.insertTag = RoundMenu(QCoreApplication.translate("menu","排版"),self)
        self.insertTag.addActions([
            Action(QCoreApplication.translate("menu","换行"), triggered=lambda:self.insert_text_to("<br>") ),
        ])
        self.insertText.addMenu(self.insertTag)

        # self.settings = UserSettings()
        global placeholders

        self.insertName = RoundMenu(QCoreApplication.translate("menu","名字"),self)
        for n in placeholders.data["placeholders"]['names']:
            self.add_insert_action(self.insertName,'names',n)
        self.insertText.addMenu(self.insertName)

        self.insertNumber = RoundMenu(QCoreApplication.translate("menu","数值"),self)
        self.insertNumber.addActions([
            Action(QCoreApplication.translate("menu","等级"), triggered=lambda:self.insert_text_to("{"+"level"+"}") ),
            Action(QCoreApplication.translate("menu","伤害"), triggered=lambda:self.insert_text_to("{"+"damage"+"}") ),
            Action(QCoreApplication.translate("menu","生命值"), triggered=lambda:self.insert_text_to("{"+"hp"+"}"))
        ])
        self.insertText.addMenu(self.insertNumber)

        self.actions = [self.insertText]
        self.selected = ""
        self.start = 0

    def add_insert_action(self,menu:RoundMenu,catalog:str,key:str):
        replace = placeholders.data["placeholders"][catalog].get(key,'')
        if not replace:
            return
        menu.addAction(Action(replace, triggered=lambda:self.insert_text_to("{"+key+"}") ))

    def add_tag_to(self,tag:Format):
        wrapped_text = add_tag(self.selected,tag)
        start = self.start
        self.setText(self.text()[:start] + wrapped_text +self.text()[start+len(self.selected):])
        self.setCursorPosition(start + len(wrapped_text))
    
    def add_color_tag_to(self):
        colors = get_tag_color(self.selected)
        self.color = '#ffffff'
        if colors:
            self.color = colors[0]
        w = ColorDialog(QColor(self.color), QCoreApplication.translate("menu","选择字体颜色"), QApplication.instance().activeWindow(), enableAlpha=False)
        w.colorChanged.connect(self.choose_color)
        if w.exec_() == QDialog.Accepted:
            wrapped_text = add_color_tag(self.selected,self.color)
            start = self.start
            self.setText(self.text()[:start] + wrapped_text +self.text()[start+len(self.selected):])
            self.setCursorPosition(start + len(wrapped_text))

    def choose_color(self,color:QColor):
        self.color = color.name()
    
    def insert_text_to(self,key:str):
        current_text = self.text()           
        cursor_pos = self.cursorPosition()
        insert_text = key

        new_text = current_text[:cursor_pos] + insert_text + current_text[cursor_pos:]
        self.setText(new_text)
        self.setCursorPosition(cursor_pos + len(insert_text))

class EditorLineEdit(LineEdit,EditMenu):
    """line edit with edit menu"""
    textUpdated = pyqtSignal(str)
    unchanged = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.editingFinished.connect(self.edit)
        self.textChanged.connect(self.on_text_changed)
        self.previous_text = self.text()
        self.text_has_changed = False

    def setText(self,text:str):
        super().setText(text)
        self.previous_text = self.text()

    def edit(self):
        if self.text_has_changed:
            # print("item 已更改")
            self.textUpdated.emit(self.text())

    def on_text_changed(self, text):
        self.text_has_changed =  (text != self.previous_text)
        if self.text_has_changed:
            self.changed.emit()
        else:
            self.unchanged.emit()

    def contextMenuEvent(self, event):
        menu = RoundMenu(self)
        default_menu = LineEditMenu(self)
        default_menu._title = QCoreApplication.translate('menu','编辑')
        default_menu.setIcon(FIF.PASTE)
        menu.addMenu(default_menu)
        menu.addSeparator() 
        if self.hasSelectedText():
            self.selected = self.selectedText()
            self.start = self.selectionStart()
            menu.addMenu(self.textEdit)
        for m in self.actions:
            menu.addMenu(m)

        # 显示菜单
        menu.exec_(event.globalPos())

class EditorPlainTextEdit(PlainTextEdit,EditMenu):
    """plain text edit with edit menu"""
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):

        menu = RoundMenu(self)
        default_menu = TextEditMenu(self)
        default_menu._title = QCoreApplication.translate('menu','编辑')
        default_menu.setIcon(FIF.PASTE)
        menu.addMenu(default_menu)
        menu.addSeparator() 
        if self.hasSelectedText():
            self.selected = self.selectedText()
            self.start = self.selectionStart()
            menu.addMenu(self.textEdit)
        for m in self.actions:
            menu.addMenu(m)

        # 显示菜单
        menu.exec_(event.globalPos())

    def selectedText(self)->str:
        cursor = self.textCursor()
        return cursor.selectedText()
    def selectionStart(self):
        return self.textCursor().selectionStart()
    def hasSelectedText(self)->bool:
        if self.selectedText():
            return True  
    def text(self)->str:
        return self.toPlainText()
    def setText(self,text:str):
        self.setPlainText(text)
    def setCursorPosition(self,pos:int):
        self.textCursor().setPosition(pos)
    def cursorPosition(self)->int:
        return self.textCursor().position()

class DropDownLineEditButton(DropDownButtonBase,LineEditButton):
    """ button in line edit with drop down menu """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isPressed = False
        self.isHover = False

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def mouseReleaseEvent(self, e):
        LineEditButton.mouseReleaseEvent(self, e)
        self._showMenu()

    def paintEvent(self, e):
        # if self.icon:
        #     LineEditButton.paintEvent(self, e)
        DropDownButtonBase.paintEvent(self, e)

    def _drawDropDownIcon(self, painter, rect):
        if True:
            FIF.ADD.render(painter, rect)
        else:
            FIF.ARROW_DOWN.render(painter, rect, fill="#646464")

class MultiFuncButton(DropDownLineEditButton):
    """button with drop down menu"""
    action_clicked = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMenu(RoundMenu(self))
        self.action_slots = []
        self.addActions([
            Action(FIF.CODE,'空' ),
            Action(FIF.COPY,'当前模板' ),
            # Action(FIF.ADD, self.tr("其他"))
        ])

    def addActions(self,actions:list[Action]):
        [self.addAction(action) for action in actions]

    def addAction(self,action:Action):
        index = len(self.action_slots)
        action.triggered.connect(lambda :self.action_triggered(index))
        # print(index)
        self.action_slots.append(action.text())
        action.setText(QCoreApplication.translate('Form',action.text()))
        self.menu().addAction(action)
    
    def clear(self):
        self.menu().clear()
        self.action_slots = []

    def action_triggered(self,action_slot:int):
        try:
            self.setText(self.action_slots[action_slot])
            self.action_clicked.emit(self.text())
            # print(self.text())
        except TypeError:
            print(f'槽{str(action_slot)}不存在')
            return

class ButtonLineEdit(EditorLineEdit):
    """  Line edit with a button"""

    clicked = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.toolButton = LineEditButton(self)
        self.toolButton.setIcon(FIF.ADD)

        self.hBoxLayout.addWidget(self.toolButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.toolButton.clicked.connect(self.click)
        self.clearButton.clicked.connect(self.clearSignal)
    

    def click(self):
        """ emit search signal """
        text = self.text().strip()
        if text:
            self.clicked.emit(text)
        else:
            self.clearSignal.emit()

    def setClearButtonEnabled(self, enable: bool = True):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28*enable+30, 0)

class DropDownLineEdit(EditorLineEdit):
    """  Line edit with a button"""

    clicked = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.toolButton = MultiFuncButton(self)

        self.hBoxLayout.addWidget(self.toolButton, 0, Qt.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.toolButton.action_clicked.connect(self.action_click)
        self.clearButton.clicked.connect(self.clearSignal)
    

    def action_click(self,action:str):
        text = self.text().strip()
        if text:
            self.clicked.emit(action)
        else:
            self.clearSignal.emit()

    def setClearButtonEnabled(self, enable: bool = True):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28*enable+30, 0)

class StackedLineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QHBoxLayout())
        label_container = QGroupBox(self)
        label_layout = QHBoxLayout(label_container)
        label_layout.setContentsMargins(0,0,0,0)
        self.stacked_widget = QStackedWidget(self)
        # self.settings = UserSettings()
        # global placeholders
        

        self.line_edit = ButtonLineEdit(parent)
        self.line_edit.setFont(QFont("VonwaonBitmap 16px", 12))
        

        self.label = TextBrowser(label_container)
        self.label.setAlignment(Qt.AlignCenter)
        
        label_layout.addWidget(self.label)
        self.stacked_widget.addWidget(self.line_edit)
        self.stacked_widget.addWidget(label_container)
        
        # Add the stacked widget to the layout
        self.layout().addWidget(self.stacked_widget)
        
        # Create the button to switch between the two views
        self.view_button = self.line_edit.toolButton
        self.view_button.setIcon(FIF.VIEW)

        self.edit_button = TransparentToolButton(FIF.EDIT,label_container)
        label_layout.addChildWidget(QGroupBox(label_container))
        label_layout.addWidget(self.edit_button, 0, Qt.AlignRight)
        # self.edit_button.setIconSize((QSize(10,10)))
        self.view_button.setIconSize((QSize(20,20)))
        self.edit_button.setMinimumSize(QtCore.QSize(20, 50))
        self.edit_button.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setMinimumSize(QtCore.QSize(100, 50))
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        self.view_button.setMinimumSize(QtCore.QSize(20, 50))
        self.view_button.setMaximumSize(QtCore.QSize(50, 50))
        self.line_edit.setMinimumSize(QtCore.QSize(100, 50))
        self.line_edit.setMaximumSize(QtCore.QSize(16777215, 50))
        
        
        # Connect the button to the toggle function
        self.view_button.clicked.connect(self.toggle_view)
        self.edit_button.clicked.connect(self.toggle_view)

    def toggle_view(self):
        current_index = self.stacked_widget.currentIndex()
        new_index = 1 - current_index
        self.stacked_widget.setCurrentIndex(new_index)
        # self.label.setPlainText(self.line_edit.text())
        self.label.setHtml(f"""
            <div style="font-family: 'VonwaonBitmap 16px'; font-size: 15pt; text-align:center;">
                {tmp_to_html(replace_placeholders(self.line_edit.text()))}
            </div>
        """)
    def setText(self, text:str):
        self.line_edit.setText(text)
        self.toggle_view()
        self.toggle_view()
    def setAlignment(self,alignment):
        self.line_edit.setAlignment(alignment)
        self.label.setAlignment(alignment)
    def setClearButtonEnabled(self,enable):
        self.line_edit.setClearButtonEnabled(enable)

class FormLineEdit(QGroupBox):

    clicked = pyqtSignal()
    editingFinished = pyqtSignal(str,str)
    unchanged = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, parent=None, key="",value=""):
        super().__init__(parent)
        
        self.key = key
        self.setStyleSheet("QGroupBox { border: none; }")
        self.container_form = QGroupBox()
        container_form_layout = QHBoxLayout(self.container_form)
        self.stack_input = StackedLineEdit(self.container_form)
        self.input_field = self.stack_input.line_edit
        self.input_field.setClearButtonEnabled(True)
        self.input_field.setText(str(value))
        self.previous_text = str(value)
        self.stack_input.toggle_view()
        self.text_has_changed = False

        self.stack_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # self.stack_input.setMinimumSize(QtCore.QSize(100, 50))
        # self.stack_input.setMaximumSize(QtCore.QSize(16777215, 70))
        self.input_field.editingFinished.connect(self.edit)
        self.input_field.textChanged.connect(self.on_text_changed)
        container_form_layout.addWidget(self.stack_input)

        self.container = QGroupBox()
        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(0,0,0,0)
        container_layout =QHBoxLayout()
        container_layout.setContentsMargins(0,0,0,0)
        self.container.setMinimumSize(QtCore.QSize(100, 50))

        # hline = QFrame(self.container)
        # hline.setFrameShape(QFrame.HLine)
        # hline.setFrameShadow(QFrame.Sunken)
        
        remove_button = ToolButton(FIF.DELETE,parent=self.container)
        remove_button.setMinimumSize(QtCore.QSize(10, 0))
        remove_button.setMaximumSize(QtCore.QSize(60, 16777215))
        # remove_button.setIconSize((QSize(10,10)))
        remove_button.clicked.connect(self.click)

        label = BodyLabel(self.container)
        label.setMinimumSize(QtCore.QSize(50, 0))
        label.setText(key)
        container_layout.addWidget(remove_button)
        container_layout.addWidget(label)
        main_layout.addLayout(container_layout)
        # main_layout.addWidget(hline)

    def click(self):
        self.clicked.emit()
    def edit(self):
        if self.text_has_changed:
            # print("item 已更改")
            self.editingFinished.emit(self.key, self.input_field.text())
    def on_text_changed(self, text):
        self.text_has_changed =  (text != self.previous_text)
        if self.text_has_changed:
            self.changed.emit()
        else:
            self.unchanged.emit()
            
class DragDropWindow(QFrame):

    fileDropped = pyqtSignal(str)

    def __init__(self, text:str, file:str,parent:QWidget):
        super().__init__(parent=parent)
        uic.loadUi(file, self)
        self.setObjectName(text.replace(' ', '-'))
        # self.newButton.clicked.connect(parent.create_new_file)
        self.newButton.setIcon(FIF.ADD.icon())
        menu = RoundMenu()
        self.newButton.setMenu(menu)
        menu.addActions([
            Action(FIF.EDIT,QCoreApplication.translate('Form','新建空文件'),triggered=parent.create_new_file),
            Action(FIF.MESSAGE,QCoreApplication.translate('Form','新建空对话文件'),triggered=parent.create_new_dialog)
        ])

        self.recent = parent.settings.data["recent"]
        # 打开
        self.openButton.clicked.connect(parent.open_file)
        self.openButton.setIcon(FIF.FOLDER.icon())

        self.setAcceptDrops(True)

        self.menu = RoundMenu(parent=self)

        self.submenu = RoundMenu(QCoreApplication.translate('Form',"打开近期"), self)
        self.submenu.setIcon(FIF.FOLDER_ADD)
        self.initSubMenu()
        self.menu.addMenu(self.submenu)

        # add actions
        # self.menu.addActions([
        #     Action(FIF.PASTE, 'Paste'),
        #     Action(FIF.CANCEL, 'Undo')
        # ])

        # add separator
        self.menu.addSeparator()
        
    def initSubMenu(self):
        self.submenu.clear()
        action0 = Action(FIF.FOLDER, self.recent["path0"], triggered=lambda :self.dropFile("path0") )
        action1 = Action(FIF.FOLDER, self.recent["path1"], triggered=lambda :self.dropFile("path1") )
        action2 = Action(FIF.FOLDER, self.recent["path2"], triggered=lambda :self.dropFile("path2") )
        action3 = Action(FIF.FOLDER, self.recent["path3"], triggered=lambda :self.dropFile("path3") )
        action4 = Action(FIF.FOLDER, self.recent["path4"], triggered=lambda :self.dropFile("path4") )
        recentFilesActions = [action0,action1,action2,action3,action4]
        for key,path in self.recent.items():
            if path:
                index = int(re.findall(r'\d+', key)[0])
                self.submenu.addAction(recentFilesActions[index])
    
    def contextMenuEvent(self, e):
        # show menu
        self.menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

    def dropFile(self, key:str):
        # print(key)
        self.fileDropped.emit(self.recent[key])

    def dragEnterEvent(self, event):
        # 检查拖拽的数据是否包含文件（使用 MIME 类型）
        if event.mimeData().hasUrls():
            event.accept()  # 接受拖拽事件
        else:
            event.ignore()  # 忽略其他类型的拖拽
    # 当放下拖拽文件时触发
    def dropEvent(self, event):
        # 获取拖拽的文件路径
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            self.fileDropped.emit(files[0])

class BadgeButton(QWidget):
    """button with badge"""
    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.vBoxLayout = QVBoxLayout(self)


        # Using an InfoBadge in another control
        self.button = ToolButton(FIF.BASKETBALL, self)
        self.vBoxLayout.addWidget(self.button, 0, Qt.AlignHCenter)
        self.badge = InfoBadge.success(1, self, target=self.button, position=InfoBadgePosition.TOP_RIGHT)
        # self.button.clicked.connect(self.badge.hide)

class OptionRow(QGroupBox):

    clicked = pyqtSignal(str)

    def __init__(self, parent=None, content='',tooltip=''):
        super().__init__(parent)
        
        self.key = content
        self.setStyleSheet("QGroupBox { border: none; }")

        self.container_form = QGroupBox()
        container_form_layout = QHBoxLayout(self.container_form)

        self.label = DropDownPushButton(self.container_form)
        self.label.setFont(QFont("VonwaonBitmap 16px",10))
        self.label.setText(str(content))
        self.label.setToolTip(tooltip)
        self.label.installEventFilter(ToolTipFilter(self.label, showDelay=30, position=ToolTipPosition.TOP))
        container_form_layout.addWidget(self.label)
        self.label.setMenu(RoundMenu())
        self.label.menu().addActions([
                    Action(FIF.DELETE,QCoreApplication.translate('Form','移除'),triggered=lambda:parent.remove_option_from_dialog(content)),
                    Action(FIF.RIGHT_ARROW,QCoreApplication.translate('Form','转到'),triggered=lambda:parent.optionComboBox.setCurrentText(content))
        ])


        self.container = QGroupBox()
        container_layout =QHBoxLayout(self.container)

    def click(self):
        self.clicked.emit(self.key)

class ConditionBox(QFrame):
    def __init__(self, parent=None,data:str=''):
        super().__init__(parent=parent)
        # self.setupUi(self)
        # 加载对话框界面文件
        uic.loadUi(parent_dir + "/UI/ConditionBox.ui", self)
        self.addCondition.setIcon(FIF.ADD)
        if data:
            self.data = data.split(',')
        else:
            self.data = []

        for stat in Stats:
            self.conditionStats.addItem(QCoreApplication.translate("Stats",stat.text))
        for comp in Comparison:
            self.conditionCompare.addItem(QCoreApplication.translate("Compare",comp.text))
        

        self.conditionStats.currentIndexChanged.connect(self.change_spinbox_range)
        self.addCondition.clicked.connect(self.add_AND_condition)

        if self.data:
            self.load_conditions()
    
    def change_spinbox_range(self,index):
        if index==0:
            # self.conditionValue = SpinBox()
            self.conditionValue.setMaximum(2)
            return
        self.conditionValue.setMaximum(99)

    def load_conditions(self):
        
        self.conditionForm.layout().removeWidget(self.groupBox)
        for i in reversed(range(self.conditionForm.layout().count())): 
            widget = self.conditionForm.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.conditionForm.layout().addRow(self.groupBox)
        if not self.data:
            return
        for data in self.data:

            self.create_AND_condition(OptionCondition(data))

    def add_AND_condition(self):
        stats = self.conditionStats.currentIndex()
        comp = self.conditionCompare.currentIndex()
        val = self.conditionValue.value()
        data = OptionCondition(str(stats)+str(comp)+str(val))

        for d in self.data:
            if int(d[0])==stats:
                print('条件或相似条件已存在')
                return

        self.data.append(str(data))
        self.create_AND_condition(data)

    def create_AND_condition(self,data:OptionCondition):
        content = str(data)
        cond_label = DropDownPushButton(self)
        cond_label.setFont(QFont("VonwaonBitmap 16px",10))
        cond_label.setText(data.to_text()+' '+QCoreApplication.translate('Form','且'))
        cond_label.installEventFilter(ToolTipFilter(cond_label, showDelay=30, position=ToolTipPosition.TOP))
        cond_label.setMenu(RoundMenu())
        cond_label.menu().addAction(Action(FIF.DELETE,QCoreApplication.translate('Form','移除'),triggered=lambda:self.remove_AND_condition(content)))
        self.conditionForm.layout().removeWidget(self.groupBox)
        self.conditionForm.layout().addRow(cond_label)
        self.conditionForm.layout().addRow(self.groupBox)

    def remove_AND_condition(self,content):
        try:
            self.data.remove(content)
            print('移除条件'+OptionCondition(content).to_text())
        except ValueError:
            print('错误：条件不存在')
            return
        self.load_conditions()

class RangeSettingCard(SettingCard):
    """ Setting card with a slider """

    valueChanged = pyqtSignal(int)

    def __init__(self, icon:  FIF, title, content=None, parent=None):
        """
        Parameters
        ----------

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.slider = Slider(Qt.Horizontal, self)
        self.valueLabel = QLabel(self)
        self.slider.setMinimumWidth(268)

        self.slider.setSingleStep(1)
        # self.slider.setRange(*configItem.range)
        # self.slider.setValue(configItem.value)
        # self.valueLabel.setNum(configItem.value)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(6)
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.valueLabel.setObjectName('valueLabel')
        # configItem.valueChanged.connect(self.setValue)
        self.slider.valueChanged.connect(self.__onValueChanged)

    def __onValueChanged(self, value: int):
        """ slider value changed slot """
        self.setValue(value)
        self.valueChanged.emit(value)

    def setValue(self, value):
        # qconfig.set(self.configItem, value)
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.slider.setValue(value)
class ComboBoxSettingCard(SettingCard):
    """ Setting card with a combo box """

    def __init__(self,  icon: FIF, title, content=None, texts=None, parent=None):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        texts: List[str]
            the text of items

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        # self.optionToText = {o: t for o, t in zip(configItem.options, texts)}
        for text in texts:
            self.comboBox.addItem(text)

        # self.comboBox.setCurrentText(self.optionToText[qconfig.get(configItem)])
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)
        # configItem.valueChanged.connect(self.setValue)

    def _onCurrentIndexChanged(self, index: int):
        pass
        # qconfig.set(self.configItem, self.comboBox.itemData(index))

    def setValue(self, value):
        if value not in self.optionToText:
            return

        self.comboBox.setCurrentText(self.optionToText[value])
        # qconfig.set(self.configItem, value)


class EditInterface(QFrame):

    def __init__(self, text: str,parent:QWidget):
        super().__init__(parent=parent)
        self.setObjectName(text.replace(' ', '-'))
        # self.setupUi(self)
        # 加载对话框界面文件
        uic.loadUi(parent_dir + "/UI/EditInterface.ui", self)
        self.setWindowTitle("Editor")
        self.setEnabled(False)
        self.save_path = ""
        self.file = None
        # self.settings = UserSettings()
        self.settings = parent.settings
        self.resize(1000, 1000)
        self.selected_catalog = {}
        self.input_fields = {}
        self.item_unsaved = False
        self.chosen_color = '#ffffff'
        # setTheme(Theme.DARK)

        
        
        self.setStyleSheet("BodyLabel, ComboBox, QLineEdit { font-family: 'Consolas'; font-size: 12pt; }")
        self.menu = QHBoxLayout(self.groupBox)
        commandBar = CommandBar(self.groupBox)
        self.save_action = Action(FIF.SAVE, QCoreApplication.translate('Form','保存'), triggered=parent.save_file,shortcut='Ctrl+S')
        commandBar.addActions([
            Action(FIF.FOLDER, QCoreApplication.translate('Form','打开'), triggered=parent.open_file,shortcut='Ctrl+O'),
            self.save_action
            ])
        self.menu.addWidget(commandBar)
    

        # 添加始终隐藏的动作
        commandBar.addHiddenActions([
            Action(FIF.ADD, QCoreApplication.translate('Form','新建'), triggered=parent.create_new_file,shortcut='Ctrl+N'),
            Action(FIF.SAVE_AS, QCoreApplication.translate('Form','另存为'), triggered=parent.save_file_as,shortcut='Ctrl+Shift+S'),
            Action(FIF.COPY, QCoreApplication.translate('Form','保存启动备份'), triggered=parent.save_backup)
            ])


        # region Initialization
        self.itemComboBox.currentIndexChanged.connect(self.change_item)
        self.itemLineEdit.clicked.connect(self.create_item)
        self.catalogComboBox.currentIndexChanged.connect(self.change_catalog)
        self.catalogLineEdit.clicked.connect(self.create_catalog)

        self.saveItemButton.clicked.connect(self.save_item)
        self.saveItemButton.clicked.connect(parent.save_any_complete)
        self.saveItemButton.setIcon(FIF.SAVE.icon())
        self.badge = IconInfoBadge.attension(FIF.SYNC, self.saveBox, target=self.saveItemButton, position=InfoBadgePosition.TOP_RIGHT)
        self.badge.hide()

        self.resetItemButton.clicked.connect(self.reset_item)
        self.resetItemButton.setIcon(FIF.SYNC.icon())
        self.nextItemButton.clicked.connect(self.next_item)
        self.nextItemButton.setIcon(FIF.CARE_DOWN_SOLID.icon())
        self.lastItemButton.clicked.connect(self.last_item)
        self.lastItemButton.setIcon(FIF.CARE_UP_SOLID.icon())
        self.removeItemButton.clicked.connect(self.remove_item)
        self.removeItemButton.setIcon(FIF.DELETE.icon())

        self.removeCatalogButton.clicked.connect(self.remove_catalog)
        self.removeCatalogButton.setIcon(FIF.DELETE.icon())
        

        self.scrollArea.enableTransparentBackground()
        self.save_action.triggered.connect(self.change_item)
        self.currentInfoBar = None

        # endregion
    
    # region Save InfoBar
    def file_unsaved(self):
        if self.has_same_infoBar(QCoreApplication.translate('Form','更改未保存')):
            return
        self.currentInfoBar = InfoBar.info(
            title=QCoreApplication.translate('Form','更改未保存'),
            content=self.file.path,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,    
            parent=self
        )
        self.currentInfoBar.setFont(QFont("VonwaonBitmap 16px",12))
    def file_saved(self):
        if self.has_same_infoBar(QCoreApplication.translate('Form','已是最新')):
            return
        self.currentInfoBar = InfoBar.success(
            title=QCoreApplication.translate('Form','已是最新'),
            content=self.file.path,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,    
            parent=self
        )
    def has_same_infoBar(self,key)->bool:
        if self.currentInfoBar:
            try:
                if key == self.currentInfoBar.title:
                    return True
                self.currentInfoBar.close()
            except RuntimeError:
                pass
            return False
    # endregion

    # region file
    def load_file(self):
        """加载文件到显示区"""
        data = self.file.data
        # self.file_info.content = self.file.path
        self.file_saved()
        # self.currentInfoBar.duration = 1000
        # self.menu.addWidget()
        self.connect_combo_box(False)
        self.catalogComboBox.clear()
        self.catalogComboBox.addItems(data.keys())
        self.connect_combo_box(True)
        self.change_catalog()
        self.setEnabled(True)
    def save_all(self):
        self.save_item()
    # endregion

    # region catalog
    def connect_combo_box(self, connect):
        """连接/断开下拉菜单"""
        if connect:
            self.itemComboBox.currentIndexChanged.connect(self.change_item)
            self.catalogComboBox.currentIndexChanged.connect(self.change_catalog)
        else:
            self.itemComboBox.currentIndexChanged.disconnect(self.change_item)
            self.catalogComboBox.currentIndexChanged.disconnect(self.change_catalog)
    def change_catalog(self):
        """切换分类"""
        self.catalogComboBox.setToolTip(self.catalogComboBox.currentText())
        self.catalogLineEdit.setText("")
        self.connect_combo_box(False)
        try:
            self.selected_catalog = self.file.data[self.catalogComboBox.currentText()]
            self.itemComboBox.clear()
            self.itemComboBox.addItems(self.selected_catalog.keys())
            self.itemComboBox.setToolTip(self.itemComboBox.currentText())
        except KeyError:
            pass
        self.connect_combo_box(True)
        self.change_item()
    def create_catalog(self,action:str):
        """新建分类"""
        new_catalog_name = self.catalogLineEdit.text()
        

        if new_catalog_name =="":
            ConfirmDialog(content=QCoreApplication.translate('Form',"无法创建未命名的分类"),title="Warning").exec_()
            return
        elif new_catalog_name in self.selected_catalog.keys():
            ConfirmDialog(content=QCoreApplication.translate('Form',"已存在同名分类"),title="Warning").exec_()
            return
        self.save_item_confirm()

        match action:
            case '空':
                default = {'new item':{'new key':'none'}}
            case '当前模板':
                # item_name = self.itemComboBox.currentText()
                default = self.selected_catalog.copy()
            case _ :
                return

        self.file.set_catalog(new_catalog_name,default)
        self.catalogComboBox.addItem(new_catalog_name)
        # self.selected_catalog = self.file.data[new_catalog_name]
        self.catalogComboBox.setCurrentIndex(self.catalogComboBox.count() - 1)
        self.file_unsaved()
    def remove_catalog(self):
        """移除当前显示中的分类"""
        confirm = ConfirmDialog("",QCoreApplication.translate('Form',"确认删除当前分类吗"))
        if confirm.exec_() == QDialog.Accepted:
            self.file.data.pop(self.catalogComboBox.currentText())
            self.catalogComboBox.removeItem(self.catalogComboBox.currentIndex())
            self.file_unsaved()
    # endregion
    # region key
    def change_item(self):
        """切换item"""
        self.itemLineEdit.setText("")
        item_name = self.itemComboBox.currentText()
        try:
            self.input_fields = self.selected_catalog[item_name].copy()
            print(f"显示项 {item_name}")
        except KeyError:
            print(f"错误: 项 {item_name} 不存在")
            return
        except AttributeError:
            print(f"错误:  {item_name} 结构错误")
            return
        self.create_input_form()
        self.item_unsaved = False
    def create_input_form(self):
        """创建输入区域"""
        for i in reversed(range(self.editFormLayout.layout().count())): 
            widget = self.editFormLayout.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.badge.hide()
        item_name = self.itemComboBox.currentText()
        if item_name in self.selected_catalog.keys():
            item_data = self.input_fields

            for key, value in item_data.items():
                row = FormLineEdit(self,key,value)
                # row.input_field.installEventFilter(self)
                # print("创建"+key)
                row.editingFinished.connect(self.set_value)
                row.clicked.connect(lambda key=key,:self.remove_key(key=key))
                row.unchanged.connect(self.badge.hide)
                row.changed.connect(self.badge.show)

                hline = QFrame(self)
                hline.setFrameShape(QFrame.HLine)
                hline.setFrameShadow(QFrame.Sunken)
            
                # 将标签和输入框添加到布局中
                self.editFormLayout.layout().addRow(row.container, row.container_form)
                self.editFormLayout.layout().addRow(hline)

            container2 = QGroupBox()
            container_layout2 =QHBoxLayout(container2)
            container2.setMinimumSize(QtCore.QSize(100, 50))
            container_form2 = QGroupBox()

            text = DropDownLineEdit(container_form2)
            text.toolButton.clear()
            text.toolButton.addActions([
                Action(FIF.ADD,"添加" ),
                Action(FIF.PASTE, "添加至全部" ),
            ])
            self.keyLineEdit = text
            text.clicked.connect(self.create_key)
            container_layout2.addWidget(text)
            self.editFormLayout.layout().addRow(container2,container_form2)
            self.editFormLayout.layout().setSpacing(0)  # 控件之间的间距
            self.editFormLayout.layout().setContentsMargins(0, 0, 0, 0)

        else:
            print(f"error: {item_name} not in field")
    def set_value(self,key,value):
        """设置值"""
        self.input_fields[key]=value
        # self.badge.show()
        self.item_unsaved = True
        self.file_unsaved()
        print(key+" 值更新为 "+value )
    def set_key(self,key,new_key,value):
        """设置键"""
        self.input_fields.pop(key)
        self.input_fields[new_key]=value
    def create_key(self,action:str):

        new_key = self.keyLineEdit.text()
        if new_key =="":
                ConfirmDialog(content=QCoreApplication.translate('Form',"无法创建未命名的键"),title="Warning").exec_()
                return
        elif new_key in self.selected_catalog.keys():
            ConfirmDialog(content=QCoreApplication.translate('Form',"已存在同名键"),title="Warning").exec_()
            return
        
        match action:
            case '添加':
                self.input_fields[new_key]='none'
                self.item_unsaved = True
                self.badge.show()
            case '添加至全部':
                self.save_item_confirm()
                for item in self.selected_catalog:
                    self.selected_catalog[item][new_key]='none'
                self.change_item()
                self.file_unsaved()
                return
            case _ :
                return

        self.create_input_form()
        self.file_unsaved()     
    def remove_key(self,key):
        """移除选中的键值对"""
        confirm = ConfirmDialog("",QCoreApplication.translate('Form',"确认删除当前键吗"))
        if confirm.exec_() == QDialog.Accepted:
            self.input_fields.pop(key)
            self.create_input_form()
            self.item_unsaved = True
            self.badge.show()
            self.file_unsaved()
    # endregion
    # region Item
    def save_item(self):
        """更新当前item的编辑到缓存，不保存到文件"""
        # catalog_name = self.catalogComboBox.currentText()
        item_name = self.itemComboBox.currentText()
        self.selected_catalog[item_name] = self.input_fields.copy()
        self.item_unsaved = False
        self.badge.hide()
        # for key in self.input_fields.keys():
        #     self.file.set_value(catalog_name,item_name,key,self.input_fields[key])
    def reset_item(self):
        """将对当前item的编辑重置为缓存状态"""
        confirm = ConfirmDialog("",QCoreApplication.translate('Form',"确认重置当前项吗"))
        if confirm.exec_() == QDialog.Accepted:
            self.change_item()
            self.item_unsaved = False
            self.badge.hide()
    def create_item(self,action:str):

        new_item_name = self.itemLineEdit.text()
        default = {}

        if new_item_name =="":
            ConfirmDialog(content=QCoreApplication.translate('Form',"无法创建未命名的键"),title="Warning").exec_()
            return
        elif new_item_name in self.selected_catalog.keys():
            ConfirmDialog(content=QCoreApplication.translate('Form',"已存在同名键"),title="Warning").exec_()
            return
        self.save_item_confirm()

        match action:
            case '空':
                pass
            case '当前模板':
                item_name = self.itemComboBox.currentText()
                for key in self.selected_catalog[item_name]:
                    default[key] = "none"
            case _ :
                return

        self.file_unsaved()
        self.selected_catalog[new_item_name]=default
        self.itemComboBox.addItem(new_item_name)
        self.itemComboBox.setCurrentIndex(self.itemComboBox.count() - 1)
    def next_item(self):
        """切换显示到下一个item"""
        if self.itemComboBox.currentIndex()==self.itemComboBox.count()-1:
            return
        self.save_item_confirm()
        index = min(self.itemComboBox.currentIndex()+1,self.itemComboBox.count()-1)
        self.itemComboBox.setCurrentIndex(index)
    def last_item(self):
        """切换显示为上一个item"""
        if self.itemComboBox.currentIndex() == 0:
            return
        self.save_item_confirm()
        index = max(self.itemComboBox.currentIndex()-1,0)
        self.itemComboBox.setCurrentIndex(index)
    def remove_item(self):
        """移除当前活跃的item"""
        confirm = ConfirmDialog("",QCoreApplication.translate('Form',"确认删除当前项吗"))
        if confirm.exec_() == QDialog.Accepted:
            # item_to_remove = self.selected_catalog[self.itemComboBox.currentText()]
            self.selected_catalog.pop(self.itemComboBox.currentText())
            self.itemComboBox.removeItem(self.itemComboBox.currentIndex())
            self.file_unsaved()
    def save_item_confirm(self):
        if self.item_unsaved:
            confirm = ConfirmDialog("",QCoreApplication.translate('Form',"要保存当前项吗"))
            if confirm.exec_() == QDialog.Accepted:
                self.save_item()
    # endregion

class DialogInterface(QFrame):
    def __init__(self,text:str,parent:QWidget):
        super().__init__(parent=parent)
        uic.loadUi(parent_dir + "/UI/DialogInterface.ui", self)
        self.setObjectName(text.replace(' ', '-'))
        self.setEnabled(False)
        # variable init
        self.file:JSONHandler = None
        self.dialog:dict = None
        self.dialogID = '0'
        self.option:dict = None
        self.dialog_unsaved = False
        self.option_unsaved = False
        self.currentInfoBar:InfoBar = None
        self.settings = parent.settings
        self.previous_text = ''

        self.__initConditionButton()

        # style
        self.scrollArea.enableTransparentBackground()
        self.scrollArea_2.enableTransparentBackground()
        self.setStyleSheet("QGroupBox { border: 0px; }")

        # command bar
        self.menu = self.menuBox.layout()
        commandBar = CommandBar(self.menuBox)
        self.save_action = Action(FIF.SAVE, QCoreApplication.translate('Form','保存'), triggered=parent.save_file,shortcut='Ctrl+S')
        commandBar.addActions([
            Action(FIF.FOLDER, QCoreApplication.translate('Form','打开'), triggered=parent.open_file,shortcut='Ctrl+O'),
            self.save_action
            ])
        self.menu.addWidget(commandBar)

        commandBar.addHiddenActions([
            Action(FIF.ADD, QCoreApplication.translate('Form','新建'), triggered=parent.create_new_file,shortcut='Ctrl+N'),
            Action(FIF.SAVE_AS, QCoreApplication.translate('Form','另存为'), triggered=parent.save_file_as,shortcut='Ctrl+Shift+S'),
            Action(FIF.RETURN, QCoreApplication.translate('Form','保存启动备份'), triggered=parent.save_backup)
            ])
        
        
        
        # buttons
        self.__connect_combobox(True)
        self.clearDialogButton.setIcon(FIF.CLOSE.icon())
        self.clearDialogButton.clicked.connect(self.__clear_dialog)

        self.clearOptionButton.setIcon(FIF.CLOSE.icon())
        self.clearOptionButton.clicked.connect(self.__clear_option)

        self.renderDialogButton.setIcon(FIF.VIEW.icon())
        self.renderDialogButton.clicked.connect(self.__toggle_dialog_view)

        self.nextDialogButton.setIcon(FIF.PAGE_RIGHT.icon())
        self.nextDialogButton.clicked.connect(self.__next_dialog)

        self.lastDialogButton.setIcon(FIF.PAGE_LEFT.icon())
        self.lastDialogButton.clicked.connect(self.__last_dialog)

        self.saveDialogButton.setIcon(FIF.SAVE.icon())
        self.saveDialogButton.clicked.connect(self.save_dialog)
        self.badge = IconInfoBadge.attension(
            FIF.SYNC, 
            self.saveBox, 
            target=self.saveDialogButton, 
            position=InfoBadgePosition.TOP_RIGHT)
        self.badge.hide()

        self.badge_op = IconInfoBadge.attension(
            FIF.SYNC, 
            self.OptionEditBox, 
            target=self.optionIDLabel, 
            position=InfoBadgePosition.BOTTOM_RIGHT)
        self.badge_op.hide()

        self.resetDialogButton.setIcon(FIF.SYNC.icon())
        self.resetDialogButton.clicked.connect(self.__reset_dialog)

        self.addOptionButton.setIcon(FIF.ADD.icon())
        self.addOptionButton.clicked.connect(self.__add_option_to_dialog)

        self.dialogTextEdit.textChanged.connect(self.__dialog_update_text)

        self.characterName.line_edit.textUpdated.connect(self.__set_character_name)

        for align in OptionAlign:
            self.AlignComboBox.addItem(QCoreApplication.translate("Align",align.title))
            self.AlignComboBox.setItemData(self.AlignComboBox.count() - 1, QColor(align.color))
        self.AlignComboBox.setCurrentIndex(2)
        self.AlignComboBox.currentIndexChanged.connect(self.__set_align)

        self.optionComboBox.currentIndexChanged.connect(self.__change_option_from_combobox)

        self.optionCommentEdit.textUpdated.connect(self.__option_update_comment)
        self.optionCommentEdit.clicked.connect(self.__save_option)
        self.optionCommentEdit.toolButton.setIcon(FIF.SAVE)

        self.optionLineEdit.line_edit.textUpdated.connect(self.__option_update_text)

        self.tipLineEdit.line_edit.textUpdated.connect(self.__option_update_tip)

        self.optionNextBox.valueChanged.connect(self.__set_next_option)

        self.createOptionButton.setIcon(FIF.ADD)
        self.createOptionButton.clicked.connect(self.__create_option)

        self.startBox.currentIndexChanged.connect(self.__jump_to_dialog)

    def load_file(self):
        """加载文件到显示区"""
        data = self.file.data
        self.__file_saved()

        self.__connect_combobox(False)
        self.dialogComboBox.clear()
        self.dialogComboBox.addItems(data['dialog'].keys())
        self.dialogSpinBox.setMaximum(len(data['dialog'])+1)
        self.dialog = data['dialog']['0'].copy()
        self.option = data['option']['0'].copy()

        self.__load_conditions()

        self.change_dialog('0')
        self.__change_option('0')
        self.__connect_combobox(True)
        self.allOptionsComboBox.clear()
        self.optionComboBox.clear()
        for index, option in enumerate(data['option']):
                content = option+','+self.file.data['option'][option]['comment']
                self.allOptionsComboBox.addItem(content)
                self.optionComboBox.addItem(content)
                # self.allOptionsComboBox.setItemData(index, self.file.data['option'][option]['text'], Qt.ToolTipRole)
        self.__file_saved()
        self.__load_preview()
        self.setEnabled(True)

    def save_all(self):
        self.__save_option()
        self.save_dialog()

    # region Save InfoBar
    def __file_unsaved(self):
        if self.__has_same_infoBar(QCoreApplication.translate('Form','更改未保存')):
            return
        self.currentInfoBar = InfoBar.info(
            title=QCoreApplication.translate('Form','更改未保存'),
            content=self.file.path,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,    
            parent=self
        )
        self.currentInfoBar.setFont(QFont("VonwaonBitmap 16px",12))
    def __file_saved(self):
        if self.__has_same_infoBar(QCoreApplication.translate('Form','已是最新')):
            return
        self.currentInfoBar = InfoBar.success(
            title=QCoreApplication.translate('Form','已是最新'),
            content=self.file.path,
            orient=Qt.Horizontal,
            position=InfoBarPosition.TOP_RIGHT,
            duration=-1,    
            parent=self
        )
        self.badge.hide()
    def __has_same_infoBar(self,key)->bool:
        if self.currentInfoBar:
            try:
                if key == self.currentInfoBar.title:
                    return True
                self.currentInfoBar.close()
            except RuntimeError:
                pass
            return False
    # endregion

    # region Dialog
    def save_dialog(self):
        print("保存对话中...")
        id = self.dialogID
        # if id !=  self.dialogComboBox.currentText():
        #     return
        if self.dialog['options']:
            self.dialog['next'] = '-1'
        self.file.data['dialog'][id] = self.dialog.copy()
        # self.save_option()
        self.badge.hide()
        self.dialog_unsaved = False
        print("对话已保存")
        self.__load_preview()
        self.startBox.setCurrentIndex(int(id))

    def __reset_dialog(self):
        # id = str(self.dialogSpinBox.value())
        # if id !=  self.dialogComboBox.currentText():
        #     return
        self.dialog = self.file.data['dialog'][self.dialogID].copy()
        self.change_dialog(self.dialogID)
    def __clear_dialog(self):
        self.dialog = {
            "character": "none",
            "text": "",
            "options": [],
            "next": "-1"
        }
        self.change_dialog(self.dialogID)

    def __change_dialog_from_combobox(self):
        self.__save_dialog_confirm()
        # self.dialogComboBox = ComboBox()
        self.dialogID = self.dialogComboBox.currentText()
        try:
            self.dialog = self.file.data['dialog'][self.dialogID].copy()
        except KeyError:
            self.create_dialog()

        self.change_dialog(self.dialogID)
    def __change_dialog_from_spinbox(self):
        self.__save_dialog_confirm()
        self.dialogID = str(self.dialogSpinBox.value())
        try:
            self.dialog = self.file.data['dialog'][self.dialogID].copy()
        except KeyError:
            self.create_dialog()

        # self.dialogSpinBox = SpinBox()

        self.change_dialog(self.dialogID)

    def change_dialog(self,id:str):
        self.__connect_combobox(False)
        self.dialogSpinBox.setValue(int(id))
        self.dialogComboBox.setCurrentText(id)
        self.dialogID = id
        self.__connect_combobox(True)
        self.characterName.setText(self.dialog['character'])
        self.nextDialogBox.setValue(int(self.dialog['next']))
        self.dialogTextEdit.setText(self.dialog['text'])
        self.__toggle_dialog_view()
        self.__toggle_dialog_view()
        self.__load_options()
        self.dialog_unsaved = False
        self.badge.hide()
    def create_dialog(self):
        new_dialog = {
                "character": self.dialog['character'],
                "text": "",
                "options": [],
                "next": "-1"
        }
        print('创建新对话')
        # self.file.data['dialog'][id] = new_dialog
        self.dialog = new_dialog
        self.dialogSpinBox.setMaximum(len(self.file.data['dialog'])+1)
        self.dialogComboBox.addItem(str(self.dialogSpinBox.maximum()-1))
        self.file.data['dialog'][str(self.dialogSpinBox.maximum()-1)] = new_dialog
        self.__file_unsaved()

    def __connect_combobox(self,connect:bool):
        commands = [
            (self.dialogComboBox.currentIndexChanged.disconnect,self.__change_dialog_from_combobox),
            (self.dialogSpinBox.valueChanged.disconnect,self.__change_dialog_from_spinbox),
            (self.nextDialogBox.valueChanged.disconnect,self.__set_next_dialog)
        ]
        for func, *args in commands:
            try:
                func(*args)
            except TypeError:
                pass

        if connect:
            self.dialogComboBox.currentIndexChanged.connect(self.__change_dialog_from_combobox)
            self.dialogSpinBox.valueChanged.connect(self.__change_dialog_from_spinbox)
            self.nextDialogBox.valueChanged.connect(self.__set_next_dialog)

    def __add_option_to_dialog(self):
        option_str = str(self.allOptionsComboBox.currentText())
        if option_str:
            option = option_str.split(',')[0]
            if option in self.dialog['options']:
                return
            self.dialog['options'].append(option)

            self.optionForm.layout().removeWidget(self.addOptionButton)
            self.optionForm.layout().removeWidget(self.allOptionsComboBox)
            content = option+','+self.file.data['option'][option]['comment']
            tooltip = self.file.data['option'][option]['text']
            row  = OptionRow(self,content,tooltip)
            self.optionForm.layout().addRow(row.container,row.container_form)
            # row.clicked.connect(self.remove_option_from_dialog)

            self.optionForm.layout().addRow(self.addOptionButton,self.allOptionsComboBox)
            # self.load_options()
            self.badge.show()
            self.dialog_unsaved = True
            self.__file_unsaved()
        self.allOptionsComboBox.setCurrentText(option_str)

    def remove_option_from_dialog(self,content:str):
        if content:
            option = content.split(',')[0]
            if option in self.dialog['options']:
                self.dialog['options'].remove(option)
                self.__load_options()
                self.badge.show()
                self.dialog_unsaved = True
                self.__file_unsaved()

    def __dialog_update_text(self):
        # if not modified:
        #     return
        
        self.dialog['text'] = self.dialogTextEdit.text()
        # print('对话更新为'+self.dialog['text'])
        self.badge.show()
        self.dialog_unsaved = True
        self.__file_unsaved()
    def __toggle_dialog_view(self):
        current_index = self.stackedWidget.currentIndex()
        new_index = 1 - current_index
        self.stackedWidget.setCurrentIndex(new_index)
        match new_index:
            case 0:
                self.renderDialogButton.setIcon(FIF.VIEW.icon())
            case 1:
                self.renderDialogButton.setIcon(FIF.EDIT.icon())
        self.dialogBrowser.setHtml(f"""
            <div style="font-family: 'VonwaonBitmap 16px'; font-size: 15pt; text-align:center;">
                {tmp_to_html(self.dialogTextEdit.toPlainText())}
            </div>
        """)

    def __load_options(self):
        options = self.dialog['options']
        
        self.optionForm.layout().removeWidget(self.addOptionButton)
        self.optionForm.layout().removeWidget(self.allOptionsComboBox)

        for i in reversed(range(self.optionForm.layout().count())): 
            widget = self.optionForm.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        if options:
            for option in options:
                content = option+','+self.file.data['option'][option]['comment']
                tooltip = remove_all_tags(self.file.data['option'][option]['text']+f' ({self.file.data['option'][option]['tip']})')
                row  = OptionRow(self,content,tooltip)
                self.optionForm.layout().addRow(row.container,row.container_form)
                # row.clicked.connect(self.remove_option_from_dialog)
        self.allOptionsComboBox.setCurrentIndex(-1)
        self.optionForm.layout().addRow(self.addOptionButton,self.allOptionsComboBox)
                # self.allOptionsComboBox.addItem(content)

    def __set_next_dialog(self):
        self.dialog['next'] = str(self.nextDialogBox.value())
        self.badge.show()
        self.dialog_unsaved = True
        self.__file_unsaved()
    def __set_character_name(self):
        self.dialog['character'] = self.characterName.line_edit.text()
        self.badge.show()
        self.dialog_unsaved = True
        self.__file_unsaved()
    
    def __next_dialog(self):
        self.dialogComboBox.setCurrentIndex(self.dialogSpinBox.value()+1)
    def __last_dialog(self):
        self.dialogComboBox.setCurrentIndex(self.dialogSpinBox.value()-1)
    def __save_dialog_confirm(self):
        if self.dialog_unsaved:
            confirm = ConfirmDialog(QCoreApplication.translate('Form',"未保存"),QCoreApplication.translate('Form',"要保存当前对话吗"))
            if confirm.exec_() == QDialog.Accepted:
                self.save_dialog()
    # endregion

    # region Option
    def __change_option_from_combobox(self):
        option_str = str(self.optionComboBox.currentText())
        if option_str:
            option = option_str.split(',')[0]
            try:
                self.__save_option_confirm()
                self.option = self.file.data['option'][option].copy()
                self.__change_option(option)
            except KeyError:
                pass
    def __change_option(self,id:str):
        self.__connect_combobox(False)
        self.optionIDLabel.setText(id)
        self.__connect_combobox(True)
        self.optionNextBox.setValue(int(self.option['next']))
        self.optionLineEdit.setText(self.option['text'])
        self.optionCommentEdit.setText(self.option['comment'])
        self.AlignComboBox.setCurrentIndex(self.option['align']+2)
        self.tipLineEdit.setText(self.option['tip'])
        self.__load_conditions()
        self.__load_options()
        self.badge_op.hide()
        self.option_unsaved = False
    def __save_option(self):
        print('选项已保存')
        id = self.optionIDLabel.text()
        conds = self.option.get('conditions',[])
        conds.clear()
        for condition in self.conditions:
            if condition.data:
                conds.append(','.join(condition.data))

        self.file.data['option'][id] = self.option.copy()
        self.optionComboBox.setItemText(int(id),id+','+self.option['comment'])
        self.allOptionsComboBox.setItemText(int(id),id+','+self.option['comment'])
        self.__jump_to_dialog(self.startBox.currentIndex())    
        self.badge_op.hide()
        self.option_unsaved = False
        
    def __reset_option(self):
        id = str(self.optionIDLabel.text())
        self.option = self.file.data['option'][id].copy()
        self.badge_op.hide()
        self.option_unsaved = False
        self.__change_option(id)

    def __clear_option(self):
        self.option = {
                "comment": "",
                "text": "",
                "align": 0,
                "tip": "",
                "next": "-1",
                "conditions":[]
            }
        self.badge_op.show()
        self.option_unsaved = True
        self.__change_option(self.optionIDLabel.text())
    def __create_option(self):
        self.__save_option_confirm()
        new_option = {
                "comment": "none",
                "text": "",
                "align": 0,
                "tip": "",
                "next": "-1",
                "conditions":[]
            }
        # self.file.data['dialog'][id] = new_dialog
        id = int(max(self.file.data['option'].keys(),key=int))+1
        self.optionIDLabel.setText(str(id))
        self.option = new_option
        self.__change_option(str(id))
        self.optionComboBox.addItem(str(id)+','+self.option['comment'])
        self.allOptionsComboBox.addItem(str(id)+','+self.option['comment'])

        self.optionComboBox.currentIndexChanged.disconnect(self.__change_option_from_combobox)
        self.optionComboBox.setCurrentIndex(self.optionComboBox.count()-1)
        self.optionComboBox.currentIndexChanged.connect(self.__change_option_from_combobox)

        self.__save_option()
        self.__file_unsaved()

    def __option_update_text(self):
        self.option['text'] = self.optionLineEdit.line_edit.text()
        print('选项文本更新为'+self.option['text'])
        self.badge_op.show()
        self.option_unsaved = True
        self.__file_unsaved()
    def __option_update_tip(self):
        self.option['tip'] = self.tipLineEdit.line_edit.text()
        print('选项提示更新为'+self.option['tip'])
        self.badge_op.show()
        self.option_unsaved = True
        self.__file_unsaved()
    def __option_update_comment(self):
        self.option['comment'] = self.optionCommentEdit.text()
        print('选项备注更新为'+self.option['comment'])
        self.badge_op.show()
        self.option_unsaved = True
        self.__file_unsaved()
    def __set_next_option(self):
        self.option['next'] = str(self.optionNextBox.value())
        self.badge_op.show()
        self.option_unsaved = True
        self.__file_unsaved()
    def __set_align(self,index:int):
        # self.AlignComboBox = ComboBox()
        palette = self.AlignComboBox.palette()
        palette.setColor(QPalette.Text, QColor("red"))  # 设置文本颜色
        self.AlignComboBox.setPalette(palette)

        self.option['align'] = index-2
        self.badge_op.show()
        self.option_unsaved = True
        self.__file_unsaved()
    def __save_option_confirm(self):
        if self.option_unsaved:
            confirm = ConfirmDialog(QCoreApplication.translate('Form',"未保存"),QCoreApplication.translate('Form',"要保存当前选项吗"))
            if confirm.exec_() == QDialog.Accepted:
                self.__save_option()

    def __load_conditions(self):
        self.conditionForm.layout().removeWidget(self.addConditionButton)
        for i in reversed(range(self.conditionForm.layout().count())): 
            widget = self.conditionForm.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
            self.conditions = []

        for cond in self.option.get('conditions',[]):
            condBox = ConditionBox(self,cond)
            self.conditionForm.layout().addRow(condBox)
            self.conditions.append(condBox)

        # self.conditionBox = ConditionBox(self)
        # self.conditionForm.layout().addRow(self.conditionBox)
        self.conditionForm.layout().addRow(self.addConditionButton)
    def __initConditionButton(self):
        self.addConditionButton.setMenu(RoundMenu())
        self.addConditionButton.menu().addActions([
            Action(FIF.ADD,self.tr('添加OR条件'),self,triggered = self.__create_condition),
            Action(FIF.CANCEL,self.tr('移除OR条件'),self,triggered = self.__remove_condition)
        ])
        self.conditions = []
    def __create_condition(self):
        condition = ConditionBox(self)
        self.conditionForm.layout().removeWidget(self.addConditionButton)
        self.conditionForm.layout().addRow(condition)
        self.conditionForm.layout().addRow(self.addConditionButton)
        self.conditions.append(condition)
        self.__file_unsaved()
        self.option_unsaved = True
        self.badge_op.show()
    def __remove_condition(self):
        if self.conditions:
            self.conditionForm.layout().removeWidget(self.conditions[-1])
            self.conditions[-1].deleteLater()
            self.conditions.pop(-1)
            self.__file_unsaved()
            self.option_unsaved = True
            self.badge_op.show()

    # endregion

    # region previewer
    def __load_preview(self):
        dialogs = self.file.data['dialog']
        self.startBox.clear()
        for id,dialog in dialogs.items():
            self.startBox.addItem(id+':'+replace_placeholders(dialog['character']))

    def __jump_to_dialog(self,index:int):
        self.previous_text = ''
        self.__load_dialog(str(index))
        
    def __load_dialog(self,id:str):
        if id=='-1':
            self.__load_dialog_end()
            return

        data = self.file.data
        try:
            dialog = data['dialog'][id]
            self.continueButton.clicked.disconnect()
        except KeyError:
            return
        except TypeError:
            pass
        self.__set_current_preview_index(int(id))
        self.continueButton.setMenu(RoundMenu())
        
        # self.continueButton.menu().setToolTipsVisible(True)
        # self.continueButton.menu().installEventFilter(
        #     ToolTipFilter(self.continueButton.menu(), showDelay=30, position=ToolTipPosition.BOTTOM))
        self.previous_text += dialog_preview_text(tmp_to_html(dialog['character']),
                                                  tmp_to_html(dialog['text']))
        self.previewBrowser.setHtml(self.previous_text)
        self.__scroll_to_bottom()

        if dialog['next'] == '-1':
            if dialog['options']:
                self.continueButton.setText(self.tr('选项'))
                for option in dialog['options']:
                    self.__set_options_menu(option)
            else:
                self.__load_dialog_end()
        else:
            self.continueButton.setText(self.tr('继续'))
            self.__set_continue_button(dialog['next'])
                             
    def __set_options_menu(self,option:str):
        options  = self.file.data['option']
        tip = options[option]['tip']
        align = OptionAlign(options[option]['align'])

        conditions  = options[option]['conditions']
        content = remove_all_tags(options[option]['text']+f'({tip})'+f'[{align.title}]')
        if conditions:
            submenu = RoundMenu(content)
            self.continueButton.menu().addMenu(submenu)
            for cond in conditions:
                submenu.addAction(
                    Action(condition_to_text(cond),triggered=lambda:self.__option_to_dialog(option))
                )
            return
       
        self.continueButton.menu().addAction(
            Action(content,
                   triggered=lambda:self.__option_to_dialog(option))
        )
        # action.setToolTip(all_conditions_to_text(conditions))
        # action.installEventFilter(
        #     ToolTipFilter(action, showDelay=30, position=ToolTipPosition.BOTTOM))
        # self.continueButton.menu().addAction(action)
    def __set_continue_button(self,next:str):
        self.continueButton.clicked.connect(lambda :self.__load_dialog(next))
    def __option_to_dialog(self,option):
        options  = self.file.data['option']
        text = options[option]['text']+f'({options[option]['tip']})'
        align = OptionAlign(options[option]['align'])
        text = tmp_to_html(text) + f' [<span style="color:{align.color}">{align.title}</span>]'
        self.previous_text+= dialog_preview_text(self.tr('选项'),text,True)
        self.previewBrowser.setHtml(self.previous_text)
        self.__scroll_to_bottom()
        self.__load_dialog(options[option]['next'])
    def __scroll_to_bottom(self):
        # 滚动到垂直滚动条的最大位置
        self.previewBrowser.verticalScrollBar().setValue(self.previewBrowser.verticalScrollBar().maximum())
    def __load_dialog_end(self):
        self.continueButton.setText(self.tr('结束对话'))
        self.previous_text+= dialog_preview_text(self.tr('选项'),f'<i>{self.tr('对话已结束')}</i>',True)
        self.previewBrowser.setHtml(self.previous_text)
        self.__scroll_to_bottom()
        self.continueButton.menu().clear()
        try:
            self.continueButton.clicked.disconnect()
        except TypeError:
            pass
    def __set_current_preview_index(self,index:int):
        self.startBox.currentIndexChanged.disconnect(self.__jump_to_dialog)
        self.startBox.setCurrentIndex(index)
        self.startBox.currentIndexChanged.connect(self.__jump_to_dialog)
    # endregion

class SettingsInterface(ScrollArea):
    def __init__(self, text:str, parent=None):
        super().__init__(parent=parent)

        self.setObjectName(text.replace(' ', '-'))
        
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.saveGroup = SettingCardGroup(
            self.tr('自动保存'), self.scrollWidget)
        self.autosaveCard = SwitchSettingCard(
            FIF.SYNC,
            self.tr('自动保存'),
            self.tr('启用定时自动保存'),
            None,
            self.saveGroup
        )
        
        self.timeCard = RangeSettingCard(
            FIF.STOP_WATCH,
            self.tr('保存间隔'),
            self.tr('自动保存间隔（秒）'),
            parent=self.saveGroup
        )
        
        self.languageGroup = SettingCardGroup(
            self.tr('语言'), self.scrollWidget)

        self.languageCard = ComboBoxSettingCard(
            FIF.LANGUAGE,
            self.tr('语言'),
            self.tr('选择语言（需要重启应用）'),
            texts=['简体中文', 'English'],
            parent=self.languageGroup
        )

        
        self.__initWidget()
        self.__connectSignals()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')
        self.enableTransparentBackground()
        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        # self.settingLabel.setObjectName('settingLabel')
        # StyleSheet.SETTING_INTERFACE.apply(self)

        # self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        # self.__connectSignalToSlot()
    def __initLayout(self):

        self.saveGroup.addSettingCard(self.autosaveCard)
        self.saveGroup.addSettingCard(self.timeCard)

        self.languageGroup.addSettingCard(self.languageCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.saveGroup)
        self.expandLayout.addWidget(self.languageGroup)

    def __connectSignals(self):
        self.autosaveCard.setChecked(self.parent().settings.get_setting('auto save'))
        self.autosaveCard.checkedChanged.connect(self.parent().enable_auto_save)

        self.timeCard.slider.setRange(30,300)
        self.timeCard.setValue(int(self.parent().auto_save_time/1000))
        self.timeCard.valueChanged.connect(self.parent().change_save_time)

        index = 0
        if self.parent().settings.get_setting('language') == 'en_US':
            index = 1
        self.languageCard.comboBox.setCurrentIndex(index)
        self.languageCard.comboBox.currentIndexChanged.connect(self.parent().change_language)