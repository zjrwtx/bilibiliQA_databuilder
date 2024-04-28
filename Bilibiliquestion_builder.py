import openai
from openai import OpenAI
from dotenv import load_dotenv

import time
import random

import asyncio
from bilix.sites.bilibili import DownloaderBilibili
from bcut_asr import run_everywhere
from argparse import Namespace
import os


# Replace 'YOUR_VIDEO_ID' with the ID of the YouTube video you want to download subtitles for
video_url = input("请输入你要生成视频问题的bilibili 视频地址: e.g.")
question_num=input("要生成的问题的个数:")
question_language=input("生成的问题的语言: 中文，English, etc. ")



try:
    async def main():
        async with DownloaderBilibili() as downloader:
            # 下载视频并获取文件名
            await downloader.get_video(video_url)
            # 设置包含视频文件的文件夹路径
            video_folder_path = './'

            # 遍历文件夹中的所有文件
            for filename in os.listdir(video_folder_path):
                # 检查文件扩展名是否为视频文件，这里我们假设视频文件扩展名为.mp4
                if filename.endswith('.mp4'):
                    # 构建完整的文件路径
                    file_path = os.path.join(video_folder_path, filename)
                    
                    # 打开视频文件
                    with open(file_path, "rb") as f:
                        # 创建Namespace对象，设置参数
                        argg = Namespace(format="txt", interval=15.0, input=f, output=None)
                        
                        # 运行语音识别并生成字幕
                        run_everywhere(argg)
    asyncio.run(main())

except Exception as e:
    print(f"An error occurred: {e}")

import os

# 指定要遍历的文件夹路径
folder_path = './'

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    # 检查文件扩展名是否为.txt
    if filename.endswith('.txt'):
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, filename)
        # 打开文件并进行操作
        with open(file_path, 'r', encoding='utf-8') as file:
            # 这里可以添加读取文件内容的代码
            content = file.read()
            print(f'文件 {filename} 的内容是：')
            print(content)


# 在使用API密钥和基础URL之前加载.env文件
load_dotenv()

# 现在可以通过os.environ访问这些值
API_BASE = os.environ.get("API_BASE")
API_KEY = os.environ.get("API_KEY")


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=API_KEY,
    base_url=API_BASE
)
completion = client.chat.completions.create(
    model="yi-34b-chat-200k",
    messages=[{"role": "system", "content":"你是一个QA问答对构建专家，专门根据用户视频的内容构建"+question_num+"个高质量的"+question_language+"问题："},
              {"role":"user","content":"生成"+question_num+"个高质量的问题："+content+";并每个问题输出显示都要换行"},
              ],
    max_tokens=6000,
    top_p=0.8,
    # stream=True,
)
outputtext=completion.choices[0].message.content
print(outputtext)
with open('questions.txt', 'w', encoding='utf-8') as file:
    file.write(outputtext)

print("输出内容已保存到questions.txt文件中。")
# for chunk in completion:
#     # print(chunk) 
#     print(chunk.choices[0].delta.content or "", end="", flush=True)


# https://www.youtube.com/watch?v=CjTTSa33axg