import datetime
import os
import sys
import time


import click_func as cf
from call_back_func import press_f, begin_fb_loop, change_to_outer_fb, leave_team,press_esc

# 全局状态
# 0.初始化
# 1.准备进入副本
# 2.在副本中
# 3.进入副本前置动作
# 4.出现全局异常
# 5.人物死亡
# 6.出现全局异常
global_status = 0
# 图像识别类
automation_tool = None
replay = None
fb_times = 0
fb_time_out_times = 0
fb_time_out_sec = 300
last_fb_start_time = time.time()
# 进本前的职业
target_careers = None
# 进本前的职业
red_careers = None
fb_difficulty_mode = 1
def get_image_path(relative_path):
    """
    获取图片的绝对路径，同时兼容开发环境和打包后的环境

    参数:
        relative_path: 图片相对于项目根目录的路径
                       例如: "images/logo.png" 或 "resources/background.jpg"
    """
    try:
        # 打包后的环境：资源会被解压到sys._MEIPASS临时目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境：使用当前文件所在目录
        base_path = os.path.abspath(os.path.dirname(__file__))

    # 拼接完整路径
    return os.path.join(base_path, relative_path)


script_json = get_image_path('resource/json/蒂娜.json')


def print_log(str):
    print(f"{datetime.now()}:{str}")


class img_info:
    def __init__(self, path, click_func=None, call_back=None, status_change_to=None, interval=3, threshold=0.95,
                 check_when_status=None):
        self.path = path
        self.click_func = click_func
        self.call_back = call_back
        self.status_change_to = status_change_to
        self.interval = interval
        self.threshold = threshold
        self.check_when_status = check_when_status


img_info_arr = [
    img_info(get_image_path("resource/img/change_to_single.png"), click_func=cf.change_to_single, status_change_to=1,
             check_when_status=[1, 2]),
    img_info(get_image_path("resource/img/gotoFb.png"), click_func=cf.gotoFb, status_change_to=1, threshold=0.9,
             check_when_status=[1, 2]),
    img_info(get_image_path("resource/img/trigger_fb.png"), click_func=None, status_change_to=2, check_when_status=[2]),
    img_info(get_image_path("resource/img/win.png"), click_func=None, status_change_to=0, check_when_status=[2],
             threshold=0.9),
    img_info(get_image_path("resource/img/die.png"), click_func=cf.qilai, status_change_to=None,
             threshold=0.7),
    img_info(get_image_path("resource/img/esc.png"), click_func=press_esc,
             threshold=0.88),
]


class ocr_info:
    def __init__(self, match_str, pos, operation=None, check_when_status=None, need_pos=False):
        self.match_str = match_str
        self.pos = pos
        self.operation = operation
        self.check_when_status = check_when_status
        self.need_pos = need_pos

    def is_match(self, results):
        if results:
            for result in results:
                ocr_str, pos = result
                if self.match_str in ocr_str:
                    if self.need_pos:
                        self.operation(pos)
                    else:
                        self.operation()
        return False


ocr_info_arr = {
    "副本入口": ocr_info("F", (1371, 534, 280, 80), operation=press_f, check_when_status=[1]),  # 检查是否有“F”
    "副本内": ocr_info("退出副本", (39, 226, 296, 33), operation=begin_fb_loop, check_when_status=[1]),  # 检查是否有“退出”
    "副本外": ocr_info("阿斯特", (41, 228, 83, 26), operation=change_to_outer_fb, check_when_status=[2]),  # 检查是否有“阿斯特”
    "未退队": ocr_info("超过2人", (721, 265, 476, 50), operation=leave_team, check_when_status=[1, 3]),
    # 你的队伍人数超过2人，无法进行此模式
}
