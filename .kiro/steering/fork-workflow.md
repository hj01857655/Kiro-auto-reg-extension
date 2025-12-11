# Fork 仓库工作流规范

## Remote 命名
- `dev` - 自己的 fork 仓库（有推送权限）
- `upstream` - 原始仓库（只读，用于同步）

## 分支策略
- `master` - 主分支，保持与 upstream 同步
- `feature/*` - 功能分支，从 master 创建

## 同步流程
```bash
# 1. 获取 upstream 更新
git fetch upstream

# 2. 切到 master 合并
git checkout master
git merge upstream/master

# 3. 推送到自己的仓库
git push dev master

# 4. rebase 功能分支
git checkout feature/xxx
git rebase master
```

## 提交规范
- 功能分支开发完成后推送到 dev
- 不直接推送到 upstream
- 通过 PR 贡献代码到原仓库

## 冲突处理
- 优先保留 upstream 的改动（`--theirs`）
- 除非有明确理由保留自己的改动
