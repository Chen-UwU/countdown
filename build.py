"""
这个文件的用途为快速构建一个可以直接分发的文件包
"""

import os
import subprocess
import shutil

for root, dirs, files in os.walk("./dist", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

source_paths = ["./cache", "./config", "./adapter", "./font", "./image", "./plugin"]
target_path = "./dist"
for i in source_paths:
    if os.path.exists(target_path + i[1:]):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path + i[1:])
    # if not os.path.exists(target_path+i[1:]):
    #     # 如果目标路径不存在原文件夹的话就创建
    #     os.makedirs(target_path+i[1:])
    shutil.copytree(i, target_path + i[1:])

print("第一次编译时间可能较长，耐心等待1到2分钟即可。")
# proc = subprocess.Popen(
#     'poetry run pyinstaller countdown.spec',
#     stdin=None, # 标准输入 键盘
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     shell=True)
# outinfo, errinfo = proc.communicate() # 获取输出和错误信息
# print(outinfo.decode("utf-8")) # 外部程序 (windows系统)决定编码格式
# print(errinfo.decode("utf-8"))
os.system("poetry run pyinstaller countdown.spec")
