from __future__ import annotations

from math import isclose
from typing import Iterable

Vec4 = tuple[float, float, float, float]
Mat4 = tuple[tuple[float, float, float, float], ...]


def mat_vec(m: Mat4, v: Vec4) -> Vec4:
    return tuple(
        sum(m[row][col] * v[col] for col in range(4)) for row in range(4)
    )  # type: ignore[return-value]


def mat_mul(a: Mat4, b: Mat4) -> Mat4:
    return tuple(
        tuple(
            sum(a[row][k] * b[k][col] for k in range(4))
            for col in range(4)
        )
        for row in range(4)
    )


def translation(tx: float, ty: float, tz: float) -> Mat4:
    return (
        (1.0, 0.0, 0.0, tx),
        (0.0, 1.0, 0.0, ty),
        (0.0, 0.0, 1.0, tz),
        (0.0, 0.0, 0.0, 1.0),
    )


def scale(sx: float, sy: float, sz: float) -> Mat4:
    return (
        (sx, 0.0, 0.0, 0.0),
        (0.0, sy, 0.0, 0.0),
        (0.0, 0.0, sz, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )


def assert_vec(actual: Iterable[float], expected: Iterable[float]) -> None:
    actual_values = tuple(actual)
    expected_values = tuple(expected)
    for a, e in zip(actual_values, expected_values, strict=True):
        assert isclose(a, e, rel_tol=1e-9, abs_tol=1e-9), (
            actual_values,
            expected_values,
        )


def main() -> None:
    t = translation(10.0, -2.0, 5.0)
    s = scale(2.0, 3.0, 4.0)

    point: Vec4 = (1.0, 2.0, 3.0, 1.0)
    direction: Vec4 = (1.0, 2.0, 3.0, 0.0)

    assert_vec(mat_vec(t, point), (11.0, 0.0, 8.0, 1.0))
    assert_vec(mat_vec(t, direction), direction)

    scale_then_translate = mat_mul(t, s)
    translate_then_scale = mat_mul(s, t)

    assert_vec(
        mat_vec(scale_then_translate, point),
        (12.0, 4.0, 17.0, 1.0),
    )
    assert_vec(
        mat_vec(translate_then_scale, point),
        (22.0, 0.0, 32.0, 1.0),
    )

    assert mat_vec(scale_then_translate, point) != mat_vec(
        translate_then_scale,
        point,
    )
    print("coordinate conventions: PASS")


if __name__ == "__main__":
    main()
