import resend

resend.api_key = "re_au54eMHk_CQx3hJi5zKbWkfkDAJ2Xn8i6"

params: resend.Emails.SendParams = {
  "from": "果园编程 <admin@guoyuangzs.dpdns.org>",
  "to": ["guoyuan@guoyuangzs.dpdns.org"],
  "subject": "他工作了呢！",
  "html": "<p>他工作了</p>"
}

email = resend.Emails.send(params)
print(email)