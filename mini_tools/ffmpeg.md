## YUV序列播放
```shell
ffplay -f rawvideo -video_size 1920x1080 input.yuv
```
## YUV序列转AVI
```shell
ffmpeg –s w*h –pix_fmt yuv420p –i input.yuv –vcodec h264 output.avi

ffmpeg –s w*h –pix_fmt yuv420p –i input.yuv –vcodec hevc output.avi
```
## 其他格式转YUV
```shell
ffmpeg -i input.avi -pix_fmt yuv420p output.YUV
```
