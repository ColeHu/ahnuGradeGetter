import requests
import re
import json
import hashlib
import getpass
import warnings

warnings.filterwarnings('ignore')

url = "http://jw.ahnu.edu.cn/student/login"     # 安徽师范大学新教务系统地址
loginSaltUrl = "http://jw.ahnu.edu.cn/student/login-salt"        # 获取教务系统密码加盐url
homeUrl = "http://jw.ahnu.edu.cn/student/home"  #主页url
checkUrl = "http://jw.ahnu.edu.cn/student/login"        # 登录提交url
scoreUrl = "https://jw.ahnu.edu.cn/student/for-std/grade/sheet/info/" # 成绩表url

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}

headers_content_json = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    "Content-Type": "application/json",
}  # json类型内容

headers_content_xml = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}  # xml request

def login(username, password):

    loginSalt = req.get(loginSaltUrl, headers=headers, verify=False).content.decode('utf-8') #获得密码加密代码

    passwordSalt = loginSalt + '-' + password
    passwordPost = hashlib.sha1(passwordSalt.encode('utf-8')).hexdigest()

    data={
        "username": username,   #用户名
        "password": passwordPost,   #密码
        "captcha": "",  #验证码，默认无
        "terminal": "student" #登录端
    }

    response = req.post(checkUrl, data=json.dumps(data), headers=headers_content_json, verify=False).content.decode('utf-8')


    try:
        print("exception", json.loads(response)["exception"])
        print("message", json.loads(response)["message"])
    except:  # 获取失败
        result = json.loads(response)
        if result.get("result", None):
            print("登录成功")
        else:
            print("登录失败, message: {}".format(result.get("message", None)))
            exit(1)

def getScore():

    s1 = req.get('https://jw.ahnu.edu.cn/student/for-std/grade/sheet', headers=headers_content_xml, verify=False)
    stuNum = s1.url[-6:]    #获取唯一标识码
    checkUrl = scoreUrl + stuNum + '?' + "semester=" + str(semester)    #产生成绩单链接
    scorePage = req.get(checkUrl, headers=headers_content_xml, verify=False).content.decode('utf-8')
    scoreJSON = json.loads(scorePage)
    return scoreJSON['semesterId2studentGrades'][semester]


def praseScore(courses):

    scores = []
    print("本学期成绩如下：")
    for course in courses:
        print(course['course']['nameZh'] + '\t' + "总分：" + str(course['gaGrade']) + " \t绩点：" + str(course['gp']))


if __name__ == '__main__':
    username = input("学号: ")
    password = getpass.getpass("密码(已隐藏): ")
    semester = input("请输入要查询的学期:")
    req = requests.session()
    login(username, password)
    praseScore(getScore())
    print()


