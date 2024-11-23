import json
import os
from collections import deque

class JSONHandler:
    """
    默认结构 catalog:{object:{keys:values}}}
    """

    def __init__(self, path):
        self.path = path
        self.data = self.load_json()
        self.backup = None
        if self.data:
            self.backup = self.data.copy()

    def load_json(self)->dict:
        """
        读取JSON文件内容并加载到字典中。如果文件不存在，则返回空字典。
        """
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("文件内容不是有效的JSON格式，初始化为空字典。")
                    return {}
        else:
            print(self.path+" 文件不存在，创建空数据。")
            return {}
    
    def save_json(self, path)->bool:
        """
        将字典内容写入JSON文件，保存更改，返回True。
        保存失败返回False
        """
        try:
            # 尝试将数据序列化为 JSON 字符串
            json.dumps(self.data)
        except (TypeError, ValueError) as e:
            print("Invalid JSON data:", e)
            return False  # 序列化失败，返回错误
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        return True
    def save_backup(self,path):
        """
        将备份内容写入JSON文件
        """
        try:
            # 尝试将数据序列化为 JSON 字符串
            json.dumps(self.data)
        except (TypeError, ValueError) as e:
            print("Invalid JSON data:", e)
            return False  # 序列化失败，返回错误
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.backup, f, ensure_ascii=False, indent=4)
    def set_catalog(self, catalog_name, default={}):
        """"""
        self.data[catalog_name] = default
        print(f"创建分类 '{catalog_name}' 成功。")
        
    def set_item(self, catalog_name,item_name, default={}):
        """创建或更新JSON中的一个对象（字典）。"""
        self.data[catalog_name][item_name] = default
        print(f"创建对象 '{item_name}' 成功。")

    def create_new_key_for_all_items(self, catalog_name, key):
        for item in self.data[catalog_name]:
            item[key] = None
        print(f"为所有项创建 '{key}' 。")

    def set_key(self, catalog_name, item_name, key, value=None):
        self.data[catalog_name][item_name][key] = value
        print(f"添加/更新键 '{key}' 在对象 '{item_name}' 中，值为：{value}")

    def set_value(self, catalog_name, item_name, key, value):
        """更新指定对象中键的值。"""
        self.data[catalog_name][item_name][key] = value
        print(f"更新对象 '{item_name}' 中键 '{key}' 的值为：{value}")

    def show_data(self):
        """打印当前的数据，用于调试。"""
        print(json.dumps(self.data, indent=4))


class UserSettings(JSONHandler):

    default_settings = {
            "settings":{
                "theme": "light",
                "language": "",
                "notifications": True,
                "auto save":False,
                "auto save time":180000,
            },
            "recent":{
                "path0":None,
                "path1":None,
                "path2":None,
                "path3":None,
                "path4":None
            },
            "new dialog":{
                "dialog":{
                    "0":{
                        "character": "",
                        "text": "",
                        "options": [],
                        "next": "-1"
                    }
                },
                "option":{
                    "0":{
                        "comment": "none",
                        "text": "",
                        "align": 0,
                        "tip": "",
                        "next": "-1",
                        "conditions":[]
                    }
                }
            },
            "default_dialogue": {
                "character": "none",
                "text": "",
                "options": [],
                "next": "-1"
            },
            "default_option": {
                "comment": "",
                "text": "",
                "align": 0,
                "tip": "",
                "next": "-1",
                "conditions":[]
            },
            "default_item":{
                "name":"",
                "description":""
            },
            "placeholders":{
                "names":{
                    "narrator":"旁白",
                    "playerName":"玩家",
                    "self":"self",
                    "opponent":"opponent"

                        }
                
            }}
    
    def __init__(self):
        super().__init__(path = "user_settings.json")
        self.load_defaults()
        
    def load_json(self):
        """
        检查指定路径下是否存在配置文件。
        如果不存在，则创建一个并写入默认设置。
        """
        # 检查配置文件是否存在
        if os.path.exists(self.path):
            print("配置文件已存在，加载配置...")
            with open(self.path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            # 如果配置文件不存在，则创建一个新的
            print("配置文件不存在，创建默认配置...")
            config = self.default_settings
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        
        return config
        
    def load_defaults(self):
        """加载默认设置到用户设置中，若某些设置缺失则补充"""
        for key, value in self.default_settings["settings"].items():
            self.data.setdefault(key, value)

    def set_setting(self, key, value):
        """设置用户偏好并更新文件"""
        self.data["settings"][key] = value
        print(f"设置更新：{key} = {value}")
        self.save_json(self.path)

    def get_setting(self, key):
        """获取某个设置的值"""
        return self.data["settings"].get(key)

    def save_recent_path(self, path:str):
        """存储最近打开的文件路径"""
        paths = deque(reversed(list(self.data["recent"].values())))
        while True:
            if path in paths:
                paths.remove(path)
                paths.append(path)
                print(path+"文件已在列表中")
                break
            if len(paths) <5:
                paths.append(path)
                print(path+"添加到最近打开")
                break
            paths.popleft()
            paths.append(path)
            print(path+"添加到最近打开")
            break
        while len(paths) <5:
            paths.appendleft("")
        for key in reversed(self.data["recent"]):
            self.data["recent"][key] = paths.popleft()

        self.save_json(self.path)
            
    def reset_to_defaults(self):
        """重置为默认设置"""
        self.data["settings"] = self.default_settings.copy()
        self.save_json()
        print("设置已重置为默认值")