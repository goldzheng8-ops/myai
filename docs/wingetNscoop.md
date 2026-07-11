| 对比         | WinGet | Scoop      |
| ---------- | ------ | ---------- |
| 官方支持       | ✅ 微软官方 | ❌ 社区维护     |
| Windows 11 | ✅ 默认内置 | ❌ 需要安装     |
| 软件数量       | 很多     | 很多（开发工具更多） |
| 开发工具       | 很好     | ⭐ 非常好      |
| 修改系统环境     | 较少     | 基本安装到用户目录  |
| 企业环境       | ⭐⭐⭐⭐⭐  | ⭐⭐⭐        |
| 推荐程度（你的情况） | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐       |

## winget

winget --version
winget search uv
winget install --id=astral-sh.uv
winget upgrade
winget upgrade --all

## scoop

scoop install git

#################################################
winget install Git.Git

winget install Microsoft.VisualStudioCode

winget install Docker.DockerDesktop

winget install astral-sh.uv

winget install Microsoft.PowerShell

winget install Microsoft.WindowsTerminal
################################################
scoop install jq

scoop install ripgrep

scoop install fd

scoop install fzf

scoop install lazygit
