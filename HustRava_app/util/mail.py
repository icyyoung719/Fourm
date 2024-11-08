import smtplib
from email.mime.text import MIMEText

def send_mail(to_addr, subject, body):
    send_mail_full('1523231052', 'xqlzabovkigufjig', '1523231052@qq.com', to_addr, subject, body)




def send_mail_full(username, pwd, from_addr, to_addr, subject, body):
    try:
        message = MIMEText(body, 'plain', 'utf-8')

        message['From'] = from_addr
        message['To'] = to_addr
        message['Subject'] = subject

        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(username, pwd)
        smtp.sendmail(from_addr, to_addr, message.as_string())

        smtp.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"Error: {str(e)}")

# # 配置邮件参数
# username = '1523231052'
# pwd = 'xqlzabovkigufjig'
# from_addr = '1523231052@qq.com'
# to_addr = '1073182632@qq.com'
# subject = '测试邮件'    #邮件主题
# body = 'Python 邮件发送测试'   #邮件正文
#
# # 调用发送函数
# send_mail_full(username, pwd, from_addr, to_addr, subject, body)