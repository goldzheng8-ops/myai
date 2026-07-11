@echo off
REM Windows环境下的HTTPS设置脚本

echo 🔐 设置HTTPS安全配置...

REM 检查OpenSSL是否安装
where openssl >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ OpenSSL未安装，请先安装OpenSSL
    echo 下载地址: https://slproweb.com/products/Win32OpenSSL.html
    pause
    exit /b 1
)

REM 创建SSL目录
if not exist "ssl" mkdir ssl

REM 检查是否已有证书
if exist "ssl\cert.pem" if exist "ssl\key.pem" (
    echo ✅ SSL证书已存在
    echo 证书信息：
    openssl x509 -in ssl\cert.pem -text -noout | findstr "Subject:"
    openssl x509 -in ssl\cert.pem -text -noout | findstr "Not After"
    goto :end
)

echo 🔨 生成自签名证书...

REM 生成私钥
openssl genrsa -out ssl\key.pem 2048

REM 生成证书签名请求
openssl req -new -key ssl\key.pem -out ssl\cert.csr -subj "/C=CN/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

REM 生成自签名证书
openssl x509 -req -days 365 -in ssl\cert.csr -signkey ssl\key.pem -out ssl\cert.pem

REM 清理临时文件
del ssl\cert.csr

echo ✅ 自签名证书生成完成！
echo.
echo 📋 证书信息：
openssl x509 -in ssl\cert.pem -text -noout | findstr "Subject:"
openssl x509 -in ssl\cert.pem -text -noout | findstr "Not After"

echo.
echo ⚠️  注意：
echo    1. 这是自签名证书，浏览器会显示安全警告
echo    2. 生产环境请使用Let's Encrypt或商业证书
echo    3. 证书有效期为365天
echo.
echo 🔧 使用Let's Encrypt证书：
echo    1. 确保有域名和公网IP
echo    2. 在Linux服务器上运行: certbot --nginx -d your-domain.com
echo    3. 证书会自动配置到Nginx

:end
echo.
echo �� HTTPS配置完成！
pause 