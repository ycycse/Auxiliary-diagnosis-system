# CT_AI_WEB

>该项目为大学生创新创业项目《基于医学图像的传染病辅助诊断的研究与流行范围可视化——以COVID-19为例》的系统实现
项目团队对本项目保有著作权

## 演示视频
位于项目的photos/display.mp4中，由于github不支持在readme中嵌入视频，故无法在当前页面中显示，需要自取。

## 快速开始
克隆项目
```
git clone https://github.com/yccye/Auxiliary-diagnosis-system.git
```

安装第三方包
``` 
pip install -r requirements.txt
```

## 项目结构说明
```
    |--CTAI_web_new
        |--chat                 //医患沟通模块
            |--...
        |--CTAI_web_new         //项目配置模块
            |--__init__.py
            |--asgi.py
            |--routing.py
            |--settings.py
            |--urls.py
            |--wsgi.py
        |--diagnosis            //诊断模块（CT图像上传和结果展示）
            |--...
        |--epidemic_map         //疫情流行可视化模块
            |--...
        |--login                //登录模块
            |--...              
        |--media                //用于保存上传文件（CT图片）
            |--...              
        |--static               //静态资源文件夹
            |--...
        |--logs                 //日志文件夹
            |--...
        |--templates            //前端模板文件夹
            |--...
        |--.gitignore           
        |--LICENSE      
        |--manage.py            
        |--README.md
        |--requirements.txt 
```

## 相关环境或技术
```
    1、python3.6
    2、redis
    3、mysql
```

## 各页面功能及使用

### 登录页面

可登录进入系统或是点击“注册”进入注册页面
![展示-登录页面](./photos/login.png '登录页面')

### 注册页面

可以注册并直接登录或是选择登录已有账号
![展示-注册页面](./photos/signup.png '注册页面')

### 首页

欢迎界面
![展示-首页页面](./photos/index.png '首页')

### 诊断页面

提供文件上传接口
![展示-图片上传页面](./photos/pic_upload.png '图片上传')

点击该区域或拖拽图片实现文件上传
![展示-图片上传页面](./photos/pic_upload2.png '图片上传')

跳转至图像诊断结果详情
![展示-图片上传页面](./photos/photo_segment.png '图片上传')

检测结果展示
![展示-诊断结果页面](./photos/result.png '诊断结果')

点击“复制链接”按钮，可实现诊断结果链接的复制
![展示-诊断结果页面](./photos/link_copy.png '复制链接')

### 疫情可视化

感染人员轨迹图
![展示-疫情地图页面](./photos/map.png '疫情地图')

可点击左侧齿轮图标唤起坐标上传窗口,进行坐标上传
![展示-疫情地图页面](./photos/position_upload.png '坐标上传')


### 医患聊天页面

点击左侧侧边栏图标切换好友框以及最近聊天框

好友框
![展示-聊天室](./photos/chat_index2.png '聊天室')

最近聊天框
![展示-聊天室](./photos/chat_index3.png '聊天室')

---

点击好友或最近聊天可进入聊天室（左上角可显示对方是否在聊天室内）
![展示-聊天室](./photos/chat_room.png '聊天室')

可发送消息
![展示-聊天室](./photos/chat_room2.png '聊天室')

此时对方可在聊天页面中接收到未读消息提醒
![展示-聊天室](./photos/chat_room3.png '聊天室')

点击进入可看到相应消息
![展示-聊天室](./photos/chat_room4.png '聊天室')

点击右下角 转圈圈 图标，可查询历史消息
![展示-聊天室](./photos/chat_room5.png '聊天室')
![展示-聊天室](./photos/chat_room6.png '聊天室')

若信息为链接点击信息框左侧三点，再点击”访问链接“即可跳转页面
![展示-诊断结果页面](./photos/link_visit.png '复制链接')
![展示-诊断结果页面](./photos/link_visit2.png '复制链接')








