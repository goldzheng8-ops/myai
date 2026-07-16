field: image

type: css

query: img

attr: src



# scrapy:
    node.attrib["src"]

    node.xpath("@src").get()



# SelectorEngine

负责：

遍历 SelectorConfig
default
required
组织 dict
错误包装
日志
# ResponseAdapter

负责：

xpath
css
regex
attr
many
text 提取


# SelectorConfig

负责：

描述选择规则。