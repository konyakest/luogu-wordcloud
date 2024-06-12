# luogu-wordcloud
从 luogu 提交记录爬取代码，并生成词云

## 安装

```bash
git clone https://github.com/konyakest/luogu-wordcloud.git
cd luogu-wordcloud/
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用

首先，需要填写 ``configs.json``

最简单的 ``configs.json`` 如下：

```json
{
    "spider_configs": {
        "uid": 482660,
        "client_id": "xxxxxxxxxxxxxxx"
    }
}
```

然后运行 ``python3 spider.py`` 和 ``python3 cloud.py`` 即可生成词云

## 选项

提供了以下额外选项：

``spider_configs`` 中：

- ``difficulties``：选择的题目的难度范围，例如 "``012``" 表示选择“灰，红，橙”，默认为“``567``”（“蓝，紫，黑”）
- ``person_uid``：指定要爬取的用户的用户名，默认为 ``uid`` 的值
- ``save_files``：是否保存爬取到的代码，默认为 ``false``
- ``files_dir_name``：将代码保存在哪个文件夹下
- ``sample_count``：从题目中随机选择若干道题进行爬取，不填表示选择全部

``cloud_configs`` 中：

- ``output_size``：输出的图片的长宽，默认为 1000
- ``output_file``：输出的图片文件名，默认为 ``wordcloud.png``
- ``background_color``：背景颜色，默认为 ``white``
- ``ignore_words``：去掉这些关键词

具体用法可参见 ``all_configs.json``
