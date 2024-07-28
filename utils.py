from manim.typing import Point3D

def point_eq(
    p1: Point3D,
    p2: Point3D,
    precise: float = 0.1,
) -> bool:
    return (
        abs(p1[0] - p2[0]) < precise and
        abs(p1[1] - p2[1]) < precise and
        abs(p1[2] - p2[2]) < precise
    )
