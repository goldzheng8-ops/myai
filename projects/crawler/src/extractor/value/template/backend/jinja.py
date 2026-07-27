from extractor.value.template.backend.registry import  FilterRegistry, GlobalRegistry, TestRegistry
from jinja2 import Environment

from extractor.value.template.backend.base import TemplateBackend


class JinjaBackend(
    TemplateBackend,
):

    def __init__(
        self,
        environment: Environment,
    ) -> None:

        self._filters = FilterRegistry(
            environment.filters,
        )

        self._tests = TestRegistry(
            environment.tests,
        )

        self._globals = GlobalRegistry(
            environment.globals,
        )

    @property
    def filters(
        self,
    ) -> FilterRegistry:

        return self._filters
    
    @property
    def tests(
        self,
    ) -> TestRegistry:

        return self._tests
    
    @property
    def globals(
        self,
    ) -> GlobalRegistry:

        return self._globals