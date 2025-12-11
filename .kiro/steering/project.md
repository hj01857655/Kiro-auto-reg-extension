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

## 发布流程
1. 确保代码在 `dev` 分支
2. 合并到 `master`
3. 打 tag：`git tag v{版本号}`
4. 推送 tag：`git push dev v{版本号}`
5. GitHub Actions 自动构建并创建 Release

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
