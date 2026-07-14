git checkout -b feature/crawler-v2
git switch -c feature/crawler-v2
git switch main
git merge feature/crawler-v2
git branch -d feature/crawler-v2

git worktree add ../ai-space-dev feature/crawler-v2
git worktree add -b feature/crawler ../ai-space-dev
git worktree list

git branch feature/crawler


rm -rf ai-space-dev
git worktree prune

git worktree remove ../ai-space-dev

commit
stash
或放弃修改


① 基础
git init
git clone
git status
git log

② 日常开发
git add
git commit
git push
git pull

③ 分支
git switch
git branch
git merge
git rebase

④ Worktree
git worktree add
git worktree list
git worktree remove

⑤ 撤销
git restore
git reset
git revert

⑥ 查看差异
git diff

# 重点
git restore .
git stash
git stash pop
git stash apply
git stash drop

git rebase
重新排列 commit。或者把多个 commit 压缩成一个

git rebase -i HEAD~3
pick 改成edit
git add .
git commit --amend
git rebase --continue

git diff
git diff --cached
git diff HEAD
git show <commit-id>
git diff commit1 commit2

git cherry-pick
只拿一个 commit。不是整个分支
git cherry-pick C的commit-id
|           | merge  | cherry-pick  |
| --------- | ------ | ------------ |
| 目标        | 合并整个分支 | 拿一个或几个commit |
| 历史        | 保留分叉   | 复制修改         |
| commit id | 保持     | 重新生成         |
| 常用场景      | 功能完成   | 紧急补丁         |
git add .
git cherry-pick --continue
git cherry-pick --abort


git tag
git tag v1.0
git show v1.0.0
git push origin v1.0.0
git push origin --tags

如果以后维护开源项目
# 确认代码
git status

# 创建最后一次提交
git add .
git commit -m "prepare release v1.0.0"

# 打版本
git tag -a v1.0.0 -m "AI-SPACE first release"

# 推送代码
git push

# 推送tag
git push origin v1.0.0

git tag v0.5.0 b222222
git tag -a v1.0.0 -m "AI-SPACE first stable release"
git tag -d v1.0.0
git tag -a v1.0.0 b222222 -m "release version"
git commit --amend -m "新的提交说明"