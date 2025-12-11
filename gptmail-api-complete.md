# GPTMail 临时邮箱服务 API 完整分析

## 服务概述
- **网站**: https://mail.chatgpt.org.uk/
- **基础设施**: Cloudflare Workers
- **支持语言**: 8种语言（中文、英文、日语、韩语、德语、法语、西班牙语）

## 核心 API 接口

### 1. 生成随机邮箱
**端点**: `/api/generate-email`
**方法**: GET
**响应示例**:
```json
{
  "email": "rbauy1ft@cketrust.org"
}
```

### 2. 生成自定义邮箱
**端点**: `/api/custom-email`
**方法**: POST
**请求头**:
```
Content-Type: application/json
```
**请求体**:
```json
{
  "prefix": "mytest"
}
```
**验证规则**:
- 正则表达式: `/^[a-zA-Z0-9._-]{1,32}$/`
- 允许字符: 字母、数字、点(.)、下划线(_)、短横线(-)
- 长度限制: 1-32字符

**响应示例**:
```json
{
  "email": "mytest@cketrust.org"
}
```
**错误响应**:
```json
{
  "error": "Invalid prefix format"
}
```

### 3. 获取邮件列表
**端点**: `/api/get-emails`
**方法**: GET
**参数**:
- `email`: 邮箱地址（需要URL编码）

**请求示例**:
```
GET /api/get-emails?email=rbauy1ft%40cketrust.org
```

**响应示例（无邮件）**:
```json
{
  "emails": []
}
```

**响应示例（有邮件）**:
```json
{
  "emails": [
    {
      "id": "unique-email-id",
      "from": "sender@example.com",
      "to": "rbauy1ft@cketrust.org",
      "subject": "邮件主题",
      "timestamp": "2025-01-10T14:00:00Z",
      "hasHtml": true,
      "htmlContent": "<html>...</html>",
      "textContent": "纯文本内容",
      "attachments": []
    }
  ]
}
```

### 4. 删除单个邮件
**端点**: `/api/delete-email`
**方法**: POST
**请求头**:
```
Content-Type: application/json
```
**请求体**:
```json
{
  "email": "rbauy1ft@cketrust.org",
  "id": "unique-email-id"
}
```
**响应**:
```json
{
  "success": true
}
```

### 5. 清空邮箱（删除所有邮件）
**端点**: `/api/clear-inbox`
**方法**: POST
**请求头**:
```
Content-Type: application/json
```
**请求体**:
```json
{
  "email": "rbauy1ft@cketrust.org"
}
```
**响应**:
```json
{
  "success": true,
  "deleted": 5  // 删除的邮件数量
}
```

## 邮件数据结构

### Email对象
```javascript
{
  "id": "string",           // 邮件唯一ID
  "from": "string",         // 发件人邮箱
  "to": "string",          // 收件人邮箱
  "subject": "string",     // 邮件主题
  "timestamp": "string",   // ISO 8601格式时间戳
  "hasHtml": "boolean",    // 是否包含HTML内容
  "htmlContent": "string", // HTML内容（如果有）
  "textContent": "string", // 纯文本内容
  "headers": {            // 邮件头信息
    "date": "string",
    "message-id": "string",
    "content-type": "string"
  },
  "attachments": []       // 附件列表（当前版本支持有限）
}
```

## 特殊功能

### 1. URL直接访问邮箱
可以通过URL直接访问特定邮箱的收件箱：
```
https://mail.chatgpt.org.uk/{email}
```
例如：
```
https://mail.chatgpt.org.uk/test@cketrust.org
```

### 2. 自动刷新机制
- 默认间隔: 30秒
- 实现方式: 轮询 `/api/get-emails` 接口
- JavaScript函数: `startAutoRefresh()` / `stopAutoRefresh()`

### 3. 本地存储
使用 `localStorage` 存储当前邮箱：
```javascript
localStorage.setItem('currentEmail', 'test@cketrust.org');
```

## 支持的域名列表
根据观察，服务支持多个域名，包括但不限于：
- @cketrust.org
- @cephastrust.org
- 其他域名（系统自动轮询分配）

## JavaScript 函数接口

### 前端主要函数
```javascript
// 生成随机邮箱
generateRandomEmail()

// 生成自定义邮箱
generateCustomEmail()

// 加载邮件列表
loadEmails(forceUpdate)

// 删除单个邮件
deleteEmail(emailId)

// 清空所有邮件
deleteAllEmails()

// 复制邮箱到剪贴板
copyEmailToClipboard()

// 刷新邮件
refreshEmails()

// 切换自定义输入界面
toggleCustomInput()
```

## 安全和限制

### 限制条件
- 邮箱前缀: 1-32字符
- 邮件保存时间: 1天（24小时）
- 自动刷新间隔: 30秒
- 支持的字符: `[a-zA-Z0-9._-]`

### 安全特性
- 全程HTTPS加密
- Cloudflare保护
- 无需注册
- 临时存储
- 自动清理机制

## HTTP响应状态码
- `200`: 成功
- `400`: 请求参数错误
- `404`: 邮箱或邮件不存在
- `500`: 服务器内部错误

## CORS配置
服务支持跨域请求，适合作为API服务使用。

## 使用建议
1. 使用随机生成的邮箱以避免冲突
2. 定期轮询获取新邮件（建议间隔30秒以上）
3. 及时保存重要信息（邮件1天后自动删除）
4. 不要用于接收敏感信息

## 更新记录
- 2025-01-10: 完整API分析
- 基于网站实际测试和网络请求分析