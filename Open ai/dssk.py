import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "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",
    "Content-Type": "application/json",
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  data=json.dumps({
    "model": "deepseek/deepseek-v3-base:free",
    "messages": [
      {
        "role": "user",
        "content": "Hello?"
      }
    ],
    
  })
)