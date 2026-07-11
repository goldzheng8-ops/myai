# 掌握 ES6 基础语法 + 常用内置方法


| 方法              | 作用     | 示例                                     |
| --------------- | ------ | -------------------------------------- |
| `toFixed(2)`    | 保留小数   | `(3.14159).toFixed(2)` → `"3.14"`      |
| `toUpperCase()` | 转大写    | `"news".toUpperCase()` → `"NEWS"`      |
| `toLowerCase()` | 转小写    | `"NEWS".toLowerCase()` → `"news"`      |
| `trim()`        | 去掉首尾空格 | `" hello ".trim()` → `"hello"`         |
| `split()`       | 分割字符串  | `"a,b,c".split(",")`                   |
| `join()`        | 合并数组   | `["a","b"].join("-")` → `"a-b"`        |
| `includes()`    | 是否包含   | `"hello".includes("he")` → `true`      |
| `replace()`     | 替换字符串  | `"HN News".replace("HN","HackerNews")` |
| `length`        | 获取长度   | `"hello".length` → `5`                 |
| 功能      | 表达式                                               |
| ------- | ------------------------------------------------- |
| 读取字段    | `{{$json.inserted}}`                              |
| 当前时间    | `{{$now}}`                                        |
| 字符串拼接   | `{{"新增 " + $json.inserted}}`                      |
| 模板字符串   | ``{{`新增 ${$json.inserted}`}}``                    |
| 条件判断    | `{{$json.inserted > 0 ? "Success" : "Empty"}}`    |
| 数学计算    | `{{$json.total - $json.duplicated}}`              |
| 百分比     | `{{($json.inserted/$json.total*100).toFixed(2)}}` |
| 工作流名称   | `{{$workflow.name}}`                              |
| 执行 ID   | `{{$execution.id}}`                               |
| 当前 Item | `{{$itemIndex}}`                                  |
Number((3.14159).toFixed(2))
parseFloat((3.14159).toFixed(2))

# Loop 常用变量
| 表达式            | 作用       |
| -------------- | -------- |
| `$json.title`  | 当前新闻     |
| `$itemIndex`   | 第几个 Item |
| `$json.url`    | 当前URL    |
| `$json.source` | 来源       |

| API              | 作用                 |
| ---------------- | ------------------ |
| `$input.first()` | 获取第一条数据（适合只有一条输入时） |
| `$input.all()`   | 获取所有输入数据           |
| `item.json`      | 当前数据内容             |
| `return [item]`  | 返回一条数据             |
| `return items`   | 返回多条数据             |
| `new Date()`     | 当前时间               |
| `Math.round()`   | 四舍五入               |
| `Array.map()`    | 批量转换               |
| `Array.filter()` | 过滤                 |
| `Array.sort()`   | 排序                 |
| `Set`            | 去重                 |


# 代码示例：
##############################################
let md = "# 今日新闻\n\n";

$input.all().forEach(item => {
    md += `- ${item.json.title}\n`;
});

return [
    {
        json:{
            markdown: md
        }
    }
];
##############################################
const seen = new Set();

const result = [];

for (const item of $input.all()) {

    if (!seen.has(item.json.title)) {

        seen.add(item.json.title);

        result.push(item);

    }

}

return result;
##############################################
const items = $input.all();

items.sort((a, b) =>
    a.json.title.localeCompare(b.json.title)
);

return items;
###############################################


| 通知方式     | 是否需要自己的账号 | 认证方式                | 推荐程度  |
| -------- | --------- | ------------------- | ----- |
| Telegram | ✅ 是       | Bot Token + Chat ID | ⭐⭐⭐⭐⭐ |
| Gmail    | ✅ 是       | Google OAuth        | ⭐⭐⭐⭐  |
| Outlook  | ✅ 是       | Microsoft OAuth     | ⭐⭐⭐   |
| Slack    | ✅ 是       | Slack App Token     | ⭐⭐⭐   |
| Discord  | ✅ 是       | Webhook 或 Bot       | ⭐⭐⭐⭐  |
| 企业微信     | ✅ 是       | 企业机器人/Webhook       | ⭐⭐⭐⭐  |
| 飞书       | ✅ 是       | Webhook             | ⭐⭐⭐⭐  |
