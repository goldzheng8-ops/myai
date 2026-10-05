from typing import Any

from core.template.extension.global_ import GlobalExtension


class MinGlobal(GlobalExtension):
	name = "min"

	def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> Any:
		if value is None:
			return None
		if args:
			return min(value, *args)
		return min(value)


class MaxGlobal(GlobalExtension):
	name = "max"

	def global_(self, value: Any = None, *args: Any, **kwargs: Any) -> Any:
		if value is None:
			return None
		if args:
			return max(value, *args)
		return max(value)


class SumGlobal(GlobalExtension):
	name = "sum"

	def global_(self, value: Any = None, start: Any = 0) -> Any:
		if value is None:
			return start
		return sum(value, start)


class AnyGlobal(GlobalExtension):
	name = "any"

	def global_(self, value: Any = None) -> bool:
		if value is None:
			return False
		return any(value)


class AllGlobal(GlobalExtension):
	name = "all"

	def global_(self, value: Any = None) -> bool:
		if value is None:
			return False
		return all(value)


class PowGlobal(GlobalExtension):
	name = "pow"

	def global_(self, value: Any = None, *args: Any) -> Any:
		if value is None or not args:
			return None
		return pow(value, *args)


class DivmodGlobal(GlobalExtension):
	name = "divmod"

	def global_(self, value: Any = None, *args: Any) -> Any:
		if value is None or not args:
			return None
		return divmod(value, args[0])
