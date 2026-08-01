from jinja2 import StrictUndefined
from jinja2 import Undefined

from .base import TemplateConfig


from jinja2 import Environment


class JinjaTemplateConfig(
    TemplateConfig,
):

    autoescape: bool = False

    undefined: type[Undefined] = StrictUndefined

    enable_async: bool = False

    trim_blocks: bool = False

    lstrip_blocks: bool = False

    cache_size: int = 400

    auto_reload: bool = False

    optimized: bool = True

    def create_environment(
        self,
    ) -> Environment:

        return Environment(
            autoescape=self.autoescape,
            undefined=self.undefined,
            enable_async=self.enable_async,
            trim_blocks=self.trim_blocks,
            lstrip_blocks=self.lstrip_blocks,
            cache_size=self.cache_size,
            auto_reload=self.auto_reload,
            optimized=self.optimized,
        )