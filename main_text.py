import json,sys,os
import initialize_agents

import os,json,sys,configparser
import readline

workdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(workdir)

def input_with_delete(prompt=''):
    readline.parse_and_bind("set editing-mode vi")  # 设置编辑模式为vi（可选）
    line = input(prompt)
    return line

# 增加程序启动时的开机广告，并且告知用户智能音箱的唤醒词。
# print(f"system:我是你的智能助手，欢迎开始和我对话。")

# 这是用于判断一个字符串中，是不是包含一个列表中的任意词，如果包含就会返回列表中的这个元素。
# 实际业务上，是判断语音转为文字的内容，是不是包含任意一个智能语音助手的激活关键词。
def find_robot_keyword(s,lst):
    for elem in lst:
        if elem in s:
            return elem
    return None

class Yoyo:
    def __init__(self):
        with open(robot_info_file_path , 'r' ,encoding="UTF-8") as f:
            # 导入智能助手的配置文件。
            self.robot_info = json.load(f)
            self.robot_id_list = [d['robot_id'] for d in self.robot_info]
            self.robot_keywords_list = [d['robot_keyword'] for d in self.robot_info]
    

    def run(self):
        print(f"system:欢迎进入HiYoyo智能助手，你可以直接对话，也可以输入「模式切换」，切换到其他对话模式。")  
        print(f"system:当前和你会话的是「{self.robot_name}」。智能助手介绍：{self.robot_describe}")    
        while True:
            # 唤醒后，打印和播放当前智能语音助手的打招呼语。     
            q = input_with_delete(f"{self.username}：") # 获取用户输入的内容。
            robot_keyword = find_robot_keyword(q,self.robot_keywords_list) #判断用户录入的内容是不是包含任意一个智能语音助手的激活关键词。如果不包含，就请求ChatGPT的结果。如果包含，就切换到对应的智能语音助手。
            hotword_keyword = find_robot_keyword(q,self.hotword_list)
            if robot_keyword == None and hotword_keyword == None:
                #print(f'{self.username}:{q}') # 打印用户录入的内容
                print(f'{self.robot_name}(GPT)：',end='') 
                res = chatmult.chatmult(self.username,q,self.robot_system_content,self.robot_function_model,voice_name="") # 请求ChatGPT的接口。
                print("")
                # print(f'{self.robot_name}(GPT)：{res}')   # 打印返回的结果。
            elif robot_keyword == None and hotword_keyword != None:
                self.hotword(hotword_keyword)
            else:
                switch_robot_index = self.robot_keywords_list.index(robot_keyword)
                switch_robot_id = self.robot_info[switch_robot_index]["robot_id"] # 确定要切换到哪一个智能语音助手。
                self.robot_model(switch_robot_id)   #切换智能语音助手。
                print(f"system:已切换到「{robot_keyword}」。")                                      

    def loop(self,):
        while True:
            try:
                self.run()
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    yoyo = Yoyo()
    yoyo.loop()
