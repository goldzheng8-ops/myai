


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
