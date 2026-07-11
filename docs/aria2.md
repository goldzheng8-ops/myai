# 下载链接
https://aria2.github.io/
# 命令
aria2c.exe -v
aria2c -x 16 -s 16 -k 1M "下载链接"
aria2c -x 4 -s 4 --all-proxy="http://127.0.0.1:7890" URL
aria2c -x 4 -s 4 --all-proxy="socks5://127.0.0.1:7891" URL
aria2c --conf-path=aria2.conf URL
# aria2.conf
enable-rpc=true
all-proxy=socks5://127.0.0.1:7891
max-connection-per-server=4
split=4
continue=true