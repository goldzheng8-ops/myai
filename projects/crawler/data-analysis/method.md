| 你想知道什么        | 常见方法                |
| ------------- | ------------------- |
| 通常是多少？        | 均值 / 中位数            |
| 数据波动多大？       | 标准差 / 分位数           |
| 谁特别高/低？       | Z-score / IQR / 分位数 |
| 随时间是否异常？      | 时间序列 / 移动平均         |
| 某个变量应该产生什么结果？ | 回归                  |
| 两个变量有没有关系？    | 相关性 / 回归            |
| 某个群体和其他群体不同吗？ | 分组比较                |
| 某条记录为什么特别？    | 回归残差 / 分组基准         |
| 是不是数据本身有问题？   | 数据质量检查              |


load
 ↓
head()
 ↓
describe()
 ↓
distribution
 ↓
groupby
 ↓
correlation
 ↓
plot
 ↓
hypothesis
 ↓
SQL
 ↓
regression
 ↓
residual
 ↓
发现异常
 ↓
继续挖
-----------------------------------------------------
你首先会大量接触的是：

线性回归
多元线性回归
Ridge / Lasso
Logistic Regression
决策树
Random Forest
Gradient Boosting
PCA
聚类
时间序列
特征工程
模型评估

pandas
    ↓
DuckDB
    ↓
pandas
    ↓
DuckDB
    ↓
scikit-learn
    ↓
CPU
    ↓
CPU

| 需求                 | 再考虑                         |
| ------------------ | --------------------------- |
| 统计检验、统计分布、显著性分析    | `scipy` / `statsmodels`     |
| 更专业的计量经济学          | `statsmodels`               |
| 时间序列               | 先用 pandas/scikit-learn，再看需求 |
| 深度学习               | `PyTorch`                   |
| 更强的梯度提升            | `XGBoost` / `LightGBM`      |
| 交互式网页图表            | `plotly`                    |
| 地理空间数据             | `geopandas`                 |
| Excel 特殊处理         | `openpyxl`                  |
| Parquet/Arrow 生态需求 | `pyarrow`                   |
