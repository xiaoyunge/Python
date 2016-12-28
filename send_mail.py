# -*- coding:utf-8 -*-
# 使用smtplib和email模块发送邮件，可以群发邮件，也可以添加多个附件

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders

# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject="", text="", files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro                # 注意：邮件的发件人(这里并不是真正发件人，是收到邮件显示的发件人，你想到了什么？？)
    msg['Subject'] = subject         # 邮件的主题
    msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
    msg['Date'] = formatdate(localtime=True) # 发送时间，当不设定时，用outlook收邮件会不显示日期，QQ网页邮箱会显示日期
    # MIMIMEText有三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码，二和三可以省略不写
    msg.attach(MIMEText(text,'plain','utf-8'))

    for file in files:          # 添加附件可以是多个，files是一个列表，可以为空
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data
        with open(file,'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(server['name']) # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
    smtp.login(server['user'], server['passwd']) # 用户名，密码
    smtp.sendmail(fro, to, msg.as_string()) # 发件人，收件人，发送信息(这里的发件人和收件人才是真正的发件人和收件人)
    smtp.close()  # 关闭连接

text = '''
   呵呵哒
   test'''
send_mail({'name':'xxx','user':'oooo','passwd':'xxxooo'},
          'xxx',
          ['xo','ox'],
          '呵呵哒01',
          text)
