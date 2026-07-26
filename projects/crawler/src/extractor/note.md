


| 模块              | 职责                    | 是否关心 default/required |
| --------------- | --------------------- | --------------------- |
| SelectorPlugin  | 根据 XPath/CSS/Regex 找值 | ❌                     |
| SelectorEngine  | 调度 SelectorPlugin     | ❌                     |
| TransformPlugin | 转换数据                  | ❌                     |
| TransformEngine | 调度 TransformPlugin    | ❌                     |
| **Extractor**   | 编排整个抽取流程              | ✅                     |


ResponseAdapter
        │
        ▼
Extractor
        │
        ├─────────────┐
        ▼             ▼
SelectorEngine   TransformEngine
        │             │
        ▼             ▼
 SelectorPlugin  TransformPlugin

 | 配置                   | 职责                                                       |
| -------------------- | -------------------------------------------------------- |
| `SelectorConfig`     | **如何定位数据**（XPath、CSS、Regex 等）                            |
| `TransformConfig`    | **如何转换数据**（strip、replace、number 等）                       |
| `ExtractFieldConfig` | **一个字段完整的抽取流程**（字段名、Selector、Transform、default、required） |

这是我最推荐的设计。 它符合我们前面一直在构建的 Pipeline（Extractor） + Engine（Selector/Transform） + Plugin（XPath/CSS/Strip 等） 分层架构，每一层的职责边界都很清晰，也方便以后扩展一个字段对应多个 Selector、条件抽取、嵌套字段等高级能力。


extractor/
│
├── base.py                    # ExtractorPlugin
├── engine.py                  # ExtractorEngine
├── registry.py                # ExtractorRegistry
│
├── builder.py                 # FieldBuilder
├── context.py                 # ExtractContext
│
├── result.py                  # ExtractResult
├── record.py                  # ExtractRecord
│
├── plugins/
│     ├── html.py              # HtmlExtractor
│     ├── json.py              # JsonExtractor
│     ├── attribute.py         # AttributeExtractor
│     ├── object.py            # ObjectExtractor
│     └── list.py              # ListExtractor
│
└── utils.py

ExtractorPlugin
        │
        ├── HtmlExtractor
        ├── JsonExtractor
        ├── ObjectExtractor
        └── ListExtractor
extractor/
│
├── field.py          # FieldExtractor
├── engine.py
├── registry.py
├── plugins/

FieldExtractor
      │
      ├── ValueExtractor      ← 负责产生原始值
      │        │
      │        ├── SelectorEngine
      │        ├── ConstantValue
      │        ├── ContextValue
      │        └── ExpressionValue
      │
      └── TransformEngine

extractor/
│
├── engine.py
├── registry.py
│
├── field.py               # FieldExtractor
├── value.py               # ValueExtractor
├── builder.py             # ExtractBuilder
│
├── plugins/
│     ├── object.py
│     ├── list.py
│     ├── html.py
│     └── json.py

ObjectExtractor
        │
        ▼
FieldExtractor
        │
        ├──────────────┐
        ▼              ▼
ValueExtractor   TransformEngine
        │
        ▼
SelectorEngine

ObjectExtractor
        │
        ▼
FieldExtractor
        │
        ├── ValueEngine
        │        ├── SelectorValuePlugin
        │        ├── ContextValuePlugin
        │        ├── ConstantValuePlugin
        │        ├── TemplateValuePlugin
        │        └── ExpressionValuePlugin
        │
        └── TransformEngine

value/
│
├── base.py               # ValuePlugin
├── engine.py             # ValueEngine
├── registry.py           # ValueRegistry
│
├── context.py            # ValueContext
├── result.py             # (可选，以后扩展)
│
├── plugins/
│      ├── selector.py
│      ├── constant.py
│      ├── context.py
│      ├── template.py
│      └── expression.py

ObjectExtractor / ListExtractor
          │
          ▼
FieldExtractor（协调器）
          │
          ├── ValueEngine（产生值）
          │        ├── SelectorValuePlugin
          │        ├── ConstantValuePlugin
          │        ├── ContextValuePlugin
          │        ├── TemplateValuePlugin
          │        └── ExpressionValuePlugin
          │
          └── TransformEngine（处理值）
                   ├── RegexTransform
                   ├── TrimTransform
                   ├── UpperTransform
                   └── …

FieldExtractor
        │
        ▼
ValueEngine
        │
        ▼
ValueRegistry
        │
        ├── SelectorPlugin
        ├── ConstantPlugin
        ├── ContextPlugin
        ├── ExpressionPlugin
        └── TemplatePlugin