from __future__ import annotations

import pytest

from core.runtime.context import RuntimeContext
from core.runtime.expression import DotPathExpression

'''
pytest src/core/runtime/test_context.py -q         

'''

class DummyResolver:
    def __init__(self):
        self.calls: list[tuple[RuntimeContext, DotPathExpression]] = []

    def resolve(self, context: RuntimeContext, expression: DotPathExpression):
        self.calls.append((context, expression))
        return context.get("user")["name"]


def test_context_set_get_and_contains_across_scopes():
    context = RuntimeContext()

    context.set("user", {"name": "alice"})
    assert context.contains("user") is True
    assert context.get("user") == {"name": "alice"}

    context.push(name="inner")
    context.set("token", "abc123")

    assert context.contains("token") is True
    assert context.get("token") == "abc123"
    assert context.get("user") == {"name": "alice"}

    context.pop()
    assert context.get("token") is None


def test_context_update_remove_clear_and_flatten():
    context = RuntimeContext()
    context.set("a", 1)
    context.update({"b": 2, "c": 3})

    assert context.flatten() == {"a": 1, "b": 2, "c": 3}

    context.remove("b")
    assert context.get("b") is None

    context.push(name="inner")
    context.set("c", 99)
    assert context.flatten() == {"a": 1, "c": 99}

    context.clear()
    assert context.flatten() == {"a": 1, "c": 3}


def test_context_merge_and_copy_keep_independent_state():
    left = RuntimeContext()
    left.set("user", {"name": "alice"})

    right = RuntimeContext()
    right.set("token", "abc")

    left.merge(right)
    assert left.get("token") == "abc"

    copied = left.copy()
    copied.set("session", "xyz")

    assert left.get("session") is None
    assert copied.get("session") == "xyz"
    assert dict(copied.as_mapping()) == {
        "user": {"name": "alice"},
        "token": "abc",
        "session": "xyz",
    }


def test_context_resolve_uses_resolver_and_wraps_string_expressions():
    context = RuntimeContext()
    context.set("user", {"name": "alice"})

    resolver = DummyResolver()
    context.set_resolver(resolver) # type: ignore

    result = context.resolve("user.name") # type: ignore

    assert result == "alice"
    assert len(resolver.calls) == 1
    expression = resolver.calls[0][1]
    assert isinstance(expression, DotPathExpression)
    assert expression.path == "user.name"


def test_context_requires_resolver_before_resolution_and_blocks_mutation_when_frozen():
    context = RuntimeContext()

    with pytest.raises(RuntimeError, match="ResolveEngine not configured"):
        context.resolve("user.name") # type: ignore

    context.freeze()
    with pytest.raises(RuntimeError, match="frozen"):
        context.set("user", {"name": "alice"})

    context.unfreeze()
    context.set("user", {"name": "alice"})
    assert context.get("user") == {"name": "alice"}


def test_context_push_pop_scope_and_global_scope_guard():
    context = RuntimeContext()
    context.set("a", 1)

    child = context.push(name="child")
    child.set("b", 2)
    assert context.get("b") == 2

    context.pop()
    assert context.get("b") is None

    with pytest.raises(RuntimeError, match="Cannot pop global scope"):
        context.pop()
