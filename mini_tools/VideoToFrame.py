# 将视频序列转为图像帧
import cv2
vc=cv2.VideoCapture("/Users/perom/v/output3.mp4")
c=1
if vc.isOpened():
    rval,frame=vc.read()
else:
    rval=False
while rval:
    rval,frame=vc.read()
    cv2.imwrite('/Users/perom/pic/'+str(c)+'.jpg',frame)
    c=c+1
    cv2.waitKey(1)
vc.release()
