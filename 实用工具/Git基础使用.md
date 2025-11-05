# Git 基础使用

Git 是一个分布式版本控制系统，用于跟踪文件变更

```
graph TB
    A[工作区] --> B[暂存区]
    B --> C[本地仓库]
    C --> D[远程仓库]
    
    A -->|git add| B
    B -->|git commit| C
    C -->|git push| D
    D -->|git pull| A
```

## 基础配置

```shell
# 设置用户信息
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱@example.com"

# 查看配置
git config --list
```

## 基础使用

```shell
# 查看仓库状态
git status

# 添加文件到暂存区
git add filename.txt          # 添加特定文件
git add .                     # 添加所有文件
git add *.java               # 添加所有Java文件

# 提交更改
git commit -m "提交描述信息"

# 查看提交历史
git log
git log --oneline            # 简洁显示
git log --graph              # 图形化显示
```

## 撤销和回退操作

撤销工作区修改(已修改，未暂存)
```shell
git checkout . # 撤销当前文件夹下所有的修改

# 撤销特定类型文件
git checkout src/test

git clean -f # untracked状态，撤销新增的文件
git clean -df # untracked状态，撤销新增的文件和文件夹
```

撤销暂存区的修改(已暂存，未提交)
```shell
# 移除所有暂存的文件
git reset HEAD

# 移除特定类型的文件
git reset HEAD *.log
git reset HEAD src/test/
```

撤销本地仓库的修改(已提交，未推送)
```shell
# 回退到特定提交(丢弃)
git reset --soft HEAD^      # 回退提交但保留更改
git reset --hard HEAD^      # 回退到本地仓库上一个版本
git reset --hard commit_id  # 回退到本地仓库特定提交

# 撤销提交(保留所有提交记录) 推荐
git revert commit_id
```

撤销远程仓库的修改(已推送)
```shell
# 强制推送(不推荐)
git push -f

# 推荐1 git revert
# 推荐2 git reset组合
git reset --hard old_commit
git reset --soft new_commit
git add .
git commit -m "回滚指定提交"
git push
```

## 分支管理

```shell
# 查看分支
git branch                   # 本地分支
git branch -a                # 所有分支（包括远程）

# 创建分支
git branch new-feature       # 创建分支
git checkout new-feature     # 切换到分支
git checkout -b new-feature  # 创建并切换分支

# 合并分支
git checkout main
git merge new-feature

# 删除分支
git branch -d new-feature    # 删除已合并的分支
git branch -D hotfix         # 强制删除分支
```