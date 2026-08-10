from __future__ import annotations

from math import isclose, radians, tan
from typing import Iterable

Vec4 = tuple[float, float, float, float]
Mat4 = tuple[tuple[float, float, float, float], ...]


def mat_vec(m: Mat4, v: Vec4) -> Vec4:
    return tuple(
        sum(m[row][col] * v[col] for col in range(4)) for row in range(4)
    )  # type: ignore[return-value]


def ndc(clip: Vec4) -> tuple[float, float, float]:
    x, y, z, w = clip
    assert w != 0.0
    return (x / w, y / w, z / w)


def perspective_rh_zo(
    fov_y_degrees: float,
    aspect: float,
    near: float,
    far: float,
) -> Mat4:
    assert 0.0 < near < far
    f = 1.0 / tan(radians(fov_y_degrees) * 0.5)
    return (
        (f / aspect, 0.0, 0.0, 0.0),
        (0.0, f, 0.0, 0.0),
        (0.0, 0.0, far / (near - far), near * far / (near - far)),
        (0.0, 0.0, -1.0, 0.0),
    )


def orthographic_rh_zo(
    left: float,
    right: float,
    bottom: float,
    top: float,
    near: float,
    far: float,
) -> Mat4:
    assert left < right and bottom < top and 0.0 < near < far
    return (
        (
            2.0 / (right - left),
            0.0,
            0.0,
            -(right + left) / (right - left),
        ),
        (
            0.0,
            2.0 / (top - bottom),
            0.0,
            -(top + bottom) / (top - bottom),
        ),
        (0.0, 0.0, 1.0 / (near - far), near / (near - far)),
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
    perspective = perspective_rh_zo(90.0, 1.0, 1.0, 10.0)
    assert_vec(
        ndc(mat_vec(perspective, (0.0, 0.0, -1.0, 1.0))),
        (0.0, 0.0, 0.0),
    )
    assert_vec(
        ndc(mat_vec(perspective, (0.0, 0.0, -10.0, 1.0))),
        (0.0, 0.0, 1.0),
    )
    assert_vec(
        ndc(mat_vec(perspective, (1.0, 1.0, -1.0, 1.0))),
        (1.0, 1.0, 0.0),
    )

    orthographic = orthographic_rh_zo(-2.0, 2.0, -1.0, 1.0, 1.0, 11.0)
    assert_vec(
        ndc(mat_vec(orthographic, (-2.0, -1.0, -1.0, 1.0))),
        (-1.0, -1.0, 0.0),
    )
    assert_vec(
        ndc(mat_vec(orthographic, (2.0, 1.0, -11.0, 1.0))),
        (1.0, 1.0, 1.0),
    )

    print("projection mapping: PASS")


if __name__ == "__main__":
    main()
