from __future__ import annotations

import math
import struct


def to_float32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def next_float32_up(value: float) -> float:
    value = to_float32(value)
    if math.isnan(value) or value == math.inf:
        return value
    if value == -0.0:
        value = 0.0
    bits = struct.unpack(">I", struct.pack(">f", value))[0]
    if value >= 0.0:
        bits += 1
    else:
        bits -= 1
    return struct.unpack(">f", struct.pack(">I", bits))[0]


def standard_depth(distance: float, near: float, far: float) -> float:
    assert near <= distance <= far
    a = far / (far - near)
    c = near * far / (far - near)
    return a - c / distance


def distance_from_standard_depth(
    depth: float,
    near: float,
    far: float,
) -> float:
    a = far / (far - near)
    c = near * far / (far - near)
    return c / (a - depth)


def reversed_depth(distance: float, near: float, far: float) -> float:
    return 1.0 - standard_depth(distance, near, far)


def distance_from_reversed_depth(
    depth: float,
    near: float,
    far: float,
) -> float:
    return distance_from_standard_depth(1.0 - depth, near, far)


def world_step_standard(distance: float, near: float, far: float) -> float:
    d0 = to_float32(standard_depth(distance, near, far))
    d1 = next_float32_up(d0)
    return abs(
        distance_from_standard_depth(d1, near, far)
        - distance_from_standard_depth(d0, near, far)
    )


def world_step_reversed(distance: float, near: float, far: float) -> float:
    d0 = to_float32(reversed_depth(distance, near, far))
    d1 = next_float32_up(d0)
    return abs(
        distance_from_reversed_depth(d1, near, far)
        - distance_from_reversed_depth(d0, near, far)
    )


def main() -> None:
    near = 0.1
    far = 1_000_000.0
    sample = 10_000.0

    standard_step = world_step_standard(sample, near, far)
    reversed_step = world_step_reversed(sample, near, far)

    assert reversed_step < standard_step / 1000.0, (
        standard_step,
        reversed_step,
    )
    assert math.isclose(
        standard_depth(near, near, far),
        0.0,
        abs_tol=1e-9,
    )
    assert math.isclose(
        standard_depth(far, near, far),
        1.0,
        abs_tol=1e-9,
    )
    assert math.isclose(
        reversed_depth(near, near, far),
        1.0,
        abs_tol=1e-9,
    )
    assert math.isclose(
        reversed_depth(far, near, far),
        0.0,
        abs_tol=1e-9,
    )

    print(f"forward-Z world step at {sample:g}: {standard_step:.6g}")
    print(f"reversed-Z world step at {sample:g}: {reversed_step:.6g}")
    print("depth precision: PASS")


if __name__ == "__main__":
    main()
