import os
import subprocess

def convert_ui_to_py(ui_file, output_dir=None):
    """
    将 .ui 文件转换为 .py 文件。
    
    参数：
    ui_file (str): .ui 文件的路径。
    output_dir (str): 输出目录。如果为 None，则输出至与 .ui 文件相同的目录。
    """
    if not ui_file.endswith(".ui"):
        print(f"{ui_file} 不是 .ui 文件")
        return

    # 设置输出路径
    py_file = os.path.splitext(ui_file)[0] + ".py"
    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        py_file = os.path.join(output_dir, os.path.basename(py_file))
    
    # 调用 pyuic5 命令进行转换
    try:
        subprocess.run(["pyuic5", "-o", py_file, ui_file], check=True)
        print(f"成功将 {ui_file} 转换为 {py_file}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e}")

# 示例用法
if __name__ == "__main__":
    ui_directory = "E:\项目\project Chess\jsonEditor"  # 指定 .ui 文件所在的目录
    output_directory = "E:\项目\project Chess\jsonEditor"  # 指定 .py 文件的输出目录

    # 查找指定目录下的所有 .ui 文件并进行转换
    for filename in os.listdir(ui_directory):
        if filename.endswith(".ui"):
            ui_path = os.path.join(ui_directory, filename)
            convert_ui_to_py(ui_path, output_directory)
