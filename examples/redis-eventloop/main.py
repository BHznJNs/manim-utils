from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from manim_voiceover.services.gtts import GTTSService
from text import OpeningTitle, ChapterTitle, Content, Small, CodeBlock
from shape import RectWithText, FrameRect

gtt_service = GTTSService(lang="zh-CN", tld="com", global_speed=1.25)

class Main(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        PreCaution.construct(self)

class PreCaution(VoiceoverScene):
    def construct(self):
        warning = ChapterTitle("观前提示")
        content = Content(
            "本视频需要你具备一定的：",
            "- C 语言基础",
            "- socket 编程知识",
        )
        group = VGroup(warning, content).arrange(DOWN)
        self.play(Write(group))
        self.wait(3)
        self.play(FadeOut(group))
        self.wait(1)

class Opening(VoiceoverScene):
    def construct(self):
        title = OpeningTitle("Redis 事件循环\n运行机制可视化").scale(0.8)
        chap1 = ChapterTitle("什么是事件循环")
        self.play(Write(title))
        self.wait(3)
        self.play(ReplacementTransform(title, chap1))
        self.wait(2)
        self.play(FadeOut(chap1))

class Introduction(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)

        content_text = [
            "事件循环是 Redis 内部的任务调度中心，",
            "它由 Redis 源码中的 ae 模块实现。",
            "ae 即 async event，异步事件。",
            "由此我们可以一窥这一模块的作用。",
        ]

        with self.voiceover(text="".join(content_text)) as _:
            content1 = Content(*content_text)
            self.play(Write(content1))
        self.play(FadeOut(content1))

        with self.voiceover(text="事件循环，顾名思义即“事件”加循环") as _:
            eventloop = ChapterTitle("事件循环")
            temp_text = ChapterTitle("\"事件\" + \"循环\"")
            self.play(Write(eventloop))
            self.wait(1.5)
            self.play(Transform(eventloop, temp_text))

        with self.voiceover(text="所以我们接下来会从事件和循环两个角度") as _: pass
        with self.voiceover(text="来介绍事件循环模块的实现。") as _: pass
        self.play(FadeOut(eventloop))
        self.wait(1)

class Events(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        title = ChapterTitle("事件")
        self.play(Write(title))
        self.wait(2)

        file_event = Content("文件事件")
        time_event = Content("时间事件")
        with self.voiceover(text="Redis 中的事件分为文件事件和时间事件") as _:
            event_group = VGroup(file_event, time_event).arrange(RIGHT, buff=4)
            self.play(ReplacementTransform(title, event_group))

        with self.voiceover(text="其中，文件事件主要负责处理网络 爱哦", subcaption="其中，文件事件主要负责处理网络 I/O") as _:
            self.play(file_event.animate.shift(UP))
            file_event_usage = Small("网络 I/O").next_to(file_event, DOWN)
            self.play(Write(file_event_usage))

        with self.voiceover(text="而时间事件则负责以一定的间隔反复执行特定任务") as _: pass
        with self.voiceover(text="如打日志，") as _:
            self.play(time_event.animate.shift(UP))
            log = Small("日志").next_to(time_event, DOWN)
            self.play(Write(log))
        with self.voiceover(text="进行数据持久化存储，") as _:
            persistence = Small("持久化").next_to(log, DOWN)
            self.play(Write(persistence))
        with self.voiceover(text="关闭超时连接等，") as _:
            clean = Small("处理超时").next_to(persistence, DOWN)
            self.play(Write(clean))
        
        self.wait(2)
        self.play(FadeOut(VGroup(*self.mobjects)))
        self.wait(2)

class Loop(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        title = ChapterTitle("循环")
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        with self.voiceover(text="让我们先看看 ae 模块的入口函数") as _:
            code = CodeBlock('''\
            // ae.c
            void aeMain(aeEventLoop *eventLoop) {
                eventLoop->stop = 0;
                while (!eventLoop->stop)
                    aeProcessEvents(eventLoop, AE_ALL_EVENTS);
            }''', "c")
            self.play(Create(code))
        with self.voiceover(text="不难看出，事件循环和普通的循环没有太大区别") as _: pass
        with self.voiceover(text="其实现的关键就在于第5行的 aeProcessEvents") as _:
            self.play(code.highlight_line(4))
        with self.voiceover(text="接下来，就让我们用可视化的方式来看看事件循环的运行机制") as _: pass

class EventLoopViz(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        loop_rect = RoundedRectangle(
            corner_radius=0.5,
            width =config.frame_width  - 2,
            height=config.frame_height - 4,
            color=BLUE,
        )
