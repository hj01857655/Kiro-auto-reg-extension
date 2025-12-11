# GPTMail API 文档

## 基本信息

- **Base URL**: `https://mail.chatgpt.org.uk`
- **认证方式**: Referer 头验证（必须带 `Referer: https://mail.chatgpt.org.uk/`）
- **SSL**: 需要禁用 SSL 验证（`verify=False`）

## 请求头

```python
HEADERS = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'referer': 'https://mail.chatgpt.org.uk/',
    'origin': 'https://mail.chatgpt.org.uk'
}
```

## API 端点

### 1. 生成随机邮箱

**GET** `/api/generate-email`

**响应**:
```json
{
  "success": true,
  "data": {
    "email": "fd298aa5@teamnewmexico.org"
  }
}
```

### 2. 生成自定义前缀邮箱

**POST** `/api/generate-email`

**请求体**:
```json
{
  "prefix": "mytest"
}
```

**响应**:
```json
{
  "success": true,
  "data": {
    "email": "mytest@gxgukuang.asia"
  }
}
```

### 3. 获取邮件列表

**GET** `/api/emails?email={email}`

**参数**:
- `email`: 邮箱地址（URL 编码）

**响应**:
```json
{
  "success": true,
  "data": {
    "emails": [
      {
        "id": "unique-id",
        "from_address": "sender@example.com",
        "subject": "邮件主题",
        "content": "纯文本内容",
        "html_content": "<html>...</html>",
        "timestamp": 1736500000
      }
    ],
    "count": 1
  }
}
```

### 4. 获取单封邮件详情

**GET** `/api/email/{id}`

**响应**:
```json
{
  "success": true,
  "data": {
    "id": "unique-id",
    "from_address": "sender@example.com",
    "subject": "邮件主题",
    "content": "纯文本内容",
    "html_content": "<html>...</html>",
    "timestamp": 1736500000
  }
}
```

### 5. 删除单封邮件

**DELETE** `/api/email/{id}`

**响应（成功）**:
```json
{
  "success": true
}
```

**响应（邮件不存在）**:
```json
{
  "success": false,
  "error": "Email not found"
}
```

### 6. 清空邮箱

**DELETE** `/api/emails/clear?email={email}`

**参数**:
- `email`: 邮箱地址（URL 编码）

**响应**:
```json
{
  "success": true,
  "data": {
    "count": 5,
    "message": "Deleted 5 emails"
  }
}
```

## 邮件数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 邮件唯一 ID |
| from_address | string | 发件人地址 |
| subject | string | 邮件主题 |
| content | string | 纯文本内容 |
| html_content | string | HTML 内容 |
| timestamp | int | Unix 时间戳 |

## 限制

- 邮件保存时间: 7 天
- 自动刷新间隔: 30 秒
- 前缀长度: 1-32 字符
- 允许字符: `[a-zA-Z0-9._-]`

## Python 示例

```python
import requests
import urllib3

urllib3.disable_warnings()

BASE_URL = 'https://mail.chatgpt.org.uk'
HEADERS = {
    'accept': 'application/json',
    'referer': 'https://mail.chatgpt.org.uk/',
    'user-agent': 'Mozilla/5.0'
}

# 生成邮箱
resp = requests.get(f'{BASE_URL}/api/generate-email', headers=HEADERS, verify=False)
email = resp.json()['data']['email']

# 获取邮件
resp = requests.get(f'{BASE_URL}/api/emails', params={'email': email}, headers=HEADERS, verify=False)
emails = resp.json()['data']['emails']

# 删除单封邮件
email_id = emails[0]['id']
resp = requests.delete(f'{BASE_URL}/api/email/{email_id}', headers=HEADERS, verify=False)

# 清空邮箱
resp = requests.delete(f'{BASE_URL}/api/emails/clear', params={'email': email}, headers=HEADERS, verify=False)
```
