# 简单智能官方实现

官方网站 [http://www.www.easysmart.top](http://www.easysmart.top)

新设备&demo投稿请提交issue

# 使用本项目的demo

## 人类反馈强化学习（开发中）
https://github.com/jiandanzhineng/humanRL

# 安装方式

```shell
pip install easysmart
```
# 在其他脚本中使用
```python
import easysmart as ezs
import threading
import pathlib
root_path = pathlib.Path(__file__).parent.absolute().joinpath('data')
main_server_thread = threading.Thread(target=ezs.start_server, args=(root_path,))
main_server_thread.daemon = True
main_server_thread.start()
```

# HTTP API

https://console-docs.apipost.cn/preview/91b7075b8e535790/83ff4d1e5753d015

