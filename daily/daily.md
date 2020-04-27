## 1. MacOS挂载NTFS硬盘
```
# 创建文件 fstab
sudo vim /etc/fstab
# 输入 LABEL=XXX none ntfs rw,auto,nobrowse
# XXX 为硬盘的名称
open /Volumes
```
## 2. 连接github
测试是否连接

`ssh -T git@github.com`

## 3. 虚拟天文馆
支持全平台的虚拟天文馆软件[stellarium](https://stellarium.org). 可访问github[Stellarium/stellarium](https://github.com/Stellarium/stellarium)


