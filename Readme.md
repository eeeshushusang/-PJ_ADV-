# 视觉小说评价系统
一. 表结构设计:
    ADV信息表：包含ADV的ID、书名、制作社团、发行日期、发售平台、价格、评价(分数)等字段。
    购买信息表：包含购买编码、ADV的ID、ADV的书名、购买日期。
    客户信息表：包含购买编码、姓名、性别、评价(分数+字)、购买过的ADV等字段。
    社团信息表：包含名字、制作的adv、创立时间、评分(根据作品加权评分)
二. 基本功能要求:
    ADV入库、信息修改和删除。
    客户买ADV和评价ADV。
    查询ADV信息和评价。
    查询社团有哪些作品，社团评价

项目网页：
http://49.235.184.91/index/
http://www.adv.xn--6qq986b3xl/index/
项目github:
https://github.com/eeeshushusang/-PJ_ADV-

## 后端：
galgame信息：
wiki;CNGAL;DLsite;Steam;

## 前端：
live2d最简单的抄法：
https://github.com/stevenjoezhang/live2d-widget
登陆,注册，上传信息等页面样式参考：
https://www.bilibili.com/video/BV1X3411y7of/?spm_id_from=333.880.my_history.page.click&vd_source=efbe71818b8135cefb115ae13d27eec1
山羊鼠标样式：
https://www.bilibili.com/video/BV1wb4y1a7uQ/?spm_id_from=333.880.my_history.page.click

### 图片：
-    全局背景图：Anmi
-    部分网页框内背景：Weri

### 音乐：
-    首页，上传信息页： MANYO,三輪学 - 黑猫さんの背伸び
-    橘子班/高考恋爱100天：Days - Nuit Silencieuse    
-    AliceSoft：アリスソフト - かわいいのでてきた
       兰斯10：アリスソフト - the end
       兰斯7 战国兰斯：アリスソフト - My Glorious Days
-    Leaf:上原れな - 届かない恋 (Instrumental)
        白色相簿1：石川真也 - FILL YOU
        白色相簿2：石川真也 - あの頃のように
-    枕社：松本文紀 - 夜の向日葵
        樱之诗：松本文紀 - 夢の歩みを見上げて
        樱之刻：松本文紀 - 櫻ノ詩 -2023Mix inst ver-
-    Key社：麻枝准,Key Sounds Label - 渚
        Summer Pockets:麻枝准 - Sea, You & Me
        Clannad:麻枝准 - 同じ高みへ

### 部署上线：   
    腾讯云：服务器(学生折扣)10r/月;域名：首年10元(便宜的中文域名)
    使用nginx绕过域名报备进行上线。麻烦的一批。

### 后续跟进计划：
- live2d，本打算从BA中扣一个乐队爱丽的小人模型下来，结果发现不会用相关库，不了了之。
- 音乐未实现，同一曲目在不同网页播放时，继承上个网页的播放进度
- 鼠标特效可以做的更好看点