docker exec -it postgres psql -U aiuser -d ai_space_db
  缺省-d参数默认登录与用户名同名的数据库
\q 退出
\c 切换当前连接的数据库
\l 列出数据库
\dt 列出表
\conninfo 查看当前连接信息

CREATE DATABASE ai_space;

CREATE USER aiuser WITH PASSWORD 'ai123456';

GRANT ALL PRIVILEGES
ON DATABASE ai_space
TO aiuser;

# 导出数据库：
docker exec postgres pg_dump -U aiuser -t news ai_space > news.sql
# 导入数据库：
docker exec -i postgres psql -U aiuser -d ai_space_db < news.**sql**