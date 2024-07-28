from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from manim_voiceover.services.gtts import GTTSService
from text import OpeningTitle, ChapterTitle, Content, Small, CodeBlock
from shape import RectWithText, FrameRect

gtt_service = GTTSService(lang="zh-CN", tld="com", global_speed=1.25)

class Memory(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        frame = Rectangle(
            width=config.frame_width - 2,
            height=config.frame_height - 1,
        )
        frame.set_fill(BLACK, 1)
        squares = VGroup(*[Square(1) for _ in range(8)])
        squares.arrange(RIGHT)

        with self.voiceover(text="让我们以一小段动画来说明指针类型与内存读写的联系") as _:
            self.play(Create(frame))
        with self.voiceover(text="现在这里有8字节的内存空间") as _:
            comment = Small("*把一个小方块看作1字节")
            comment.next_to(frame.get_corner(UP + RIGHT), LEFT * 0.5 + DOWN * 0.5)
            self.play(
                FadeIn(squares),
                Write(comment)
            )
        self.play(FadeOut(comment))

        with self.voiceover(text="我们先向其中写入值 81985529216486895") as _:
            comment = Small("*即16进制 0x123456789ABCDEF")
            comment.next_to(frame.get_corner(UP + RIGHT), LEFT * 0.5 + DOWN * 0.5)
            self.play(Write(comment))
        self.play(FadeOut(comment))

        values = ["EF", "CD", "AB", "89", "67", "45", "23", "01"]
        with self.voiceover(text="由于我们的电脑使用小端序存储，因此在内存中会像这样排列") as _:
            text_list = []
            for index, value in enumerate(values):
                square = squares.submobjects[index]
                value_text = Content(value)
                value_text.move_to(square.get_center())
                text_list.append(value_text)
            self.play(Write(VGroup(*text_list)))

        temp = squares.submobjects[0].get_corner(LEFT + DOWN)
        pointer = Arrow(start=temp + DOWN * 2, end=temp)
        pointer_text = Content("unsigned char")
        pointer_text.add_updater(lambda mob: mob.next_to(pointer.get_right()))
        pointer_text.next_to(pointer.get_right())
        with self.voiceover(text="这里有一根 unsigned char 的指针") as _:
            self.play(Create(pointer), Write(pointer_text))
        with self.voiceover(text="由于 unsigned char 类型占据1字节，该指针能够读写第一个方格内的值") as _:
            for _ in range(3):
                self.play(squares.submobjects[0].animate.set_color(RED))
                self.play(squares.submobjects[0].animate.set_color(WHITE))
        with self.voiceover(text="同理，对于 unsigned short 类型的指针：") as _:
            new_text = Content("unsigned short").next_to(pointer.get_right())
            self.play(Transform(pointer_text, new_text))
            for _ in range(3):
                self.play(
                    squares.submobjects[0].animate.set_color(RED),
                    squares.submobjects[1].animate.set_color(RED)
                )
                self.play(
                    squares.submobjects[0].animate.set_color(WHITE),
                    squares.submobjects[1].animate.set_color(WHITE)
                )
        with self.voiceover(text="对于 unsigned int 类型的指针：") as _:
            new_text = Content("unsigned int").next_to(pointer.get_right())
            self.play(Transform(pointer_text, new_text))
            for _ in range(3):
                self.play(*[
                    squares.submobjects[index].animate.set_color(RED)
                    for index in range(4)
                ])
                self.play(*[
                    squares.submobjects[index].animate.set_color(WHITE)
                    for index in range(4)
                ])
        self.wait(1)

        with self.voiceover(text="对指针进行运算也是类似") as _: pass
        with self.voiceover(text="以 char 类型指针为例") as _:
            new_text = Content("char").next_to(pointer.get_right(), RIGHT)
            self.play(Transform(pointer_text, new_text))

        with self.voiceover(text="假如我们对指针加一") as _: pass
        with self.voiceover(text="由于 char 类型占据1字节，指针会向右移1字节") as _:
            self.play(pointer.animate.next_to(squares.submobjects[1].get_corner(LEFT + DOWN), DOWN))
        with self.voiceover(text="类似地，short 指针会向右移2字节") as _:
            new_text = Content("short").next_to(pointer.get_right(), RIGHT)
            self.play(Transform(pointer_text, new_text))
            self.play(pointer.animate.next_to(squares.submobjects[3].get_corner(LEFT + DOWN), DOWN))
        with self.voiceover(text="int 指针会向右移4字节") as _:
            new_text = Content("int").next_to(pointer.get_right(), RIGHT)
            self.play(Transform(pointer_text, new_text))
            self.play(pointer.animate.next_to(squares.submobjects[7].get_corner(LEFT + DOWN), DOWN))


        self.wait(1)
        self.play(FadeOut(VGroup(*[
            frame,
            squares,
            *text_list,
            pointer,
            pointer_text,
        ])))

