                CrawlerConfig
                      │
                      ▼
              ResponseAdapter
                      │
                      ▼
             SelectorEngine
                      │
             PluginRegistry
                      │
      ┌───────────────┼──────────────┐
      ▼               ▼              ▼
  CssSelector    XPathSelector   RegexSelector
                      │
                      ▼
                  Raw Value
                      │
                      ▼
             TransformEngine
                      │
             PluginRegistry
                      │
      ┌───────────────┼──────────────┐
      ▼               ▼              ▼
 StripTransform ReplaceTransform NumberTransform
                      │
                      ▼
                  Final Value