import resend

resend.api_key = "re_XztCc3fS_E4zFq8VdDHj9deDr9SW8KNEs"

params: resend.Emails.SendParams = {
  "from": "果园编程 <yun@xuzhoulab.cn>",
  "to": ["admin@xuzhoulab.cn"],
  "subject": "您的邮件收到影响",
  "html": "<p>您的邮件收到影响</p>"
}

email = resend.Emails.send(params)
print(email)