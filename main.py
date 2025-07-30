import requests, json, re, os

session = requests.session()
# 配置用户名（一般是邮箱）
# email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
# passwd = os.environ.get('PASSWD')
# 从设置的环境变量中的Variables多个邮箱和密码 ,分割
emails = os.environ.get('EMAIL', '').split(',')
passwords = os.environ.get('PASSWD', '').split(',')
#print("邮箱地址: \t",emails)
# server酱
SCKEY = os.environ.get('SCKEY')
# PUSHPLUS
Token = os.environ.get('TOKEN')



path = "https://ikuuu.org/"
#获取剩余流量的请求路径
user_url = path + 'user'


def push(content):
    if SCKEY != '1':
        url = "https://sctapi.ftqq.com/{}.send?title={}&desp={}".format(SCKEY, 'ikuuu签到', content)
        requests.post(url)
        print('推送完成')
    elif Token != '1':
        headers = {'Content-Type': 'application/json'}
        json = {"token": Token, 'title': 'ikuuu签到', 'content': content, "template": "json"}
        resp = requests.post(f'http://www.pushplus.plus/send', json=json, headers=headers).json()
        print('push+推送成功' if resp['code'] == 200 else 'push+推送失败')
    else:
        print('未使用消息推送推送！')

# 会不定时更新域名，记得Sync fork

login_url = path + 'auth/login'
check_url = path + 'user/checkin'
info_url = path + 'user/profile'

header = {
        'origin': 'https://ikuuu.one',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
res = ''
for email, passwd in zip(emails, passwords):
    session = requests.session()
    data = {
        'email': email,
        'passwd': passwd
    }
    try:
        print(f'[{email}] 进行登录...')
        response = json.loads(session.post(url=login_url,headers=header,data=data).text)
        print(response['msg'])
        # 获取之前的流量
        remain_html = session.get(url=user_url,headers=header).text
        #之前剩余流量
        remain = re.findall('<span class="counter">(.*?)</span>" GB "', remain_html, re.S);
        # 进行签到
        result = json.loads(session.post(url=check_url,headers=header).text)
        print(result['msg'])
        content = result['msg']
        #签到后获取剩余总流量
        total_html = session.get(url = user_url,headers = header).text;
        total = re.findall('<span class="counter">(.*?)</span> GB', total_html, re.S);
        # 进行推送
        content = email + '\n签到前剩余总流量: ' + (remain[0] if len(remain) > 0 else "NULL ") + 'GB\n' + content + '\n当前剩余总流量: ' + (total[0] if len(total) > 0 else "NULL ") + 'GB\n';
        #push(content)
        res += content
    except:
        total_html = session.get(url = user_url,headers = header).text;
        total = re.findall('<span class="counter">(.*?)</span> GB', total_html, re.S);
        print(email,passwd)
        content = email + ' 签到失败' + ',当前剩余总流量: ' + (total[0] if len(total) > 0 else "NULL ")  + "GB\n" 
        print(content);
        #push(content);
        res += content

#最后统一推送
push(res)
