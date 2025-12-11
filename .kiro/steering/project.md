---
inclusion: always
---

# 项目规范

## 项目结构
```
├── src/                # TypeScript 插件源码
├── autoreg/            # Python 自动注册脚本
├── docs/               # API 文档
├── tests/              # 测试文件
└── dist/               # 构建输出（gitignore）
```

## 构建命令
| 命令 | 用途 |
|------|------|
| `npm run build` | 编译 TypeScript |
| `npm run package` | 打包 VSIX 插件 |
| `npm run lint` | TypeScript 类型检查 |

## CI/CD 流程

### 推送到 dev 分支
- 自动触发 workflow 打包
- 生成 artifact（可在 Actions 页面下载）
- 不创建 Release

### 创建 Release
1. 打 tag：`git tag v{版本号}`
2. 推送 tag：`git push dev v{版本号}`
3. GitHub Actions 自动构建并创建 Release

### 发布失败后清理
发布失败时，必须按顺序清理后才能重新发布：
1. 删除远程 tag：`git push dev --delete v{版本号}`
2. 删除本地 tag：`git tag -d v{版本号}`
3. 删除 GitHub Release（如有）
4. 修复问题后重新打 tag 发布

## autoreg 模块
- 邮件服务：GPTMail 临时邮箱（无需配置 IMAP）
- 入口文件：`autoreg/registration/register.py`
- 邮件处理：`autoreg/registration/gptmail_handler.py`

## 注意事项
- `~/.kiro-autoreg` 目录优先级高于插件自带，开发时注意清理
- Python 脚本修改后需重新打包插件才能生效

## 同步记录
| 日期 | upstream 版本 | 说明 |
|------|---------------|------|
| 2024-12-11 | v4.6.0 (cfc1df2) | UI 改进、headless 修复、Linux OAuth 支持 |
