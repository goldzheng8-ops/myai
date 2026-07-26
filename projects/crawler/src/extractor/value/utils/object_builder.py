

from extractor.value.utils.object_context import ObjectContext
from runtime.extract_context import ExtractContext


class ObjectContextBuilder:

    def build(
        self,
        context: ExtractContext,
    ) -> ObjectContext:

        scope = ObjectContext()

        self.add_variables(
            scope,
            context,
        )

        self.add_objects(
            scope,
            context,
        )

        return scope
    
    def add_variables(

        self,

        scope:ObjectContext,

        context:ExtractContext,

    ):

        scope.update(
            context.variables,
        )

    def add_objects(

        self,

        scope:ObjectContext,

        context:ExtractContext,

    ):

        scope.set(
            "request",
            context.request,
        )

        scope.set(
            "response",
            context.response,
        )

        scope.set(
            "node",
            context.node,
        )