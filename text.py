from manim import *

DEFAULT_FONT = "Microsoft YaHei"

def OpeningTitle(text: str):
    return Text(text, font=DEFAULT_FONT).scale(2)

def ChapterTitle(text: str):
    return Text(text, font=DEFAULT_FONT).scale(1.25)

def Content(*text_list: List[str]):
    if len(text_list) == 1:
        return Text(text_list[0], font=DEFAULT_FONT).scale(0.8)
    else:
        return Paragraph(*text_list, line_spacing=0.75, font=DEFAULT_FONT).scale(0.75)

def Small(text: str):
    return Text(text, font=DEFAULT_FONT).scale(0.6)

class CodeBlock(Code):
    HIGHLIGHT_OPACITY = 1
    DIM_OPACITY = 0.4

    def __init__(self, code: str, lang: str, **kwargs):
        # new_string = ''.join(char for char in code if char in printable)
        super().__init__(
            code=code,
            language=lang,
            tab_width=4,
            line_spacing=1,
            background="window",
            insert_line_no=False,
            style="github-dark",
            font="Consolas",
            **kwargs,
        )
    
    def highlight_line(self, index: int):
        lines = self.code
        animations = []
        for i, line in enumerate(lines):
            if i == index:
                animations.append(line.animate.set_opacity(CodeBlock.HIGHLIGHT_OPACITY))
            else:
                animations.append(line.animate.set_opacity(CodeBlock.DIM_OPACITY))
        return animations

    def highlight_line_list(self, list: List[int]):
        lines = self.code
        animations =\
        [line.animate.set_opacity(CodeBlock.DIM_OPACITY) for line in lines] +\
        [lines[i].animate.set_opacity(CodeBlock.HIGHLIGHT_OPACITY) for i in list]
        return animations

    def highlight_lines(self, start: int, end: int):
        lines = self.code
        animations = []
        for i, line in enumerate(lines):
            if start <= i < end:
                animations.append(line.animate.set_opacity(CodeBlock.HIGHLIGHT_OPACITY))
            else:
                animations.append(line.animate.set_opacity(CodeBlock.DIM_OPACITY))
        return animations

    def cancel_highlight(self):
        lines = self.code
        animations = [
            line.animate.set_opacity(CodeBlock.HIGHLIGHT_OPACITY)
            for line in lines
        ]
        return animations
