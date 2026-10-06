第一层：先学通用 SQL

这才是你真正应该系统掌握的。

SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT

JOIN
LEFT JOIN
INNER JOIN

UNION
UNION ALL

CASE WHEN

COUNT
SUM
AVG
MIN
MAX

DISTINCT

WITH / CTE

子查询

窗口函数
OVER
PARTITION BY
ROW_NUMBER
RANK
LAG
LEAD

对于你的数据分析项目，这些已经能覆盖绝大多数日常 SQL。

而且 DuckDB 官方也明确说，它的 SQL dialect 紧密遵循 PostgreSQL。基本 SQL 概念完全没必要从 DuckDB 特有语法开始学。

第二层：用到 DuckDB 特性时再学

这反而是 DuckDB 很有意思的地方。

比如：

GROUP BY ALL

代替：

GROUP BY
    category,
    region,
    year

或者：

ORDER BY ALL

以及：

SELECT * EXCLUDE (created_at)

还有：

SELECT * REPLACE (...)

以及：

UNION BY NAME

这些都是 DuckDB 提供的 Friendly SQL 特性。

对于你的项目，它们其实非常实用。

例如：

SELECT
    category,
    region,
    SUM(amount) AS revenue
FROM sales
GROUP BY ALL
ORDER BY ALL

这种 SQL 对个人数据分析非常舒服。