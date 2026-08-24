model.py
    │
    ├── ApplicationConfig
    ├── SpiderDefinition
    ├── RuntimeSettings
    └── CrawlRequest / OverrideModel

loader.py
    │
    └── YAML / environment / file loading

parser.py
    │
    └── raw data → ApplicationConfig

factory.py
    │
    ├── ApplicationConfig
    │       ↓
    │   core configuration
    │
    └── CrawlRequest + SpiderDefinition
            ↓
        effective configuration

factory.py
    ApplicationConfig → Core objects

resolver.py
    Default SpiderConfig
          +
    Runtime Override
          ↓
    Effective SpiderConfig