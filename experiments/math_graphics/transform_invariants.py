from __future__ import annotations

from math import isclose
from typing import Iterable

Vec3 = tuple[float, float, float]
Vec4 = tuple[float, float, float, float]
Mat3 = tuple[tuple[float, float, float], ...]
Mat4 = tuple[tuple[float, float, float, float], ...]


def mat4_vec(m: Mat4, v: Vec4) -> Vec4:
    return tuple(
        sum(m[row][col] * v[col] for col in range(4)) for row in range(4)
    )  # type: ignore[return-value]


def mat4_mul(a: Mat4, b: Mat4) -> Mat4:
    return tuple(
        tuple(sum(a[row][k] * b[k][col] for k in range(4)) for col in range(4))
        for row in range(4)
    )


def mat3_vec(m: Mat3, v: Vec3) -> Vec3:
    return tuple(
        sum(m[row][col] * v[col] for col in range(3)) for row in range(3)
    )  # type: ignore[return-value]


def transpose3(m: Mat3) -> Mat3:
    return tuple(tuple(m[col][row] for col in range(3)) for row in range(3))


def dot(a: Vec3, b: Vec3) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def assert_values(actual: Iterable[float], expected: Iterable[float]) -> None:
    av = tuple(actual)
    ev = tuple(expected)
    for a, e in zip(av, ev, strict=True):
        assert isclose(a, e, rel_tol=1e-9, abs_tol=1e-9), (av, ev)


def camera_world_and_view() -> tuple[Mat4, Mat4, tuple[Vec3, Vec3, Vec3], Vec3]:
    x_axis: Vec3 = (0.0, 1.0, 0.0)
    y_axis: Vec3 = (-1.0, 0.0, 0.0)
    z_axis: Vec3 = (0.0, 0.0, 1.0)
    position: Vec3 = (3.0, -2.0, 5.0)
    rotation: Mat3 = (
        (x_axis[0], y_axis[0], z_axis[0]),
        (x_axis[1], y_axis[1], z_axis[1]),
        (x_axis[2], y_axis[2], z_axis[2]),
    )
    rt = transpose3(rotation)
    tx = -dot(rt[0], position)
    ty = -dot(rt[1], position)
    tz = -dot(rt[2], position)
    world: Mat4 = (
        (rotation[0][0], rotation[0][1], rotation[0][2], position[0]),
        (rotation[1][0], rotation[1][1], rotation[1][2], position[1]),
        (rotation[2][0], rotation[2][1], rotation[2][2], position[2]),
        (0.0, 0.0, 0.0, 1.0),
    )
    view: Mat4 = (
        (rt[0][0], rt[0][1], rt[0][2], tx),
        (rt[1][0], rt[1][1], rt[1][2], ty),
        (rt[2][0], rt[2][1], rt[2][2], tz),
        (0.0, 0.0, 0.0, 1.0),
    )
    return world, view, (x_axis, y_axis, z_axis), position


def test_camera_view() -> None:
    world, view, axes, position = camera_world_and_view()
    assert_values(mat4_vec(view, (*position, 1.0)), (0.0, 0.0, 0.0, 1.0))
    for index, axis in enumerate(axes):
        expected = [0.0, 0.0, 0.0, 0.0]
        expected[index] = 1.0
        assert_values(mat4_vec(view, (*axis, 0.0)), expected)
    identity = mat4_mul(view, world)
    for row in range(4):
        for col in range(4):
            assert isclose(
                identity[row][col],
                1.0 if row == col else 0.0,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
    print("camera view invariants: PASS")


def test_normal_inverse_transpose() -> None:
    scale: Mat3 = (
        (2.0, 0.0, 0.0),
        (0.0, 3.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    inverse_transpose: Mat3 = (
        (0.5, 0.0, 0.0),
        (0.0, 1.0 / 3.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    tangent: Vec3 = (1.0, 0.0, -1.0)
    normal: Vec3 = (1.0, 0.0, 1.0)
    assert isclose(dot(tangent, normal), 0.0, abs_tol=1e-9)

    transformed_tangent = mat3_vec(scale, tangent)
    naive_normal = mat3_vec(scale, normal)
    correct_normal = mat3_vec(inverse_transpose, normal)

    assert not isclose(dot(transformed_tangent, naive_normal), 0.0, abs_tol=1e-9)
    assert isclose(dot(transformed_tangent, correct_normal), 0.0, abs_tol=1e-9)
    print("normal inverse-transpose invariant: PASS")


def main() -> None:
    test_camera_view()
    test_normal_inverse_transpose()


if __name__ == "__main__":
    main()
