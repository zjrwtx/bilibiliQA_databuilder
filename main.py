import asyncio
from bilix.sites.bilibili import DownloaderBilibili
from bcut_asr import run_everywhere
from argparse import Namespace
import os

async def main():
    async with DownloaderBilibili() as downloader:
        # 下载视频并获取文件名
        await downloader.get_video('https://www.bilibili.com/video/BV1UH4y1N7JQ/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=5531fb981ef79f87198a3c2651dff93')
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

if __name__ == "__main__":
    asyncio.run(main())