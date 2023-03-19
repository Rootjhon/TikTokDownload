# example.py
import TikTokDownload as TK
import Util

# 单视频下载
TK.video_download(*TK.main())

# 批量下载
if __name__ == '__main__':
    # 获取命令行参数
    cmd = Util.Command()
    # 获取headers
    headers = Util.Cookies(cmd.setting()).dyheaders
    # 获取主页内容
    profile = Util.Profile(headers)
    # 使用参数并下载
    profile.getProfile(cmd.setting())
    input('[  完成  ]:已完成批量下载，输入任意键后退出:')