# 用ffmpeg批量提取视频里的音频
import os
import sys
curr_dir = os.path.dirname(os.path.realpath(__file__)) # current directory
curr_dir_file = os.listdir(curr_dir)
bkup_dir_name= curr_dir+'/'+'video'
audios_file=curr_dir+'/'+'audio'
#print('curr_dir_file=',curr_dir_file)
#print('bkup_dir_name=',bkup_dir_name)
# 视频格式
video_format = ('.mp4','.avi','.rmvb','.mkv')
# 创建备份目录和音频存放目录
if not os.path.exists(bkup_dir_name):
    os.mkdir(bkup_dir_name)
if not os.path.exists(audios_file):
    os.mkdir(audios_file)
for videos in curr_dir_file:
    if videos.endswith(video_format):
        video=videos.replace(' ','\\ ') # 空格替换为\空格
        dotindex=video.rfind('.')       # 找到最后一个.的索引
	# 给音频命名
        if dotindex != -1:
            audios=video[:dotindex]
        else:
            audios=video
        audio=audios+'.aac'
	# 将各个命令转换为字符串
        commandffmpeg='ffmpeg -i '+video+' -vn -acodec copy '+video+'.aac'
        commandmvv='mv '+curr_dir+'/'+video+' '+bkup_dir_name+'/'+video
        commandmva='mv '+curr_dir+'/'+video+'.aac'+' '+audios_file+'/'+audio
	# 运行shell命令
        os.system(commandffmpeg)
        os.system(commandmvv)
        os.system(commandmva)
