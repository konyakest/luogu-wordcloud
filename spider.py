from urllib.parse import unquote
from requests import get
from json import load, loads, dumps
from time import sleep
from random import sample
from os import mkdir
import re

CONFIGS = load(open("configs.json"))["spider_configs"]
CLIENT_ID = CONFIGS["client_id"]
UID = CONFIGS["uid"]
PERSON_UID = CONFIGS.get("person_uid", UID)


def luogu_get(url):
    content = get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": f"__client_id={CLIENT_ID};_uid={UID}"
        }
    ).content.decode().split("JSON.parse(decodeURIComponent(\"")[1].split("\"));window.")[0]
    return loads(unquote(content))["currentData"]


def get_problems():
    return [i["pid"]
            for i in luogu_get(
            f"https://www.luogu.com.cn/user/{PERSON_UID}#practice"
            )["passedProblems"]
            if str(i["difficulty"]) in CONFIGS.get("difficulties", "567")
            ]


if CONFIGS.get("save_files", False):
    try:
        mkdir(CONFIGS.get("files_dir_name", "codes"))
    except FileExistsError:
        pass

print("正在获取题目列表")

words = {}
cnt = 1
problems = get_problems()

if "sample_count" in CONFIGS and CONFIGS["sample_count"] < len(problems):
    problems = sample(problems, CONFIGS["sample_count"])

total = len(problems)


def show():
    lst = [i for i in words.items()]
    lst.sort(key=lambda x: x[1], reverse=True)
    return lst


for problem_id in problems:
    print(f"{cnt}/{total} ({cnt/(total)*100:.2f}%): 正在爬取 {problem_id}")
    try:
        id = luogu_get(
            f"https://www.luogu.com.cn/record/list?pid={problem_id}&\
            user={PERSON_UID}&status=12&page=1",
        )["records"]["result"][0]["id"]

        content = luogu_get(
            f"https://www.luogu.com.cn/record/{id}",
        )["record"]["sourceCode"]

        for word in re.findall("\w+", content):
            words[word] = words.get(word, 0) + 1

        if CONFIGS.get("save_files", False):
            open(f"{CONFIGS.get('files_dir_name', 'codes')}/{problem_id}.cpp",
                "w").write(content)

        print(f"{id} 爬取完毕！")
    except:
        print(f"{id} 爬取失败！")

    sleep(1)
    cnt += 1

    if cnt % 10 == 0:
        print("保存成功！")
        open("data.json", "w").write(dumps(show()))


open("data.json", "w").write(dumps(show()))
