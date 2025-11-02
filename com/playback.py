import os
import sys
import time
import json
from pynput import keyboard, mouse
from pynput.mouse import Controller, Button

json_file_name = 'recording_1755429068.json'
class InputRecorder:
    def __init__(self):
        self.recording = False
        self.recording_data = []
        self.replaying = False
        # 用于停止回放的事件
        self.stop_replay = False
        self.recorded_data = []


    def on_hot_key_press(self, key):
        if key ==  keyboard.Key.f12:
            self.stop_replay = not self.stop_replay
            if self.stop_replay:
                print("暂停回放，输出已回放数据：")
                print(self.recorded_data)
                self.recorded_data.clear()
            else:
                print("开始回放...")
        if key ==  keyboard.Key.f10:
            print("退出进程...")
            os._exit(1)
    def load_recording(self, filename):
        """从文件加载录制数据"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载失败: {e}")
            return None

    def start_replay(self, filename=None):
        """回放录制的数据"""
        if self.replaying:
            print("正在回放中...")
            return

        # 如果指定了文件名，则加载文件；否则使用当前录制的数据
        data = self.load_recording(filename) if filename else self.recording_data

        if not data:
            print("没有可回放的数据")
            return
        keyboard.Listener(
            on_press=self.on_hot_key_press
        ).start()
        self.replaying = True
        self.stop_replay = True
        print("按F12开始回放，再次按F12暂停回放并输出已执行指令（按F10退出进程）")
        while self.stop_replay==True:
            time.sleep(0.5)
        self._replay(data)

    def _replay(self, data):
        """实际执行回放的方法"""

        keyboard_controller = keyboard.Controller()
        mouse = Controller()
        for event in data:
            if self.stop_replay:
                while self.stop_replay:
                   time.sleep(1)
            self.recorded_data.append(event)
            # 执行事件
            try:
                print(event)
                if event['type'] == 'key_press':
                    key = self._get_key(event['key'])
                    if key:
                        keyboard_controller.press(key)

                elif event['type'] == 'key_release':
                    key = self._get_key(event['key'])
                    if key:
                        keyboard_controller.release(key)
                elif event['type'] == 'mouse_click':
                    mouse.press(Button.left)  # 按下左键
                    time.sleep(event['time'])  # 短暂延迟，模拟实际点击时长
                    mouse.release(Button.left)  # 释放左键
                elif event['type'] == 'sleep':
                    time.sleep(event['time'])

            except Exception as e:
                print(f"回放事件时出错: {e}")

        self.replaying = False
        print("回放结束")



    def _get_key(self, key_str):
        """将按键字符串转换为pynput识别的按键对象"""
        # 特殊按键
        if key_str == 'Key.space':
            return keyboard.Key.space
        elif key_str == 'Key.enter':
            return keyboard.Key.enter
        elif key_str == 'Key.backspace':
            return keyboard.Key.backspace
        elif key_str == 'Key.tab':
            return keyboard.Key.tab
        elif key_str == 'Key.esc':
            return keyboard.Key.esc
        elif key_str == 'Key.shift':
            return keyboard.Key.shift
        elif key_str == 'Key.ctrl':
            return keyboard.Key.ctrl
        elif key_str == 'Key.alt':
            return keyboard.Key.alt
        elif key_str == 'Key.up':
            return keyboard.Key.up
        elif key_str == 'Key.down':
            return keyboard.Key.down
        elif key_str == 'Key.left':
            return keyboard.Key.left
        elif key_str == 'Key.right':
            return keyboard.Key.right

        # 普通字符按键
        if len(key_str) == 1:
            return key_str

        return None



if __name__ == "__main__":
    filename = input("请输入需要回放的json文件的绝对路径\r\n")
    while not os.path.exists(filename):
        filename = input(f"路径：{filename}，不存在，请重新输入\r\n")
    recorder = InputRecorder()
    recorder.start_replay(filename=filename)


#"G:\\xhgm_script\\AutoFuckBKLGetDress\\com\\resource\\json\\鹿.json"