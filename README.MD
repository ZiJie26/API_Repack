# API RePack项目说明

## 概述

本项目基于Python，仅作为求职作品用于演示Flask和Requests对API进行二次封装的代码思路。使用<https://picwish.cn/face-cutout>这一网页端脸部抠图功能作为示例。

本示例功能的接口PicWish官方开发者文档并未提供，由本人利用抓包工具获取。同时项目中提供了PicWish官方开发者文档有提供的黑白图像上色接口colorization作为对比

### 思路

本项目以一个完整的：登录获取Token-使用Token上传图片到PicWish的阿里云OSS并回调取得对应ID-使用ID获取图片处理结果 的三步走过程。

当然也可实现仅提供登录账号和密码以及图片，就一步直接获取结果，无非是把这三个接口对应的三个类合并成一个类。只是为方便展示思路，我将其分成了三个接口。分别对应 鉴权 - 上传 - 获取结果

### 快速开始

1. 该项目基于Python 3.10，可使用`pip install -r requirements.txt`快速部署环境
2. 找到`main.py`并运行
3. 使用postman或其他工具请求文档中的接口

### 注意

- 本项目所有请求Body类型均为**form-data**。
- 本项目所有图片文件上传的key均命名为`image_file`，后续文档以**img.png**作为**示例文件**在。
- 使用Postman上传文件，需先在Body选择类型为form-data，然后**在Key右边选择file类型，上传文件**

## 授权token（公共header）

在postman中headers添加authorization，然后填上使用登录接口获取的Bearer token。

> 注： 如果遇到401错误，表示token已失效，需重新抓取。

```text
"Failed to create task,{\"status\":401,\"message\":\"needed login\"}"
```

### 获取方法：

1. 注册并登陆：<https://picwish.cn/>
2. 进入个人中心修改密码，并记下手机号和密码
3. 使用postman请求`/picwish/login`接口即可获得Bearer token,具体请求参数请查看下文的“**登录接口**”

## 登录接口

PicWish登录接口，用于获取OSS上传所需的Token，仅暴露入参手机号和密码，出餐token

### 接口地址

http://127.0.0.1:80/picwish/login

请求方法： POST

> 如果本地80端口被占用，或者权限不足，都有可能导致程序启动失败，请修改`main.py`中的端口号.

### 请求参数

在postman的body中，选择form-data，然后输入账号密码键值对：

| 参数        | 类型   | 必须 | 示例         |
|:----------|:-----|:---|:-----------|
| telephone | Text | 是  | 153XXXXXXX |
| password  | Text | 是  | 123456     |

### 返回参数

```json
{
  "api_token": "Bearer v2,some,token,number"
}
```

## 阿里云OSS图片上传接口

PicWish所使用的阿里云OSS上传接口，由创建储存空间和PutObject修改文件两个接口组成，借助阿里云的SDK：oss2来完成Authorization
Header签名的计算步骤和PutObject以及回调步骤。手动隐藏了不必要的参数，仅暴露必要参数图片文件

### 接口地址

http://127.0.0.1:80/picwish/oss-img

请求方法： POST

### 请求参数

headers：使用`/picwish/login`接口所获得的Bearer token

Body：form-data

| 参数         | 类型   | 必须 | 示例      |
|:-----------|:-----|:---|:--------|
| image_file | File | 是  | img.png |

### 返回参数

图片的文件ID，用于作为其他功能的入参。

```json
{
  "resource_id": "a-long-resource-id"
}
```

## AI脸部抠图接口

PicWish网页端功能，实现对人像或动物图进行抠图，使其仅保留脸部。

由两个接口组合而成
1. 上传图像并创建任务，返回任务ID
2. 使用任务ID发送GET请求获取图像处理结果

网页端利用这两个接口实现异步操作，本项目模拟该异步操作，整个接口逻辑为先请求接口1，再使用获取的任务ID以1秒的间隔不断请求接口2直至获取结果。

当然经过二次封装后暴露出来的仅为传入resource id然后得到图片这样的同步操作。

### 接口地址

http://127.0.0.1:80/picwish/face-cutout

请求方法： POST

### 请求参数

headers：使用`/picwish/login`接口所获得的Bearer token

Body：form-data

| 参数          | 类型   | 必须 | 示例                            |
|:------------|:-----|:---|:------------------------------|
| resource_id | Text | 是  | XXXX-XXXX-XXXX-XXX-XXXXXXXXXX |

### 返回参数

图片下载地址：

```json
{
  "image": "a-img-download-url"
}
```

## AI黑白图像上色接口

PicWish开发者文档提供的接口，实现通过AI使黑白图像变为彩色图像。需要开发者API-KEY

### 接口地址

http://127.0.0.1:80/picwish/colorization

请求方法： POST

### 请求参数

headers：PicWish 提供给开发者的API-KEY

Body：form-data

| 参数         | 类型   | 必须                | 示例                  |
|:-----------|:-----|:------------------|:--------------------|
| image_url  | Text | 是（与image_file二选一） | https://img/url.png |
| image_file | File | 是（与image_url二选一）  | img.png             |

### 返回参数

图片下载地址：

```json
{
  "image": "a-img-download-url"
}
```


