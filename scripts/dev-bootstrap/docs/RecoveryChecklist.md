# Windows 开发环境恢复

## 系统
- [ ] 微软官方发布：https://github.com/microsoft/ 下载wsl,winget-cli
- [ ] Windows 更新完成
- [ ] 开启 Hyper-V
- [ ] 开启 WSL2

## scoop

- [ ] 官网：https://scoop.sh/
- [ ] Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
- [ ] irm get.scoop.sh | iex

## Git

- [ ] 安装：winget install Git.Git或 scoop install git
- [ ] git config --global user.name
- [ ] git config --global user.email
- [ ] ssh-keygen

## uv

- [ ] 安装：Windows PowerShell 执行：powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
- [ ] PATH 环境变量：$env:Path = "C:\Users\Administrator\.local\bin;$env:Path"
- [ ] 验证：uv --version

## Python

- [ ] uv 安装 uv python install 3.12
- [ ] 查看版本 uv python list
- [ ] 虚拟环境 uv venv --python 3.12
- [ ] uv sync
  
## VSCode

- [ ] 安装
- [ ] 插件恢复
- [ ] Settings 恢复

## Docker

- [ ] Docker Desktop
- [ ] daemon.json
- [ ] Docker Network
- [ ] 镜像：  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.1panel.live"
  ]

## AI-WORKSPACE

- [ ] Clone
- [ ] docker compose up
- [ ] uv sync
- [ ] pytest