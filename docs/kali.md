windows系统：Windows 10 专业版 22H2，更好地支持wsl相关命令

重要配置文件wsl.conf，放在 Linux 里面的 /etc/ 目录下，不是 Windows 用户目录下的 .wslconfig！

[network]
generateResolvConf = false
generateHosts = false
hostname = kali-custom

[automount]
enabled = true
options = "metadata,umask=22,fmask=11"
/etc/resolv.conf的内容
nameserver 8.8.8.8
nameserver 1.1.1.1
打开 “Windows Defender 防火墙” > 高级设置；
添加新的 入站和出站规则：
允许 vmmem, wsl.exe, wslhost.exe, svchost.exe 通过所有端口和协议；
稳妥起见先试“允许所有”测试是否网络正常，然后逐步收紧。
New-NetFirewallRule -DisplayName "WSL2 Proxy Allow" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 7890
New-NetFirewallRule -DisplayName "WSL Proxy Access" -Direction Inbound -Protocol TCP -LocalPort 7890 -Action Allow
New-NetFirewallRule -DisplayName "Allow UDP 1080" -Direction Inbound -Protocol UDP -LocalPort 1080 -Action Allow
自动获取 Windows 主机 IP
# 方法一：固定网关 IP
ip route | grep default
# 输出示例：default via 172.25.144.1 dev eth0
# 所以 Windows IP 是 172.25.144.1

# 方法二：使用内置 host.docker.internal（部分 WSL 版本支持）
ping host.docker.internal
~/.bashrc
echo 'export http_proxy="http://127.0.0.1:7890"' >> ~/.bashrc
echo 'export https_proxy="http://127.0.0.1:7890"' >> ~/.bashrc
echo 'export all_proxy="http://127.0.0.1:7890"' >> ~/.bashrc
source ~/.bashrc
/etc/apt/apt.conf.d/99proxy
Acquire::http::Proxy "http://172.27.240.1:7890/";
Acquire::https::Proxy "http://172.27.240.1:7890/";
Kali 系统配置
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y kali-linux-headless
sudo apt install -y git curl wget vim net-tools build-essential unzip htop
sudo apt install -y zsh
chsh -s $(which zsh)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
sudo apt install -y python3 python3-pip
pip3 install --upgrade pip
pip3 install requests flask ipython
sudo apt install -y proxychains4 tor
sudo apt install -y openssh-server
sudo service ssh start
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt install -y kali-desktop-xfce
startxfce4
sudo apt install -y fonts-noto-cjk language-pack-zh-hans
Kali Rolling 安装源
sudo nano /etc/apt/sources.list

deb http://http.kali.org/kali kali-rolling main non-free contrib
deb http://mirrors.aliyun.com/kali kali-rolling main non-free contrib
deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main non-free contrib
deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib
GPG 错误，可尝试导入官方密钥：

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ED444FF07D8D0BF6
具体流程
在 /etc/apt/apt.conf.d/ 中创建一个配置文件：

echo 'Acquire::AllowInsecureRepositories "true";' | sudo tee /etc/apt/apt.conf.d/99insecure
sudo apt update
sudo install gnupg
sudo rm -f /etc/apt/trusted.gpg.d/kali-archive.gpg
curl -fsSL https://archive.kali.org/archive-key.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/kali-archive.gpg
sudo apt update
#备用：
curl -fsSL https://archive.kali.org/archive-key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/kali-archive.gpg > /dev/null
sudo apt update
sudo rm /etc/apt/apt.conf.d/99insecure
快捷修复命令组合
# 1. 替换清华源
echo 'deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main non-free contrib' | sudo tee /etc/apt/sources.list

# 2. 导入 Kali 签名
curl -fsSL https://archive.kali.org/archive-key.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/kali-archive.gpg > /dev/null

# 3. 更新缓存
sudo apt update


杂项
sudo nano /etc/apt/apt.conf.d/99proxy
#内容
Acquire::http::Proxy "http://127.0.0.1:7890";
Acquire::https::Proxy "http://127.0.0.1:7890";
# proxychains
sudo apt install proxychains4 -y
sudo nano /etc/proxychains4.conf
#content
socks5 127.0.0.1 1080
proxychains4 apt update
proxychains4 curl http://ipinfo.io
curl ifconfig.me
proxychains4 curl ifconfig.me

重启 LxssManager 服务：

Restart-Service LxssManager