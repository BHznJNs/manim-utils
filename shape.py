from manim import *
from manim.typing import Vector3D
from text import Content

def FrameRect() -> Rectangle:
    rect = Rectangle(
        width=config.frame_width,
        height=config.frame_height,
    )
    rect.set_opacity(0)
    return rect

def RectWithText(
    width: float,
    height: float,
    text: str,
    **kwargs,
) -> tuple[Rectangle, Text]:
    rect = Rectangle(width=width, height=height, **kwargs)
    inner_text = Content(text)
    inner_text.move_to(rect.get_center())
    return rect, inner_text

def SquareWithText(size: float, text: str) -> tuple[Rectangle, Text]:
    return RectWithText(size, size, text)

def HeadOnlyArrow(
    position: Vector3D,
    direction: Vector3D,
) -> Arrow:
    FACTOR = 100
    return Arrow(
        start=position,
        end=position + direction / FACTOR,
        max_tip_length_to_length_ratio=FACTOR,
    )
