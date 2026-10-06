# Jupyter Notebook 高频快捷键

## 一、最重要：两种模式

Jupyter 主要有两个核心模式：

| 模式 | 作用 |
| --- | --- |
| 编辑模式 | 正在输入代码或 Markdown |
| 命令模式 | 操作 Cell |

最重要的切换方式：

- `Enter` → 进入编辑当前 Cell
- `Esc` → 进入命令模式

> 以后绝大多数快捷键都在命令模式下使用。

---

## 二、运行 Cell

| 快捷键 | 功能 |
| --- | --- |
| `Shift + Enter` | 运行当前 Cell，并跳到下一个 Cell |
| `Ctrl + Enter` | 运行当前 Cell，停留在当前 Cell |
| `Alt + Enter` | 运行当前 Cell，并在下面创建新 Cell |

### 推荐使用方式

最常见和最推荐的操作：

```text
代码
  ↓
Shift + Enter
  ↓
结果
  ↓
下一个 Cell
  ↓
继续实验
```

这基本就是 Jupyter 的核心工作流。

---

## 三、Cell 操作

先按 `Esc` 进入命令模式，然后使用这些快捷键：

| 快捷键 | 功能 |
| --- | --- |
| `A` | 在上面插入 Cell |
| `B` | 在下面插入 Cell |
| `D D` | 删除当前 Cell |
| `M` | 转为 Markdown |
| `Y` | 转为 Code |
| `C` | 复制 Cell |
| `X` | 剪切 Cell |
| `V` | 粘贴 Cell |
| `Z` | 撤销删除 Cell |

### 最值得记住的几个

- `A` → 上面加 Cell
- `B` → 下面加 Cell
- `D D` → 删除 Cell
- `M` → 切到 Markdown
- `Y` → 切到 Code

---

## 四、移动 Cell

在命令模式下：

| 快捷键 | 功能 |
| --- | --- |
| `↑` | 选择上一个 Cell |
| `↓` | 选择下一个 Cell |

如果你要整理实验顺序：

| 快捷键 | 功能 |
| --- | --- |
| `Shift + ↑` | 上移 Cell |
| `Shift + ↓` | 下移 Cell |

---

## 五、编辑代码

编辑模式下常用：

| 快捷键 | 功能 |
| --- | --- |
| `Ctrl + A` | 全选 |
| `Ctrl + C` | 复制 |
| `Ctrl + X` | 剪切 |
| `Ctrl + V` | 粘贴 |
| `Ctrl + Z` | 撤销 |
| `Ctrl + /` | 注释 / 取消注释 |

### 示例

```python
df = project.load_data("sales.csv")
result = project.query(sql)
```

选中后按 `Ctrl + /`，就会变成：

```python
# df = project.load_data("sales.csv")
# result = project.query(sql)
```

---

## 六、代码补全

这个会非常常用：

- `Tab` → 代码补全

例如：

```python
df.gro
```

按 `Tab` 后可以看到：

```text
groupby
group
...
```

对象属性也能补全：

```python
df.
```

然后按 `Tab`。

---

## 七、查看 API

这个对学习 `pandas` / `DuckDB` / `Matplotlib` 很重要。

### `Shift + Tab`

例如：

```python
df.groupby(
```

把光标放在括号内部，按 `Shift + Tab`，Jupyter 会显示函数签名和帮助信息。

连续按两次：

- `Shift + Tab`
- `Shift + Tab`

可以展开更多帮助。

### `?`

```python
df.groupby?
```

可以查看帮助。

### `??`

```python
df.groupby??
```

可以查看更详细的信息或源码。

> 不过第三方库很多实现并不适合靠 `??` 深挖，所以当前更推荐：API Reference 为主，Jupyter `Shift + Tab` 为辅。

---

## 八、搜索 Notebook

非常值得记住：

- `Ctrl + F` → 搜索当前 Notebook 内容

例如你实验了很多 Cell：

- `load_data`
- `groupby`
- `merge`
- `plot`
- `DuckDB`

直接按 `Ctrl + F` 即可搜索。

---

## 九、Kernel 操作

| 操作 | 快捷键 |
| --- | --- |
| 中断运行 | `I I` |
| 重启 Kernel | `0 0` |
| 重启并清空输出 | 根据 JupyterLab 菜单操作 |

也就是说：

```text
Esc
I I
```

可以中断一个卡住的 Cell。

---

## 十、最值得记住的“核心 15 个”

如果不想背太多，只记这一张：

### 模式

- `Enter` → 编辑模式
- `Esc` → 命令模式

### 运行

- `Shift + Enter` → 运行并进入下一 Cell
- `Ctrl + Enter` → 运行但停留
- `Alt + Enter` → 运行并创建下一 Cell

### Cell

- `A` → 上面插入
- `B` → 下面插入
- `D D` → 删除
- `M` → Markdown
- `Y` → Code

### 编辑

- `Ctrl + /` → 注释
- `Tab` → 补全
- `Shift + Tab` → 查看 API

### 其他

- `Ctrl + F` → 搜索
- `I I` → 中断 Kernel
- `0 0` → 重启 Kernel

---

## 十一、适合当前项目的实验节奏

你以后可以把 Notebook 写成这样的结构：

```python
# 1. 导入
import pandas as pd
from project import NotebookProject, SqlFormatter

# 2. 数据
project = NotebookProject(...)
df = project.load_data("sales.csv")

# 3. 探索
df.head()
df.info()
df.describe()

# 4. 分析
result = (
    df.groupby("category")
      .agg(...)
)

# 5. SQL 实验
sql = SqlFormatter.format("""
    select ...
    from ...
    group by ...
""")

result = project.query_df(df, sql)

# 6. 可视化
project.plot(...)
```

然后就可以自然地这样工作：

```text
A / B
  ↓
写一点
  ↓
Shift + Enter
  ↓
看结果
  ↓
改参数
  ↓
Shift + Enter
  ↓
继续
```

这才是这个项目真正应该追求的使用体验：几乎没有工程摩擦，想到一个分析就立刻能试。

> `Shift + Tab` 和官方 API Reference，会成为你学习 `pandas` / `DuckDB` / `Matplotlib` 最重要的两个工具。

---

## 十二、总结

如果只记住一件事：

- `Esc` 控制 Cell
- `Shift + Enter` 运行并继续
- `Tab` 自动补全
- `Shift + Tab` 查看帮助
- `A/B/M/Y` 组织 Notebook

这已经足够支撑你在数据分析项目中高效实验和迭代。