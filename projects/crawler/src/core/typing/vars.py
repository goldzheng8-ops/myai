# 普通泛型（Invariant）

from typing import TypeVar


K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")
P = TypeVar("P")
H = TypeVar("H")


# Protocol 专用

K_contra = TypeVar(
    "K_contra",
    contravariant=True,
)

V_contra = TypeVar(
    "V_contra",
    contravariant=True,
)

T_co = TypeVar(
    "T_co",
    covariant=True,
)