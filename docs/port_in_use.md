# 启动中遇到端口被系统保留问题

## 问题产生原因

windows会保留一部分端口，但是端口被占用并且没有占用的程序，一般是因为hyper-V服务占用了这个端口，导致端口被保留。

可以在cmd中执行
```
netsh interface ipv4 show excludedportrange protocol=tcp
```
查看被保留的端口

## 解决方案
1. 在windows中 关闭所有hyper-V相关服务
2. 重启电脑
3. 管理员cmd中执行 
```
netsh int ipv4 set dynamicport tcp start=49152 num=16383
```
4. 重启电脑
5. 重新启动项目
