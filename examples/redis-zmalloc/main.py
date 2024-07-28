from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.openai import OpenAIService
from manim_voiceover.services.gtts import GTTSService
from text import OpeningTitle, ChapterTitle, Content, Small, CodeBlock
from shape import RectWithText, FrameRect
from memory import Memory 

gtt_service = GTTSService(lang="zh-CN", tld="com", global_speed=1.25)

class Main(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        Opening.construct(self)
        WhatIsZmalloc.construct(self)
        HeadFile.construct(self)
        Implement.construct(self)
        ZmallocViz.construct(self)
        FreeImpl.construct(self)
        FreeViz.construct(self)
        Thanks.construct(self)

class Opening(VoiceoverScene):
    def construct(self):
        title = OpeningTitle("图解 Redis zmalloc 模块").scale(0.8)
        chap1 = ChapterTitle("什么是 zmalloc")
        self.play(Write(title))
        self.wait(3)
        self.play(Transform(title, chap1))
        self.wait(2)
        self.play(FadeOut(title))

class WhatIsZmalloc(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        redis_rect, redis_text = RectWithText(2, 1, "Redis")
        temp_rect = Rectangle(width=3, height=4)

        with self.voiceover(text="zmalloc 模块是 Redis 对标准库中内存管理函数的封装") as _:
            self.play(Write(redis_rect), Write(redis_text))
            self.play(
                Transform(redis_rect, temp_rect),
                redis_text.animate.shift(UP),
            )

            zmalloc_rect = Rectangle(width=2.5, height=1)
            zmalloc_text = Content("zmalloc")
            zmalloc_rect.next_to(redis_rect.get_bottom(), UP)
            zmalloc_text.move_to(zmalloc_rect.get_center())

            self.play(Write(zmalloc_rect), Write(zmalloc_text))

            std_rect, std_text = RectWithText(3, 4, "Standard\nLibrary")
            std_text.shift(UP)
            std_alloc_rect = Rectangle(width=2.5, height=1)
            std_alloc_text = Content("allocator")
            std_alloc_rect.next_to(std_rect.get_bottom(), UP)
            std_alloc_text.move_to(std_alloc_rect.get_center())

            redis_group = VGroup(redis_rect, redis_text, zmalloc_rect, zmalloc_text)
            std_group = VGroup(std_rect, std_text, std_alloc_rect, std_alloc_text)

            self.play(
                FadeIn(std_group),
                VGroup(redis_group, std_group).animate.arrange_in_grid(row=1, buff=4)
            )

            arrow = Arrow(
                start=zmalloc_rect.get_right(),
                end=std_alloc_rect.get_left(),
            )
            arrow_text = Small("调用")
            arrow_text.next_to(arrow.get_top(), UP * 0.2)
            self.play(FadeIn(arrow), FadeIn(arrow_text))

            self.wait(1)
        
        # --- --- --- --- --- ---

        adlist = VGroup(*RectWithText(3, 1, "adlist"))
        dict_ = VGroup(*RectWithText(3, 1, "dict"))
        sds = VGroup(*RectWithText(3, 1, "sds"))
        more = VGroup(*RectWithText(3, 1, "..."))
        module_group = VGroup(adlist, dict_, sds, more)
        module_group.arrange(DOWN)
        module_group.move_to(std_rect.get_center())
        arrows = [Arrow(
            end=(zmalloc_rect.get_right() - UP * 0.2 * (i - 1)),
            start=([adlist, dict_, sds, more])[i].get_left()
        ) for i in range(4)]

        temp_rect = Rectangle(width=12, height=6)
        with self.voiceover(text="Redis 内部的动态内存分配均依赖于此模块") as _:
            self.play(
                Transform(redis_rect, temp_rect),
                Transform(std_group, module_group),
                Transform(arrow, VGroup(*arrows)),
                FadeOut(arrow_text),
            )
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)

class HeadFile(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        headfile = CodeBlock('''\
        #ifndef _ZMALLOC_H
        #define _ZMALLOC_H

        void *zmalloc(size_t size);
        void *zrealloc(void *ptr, size_t size);
        void zfree(void *ptr);
        char *zstrdup(const char *s);
        size_t zmalloc_used_memory(void);

        #endif /* _ZMALLOC_H */
        ''', "c")

        title = ChapterTitle("zmalloc 头文件")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(1)

        with self.voiceover(text="让我们先从 zmalloc 的头文件入手") as _:
            self.play(Write(headfile))

        with self.voiceover(text="在这些函数中，最重要的就是 zmalloc 和 zfree 这两个函数") as _:
            self.wait(1)
            self.play(headfile.highlight_line_list([3, 5]))
        with self.voiceover(text="接下来，让我们着眼于这两个函数，解析 zmalloc 模块的实现") as _: pass
        self.play(FadeOut(headfile))
        self.wait(1)

class Implement(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        title = ChapterTitle("zmalloc 实现")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(1)

        code_image = ImageMobject("code.png")
        code_image.scale_to_fit_width(config.frame_width)
        clipping_rect = FrameRect()
        code_image.next_to(clipping_rect.get_top(), DOWN)
        self.play(FadeIn(code_image))
        self.play(code_image.animate.next_to(clipping_rect.get_bottom(), UP))
        self.wait(0.5)
        self.play(FadeOut(code_image))

        used_memory = CodeBlock('''\
        static size_t used_memory = 0;

        size_t zmalloc_used_memory(void) {
            return used_memory;
        }
        ''', "c")
        with self.voiceover(text="我们先通过这个部分介绍一下 Redis 封装 zmalloc 模块的目的") as _:
            self.play(Write(used_memory))

        with self.voiceover(text="这里定义了一个模块私有的静态变量") as _:
            self.play(*used_memory.highlight_line(0))
        with self.voiceover(text="这个函数则用于在模块外部访问该私有变量") as _:
            self.play(*used_memory.highlight_lines(2, 5))

        self.play(*used_memory.cancel_highlight())
        with self.voiceover(text="这部分代码的作用就如这个静态变量的名字一样") as _: pass
        with self.voiceover(text="用于记录程序进行动态内存分配的内存总大小。") as _: pass

        zmalloc = CodeBlock('''\
        void *zmalloc(size_t size) {
            void *ptr = malloc(size+sizeof(size_t));

            if (!ptr) return NULL;
        #ifdef HAVE_MALLOC_SIZE
            used_memory += redis_malloc_size(ptr);
            return ptr;
        #else
            *((size_t*)ptr) = size;
            used_memory += size+sizeof(size_t);
            return (char*)ptr+sizeof(size_t);
        #endif
        }
        ''', "c")
        zmalloc_without_macro = CodeBlock('''\
        void *zmalloc(size_t size) {
            void *ptr = malloc(size+sizeof(size_t));

            if (!ptr) return NULL;
            *((size_t*)ptr) = size;
            used_memory += size+sizeof(size_t);
            return (char*)ptr+sizeof(size_t);
        }
        ''', "c")
        with self.voiceover(text="接下来，就要正式开始解析 zmalloc 的实现了") as _:
            self.play(ReplacementTransform(used_memory, zmalloc))
        with self.voiceover(text="我们先把无关紧要的预处理指令去掉方便阅读") as _:
            self.wait(1)
            self.play(ReplacementTransform(zmalloc, zmalloc_without_macro))

        with self.voiceover(text="第一行代码调用了标准库的 malloc 进行内存分配") as _:
            self.play(*zmalloc_without_macro.highlight_line(1))
        with self.voiceover(text="这里额外分配了一个 size_t 大小的内存，原因下面会介绍") as _: pass
        with self.voiceover(text="第三行处对 malloc 返回的指针进行判断，处理内存分配失败的情况") as _:
            self.play(*zmalloc_without_macro.highlight_line(3))
        with self.voiceover(text="第四行将指针看作 size_t 类型的指针向其指向的内存存入 size 的值") as _:
            self.play(*zmalloc_without_macro.highlight_line(4))
        with self.voiceover(text="size 即为 zmalloc 函数调用方实际需要的内存大小") as _: pass
        with self.voiceover(text="第五行更新了 used_memory 的值") as _:
            self.play(*zmalloc_without_macro.highlight_line(5))
        with self.voiceover(text="由于在分配内存时进行了额外分配") as _: pass
        with self.voiceover(text="这里要将额外分配的内存大小也加上") as _: pass
        with self.voiceover(text="最后一行，将指针转为 char 指针") as _:
            self.play(*zmalloc_without_macro.highlight_line(6))
        with self.voiceover(text="进行指针操作后，经过隐式转换为 void 指针后返回") as _:
            self.wait(1)
            self.play(*zmalloc_without_macro.cancel_highlight())

        with self.voiceover(text="仍然迷糊？其实我第一次读完这段代码时也这样。") as _: pass
        with self.voiceover(text="让我们用可视化的方式再来看一遍这个过程") as _:
            self.play(FadeOut(zmalloc_without_macro))

class ZmallocViz(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        frame = FrameRect()
        self.add(frame)

        kbs = Text("32 Bytes")
        with self.voiceover(text="假设现在，我们需要分配一块32字节大小的内存") as _:
            self.play(FadeIn(kbs))
        with self.voiceover(text="让我们把每个方块看作8个字节") as _:
            self.wait(1)
            self.play(FadeOut(kbs))

        squares = VGroup(*[Square() for _ in range(4)])
        squares.arrange(RIGHT)
        extra_square = Square()
        extra_square.next_to(squares.submobjects[-1], RIGHT)
        with self.voiceover(text="这是 zmalloc 调用方需要的内存") as _:
            self.play(Create(squares))
        with self.voiceover(text="我们再额外分配 size_t 大小的内存") as _:
            comment = Small("*对于64位的操作系统，为8字节")
            comment.next_to(frame.get_corner(UP + RIGHT), LEFT + DOWN)
            self.play(Write(comment))
            self.play(Create(extra_square))

            squares.add(extra_square)
            self.play(squares.animate.arrange(RIGHT))
            self.play(FadeOut(comment))

        temp = squares.submobjects[0].get_corner(LEFT + DOWN)
        pointer = Arrow(start=temp + DOWN * 2, end=temp)
        pointer.set_opacity(0).shift(DOWN * 2)
        with self.voiceover(text="现在我们有一根 size_t 的指针") as _:
            self.play(pointer.animate.set_opacity(1).shift(UP * 2))
        
        size = Content("size")
        size.move_to(squares.submobjects[0].get_center())
        with self.voiceover(text="向该指针所指的内存写入 size 的值") as _: pass
        with self.voiceover(text="由于该指针的类型，这只会在指针所指地址往后大小为 size_t 的空间内写入") as _:
            self.play(squares.submobjects[0].animate.set_color(RED))
            self.wait(1)
            self.play(Write(size))
            self.wait(1)
            self.play(squares.submobjects[0].animate.set_color(WHITE))

        Memory.construct(self)

        with self.voiceover(text="在返回指针时，为防止刚刚写入的 size 信息被覆盖") as _:
            self.wait(1)
            self.play(VGroup(size, squares.submobjects[0]).animate.set_color(RED))
            self.play(VGroup(size, squares.submobjects[0]).animate.set_color(WHITE))
        with self.voiceover(text="我们需要进行指针操作") as _:
            self.play(pointer.animate.next_to(squares.submobjects[1].get_corner(LEFT + DOWN), DOWN))
        with self.voiceover(text="这样，函数调用方在写入这块内存时就不会覆盖 size 信息") as _:
            msgs = [Content("* * *") for _ in range(4)]
            for msg, square in zip(msgs, squares.submobjects[1:]):
                msg.move_to(square.get_center())
                self.play(pointer.animate.next_to(square.get_corner(LEFT + DOWN), DOWN))
                self.play(Write(msg))
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))

class FreeImpl(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        title = ChapterTitle("zfree 实现")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        self.wait(1)

        zfree = CodeBlock('''\
        void zfree(void *ptr) {
        #ifndef HAVE_MALLOC_SIZE
            void *realptr;
            size_t oldsize;
        #endif

            if (ptr == NULL) return;
        #ifdef HAVE_MALLOC_SIZE
            used_memory -= redis_malloc_size(ptr);
            free(ptr);
        #else
            realptr = (char*)ptr-sizeof(size_t);
            oldsize = *((size_t*)realptr);
            used_memory -= oldsize+sizeof(size_t);
            free(realptr);
        #endif
        }
        ''', "c", font_size=20)
        zfree_recomposed = CodeBlock('''\
        void zfree(void *ptr) {
            if (ptr == NULL) return;

            void *realptr = (char*)ptr-sizeof(size_t);
            size_t oldsize = *((size_t*)realptr);
            used_memory -= oldsize+sizeof(size_t);

            free(realptr);
        }
        ''', "c")

        with self.voiceover(text="接下来，让我们开始解析 zfree 函数的实现") as _:
            self.play(Write(zfree))
        with self.voiceover(text="我们先把无关紧要的预处理指令去掉") as _:
            self.play(ReplacementTransform(zfree, zfree_recomposed))

        with self.voiceover(text="第一行代码过滤值为 NULL 的输入") as _:
            self.play(*zfree_recomposed.highlight_line(1))
        with self.voiceover(text="第三行进行指针运算，获取调用 zmalloc 时实际返回的指针") as _:
            self.play(*zfree_recomposed.highlight_line(3))
        with self.voiceover(text="第四行读取执行 zmalloc 时存的 size 的值") as _:
            self.play(*zfree_recomposed.highlight_line(4))
        with self.voiceover(text="第五行更新 used_memory 的值") as _:
            self.play(*zfree_recomposed.highlight_line(5))
        with self.voiceover(text="最后调用标准库中的 free 函数释放内存") as _:
            self.play(*zfree_recomposed.highlight_line(7))

        self.wait(1)
        self.play(FadeOut(zfree_recomposed))

class FreeViz(VoiceoverScene):
    def construct(self):
        self.set_speech_service(gtt_service)
        squares = VGroup(*[Square() for _ in range(5)])
        squares.arrange(RIGHT)
        temp = squares.submobjects[1].get_corner(LEFT + DOWN)
        pointer = Arrow(start=temp + DOWN * 2, end=temp)
        size = Content("size")
        text_list = [Content("* * *") for _ in range(4)]
        size.move_to(squares.submobjects[0].get_center())
        for text, square in zip(text_list, squares.submobjects[1:]):
            text.move_to(square.get_center())

        with self.voiceover(text="同样地，让我们再用可视化的方式看一遍这个过程") as _:
            self.play(Create(squares))
            self.play(
                Create(pointer),
                Write(size),
                Write(VGroup(*text_list)),
            )

        with self.voiceover(text="先将指针左移以获取 zmalloc 内部调用 malloc 时获得的指针") as _:
            self.play(pointer.animate.next_to(
                squares.submobjects[0].get_corner(LEFT + DOWN),
                DOWN,
            ))

        temp_size = Content("size").move_to(size.get_center())
        self.add(temp_size)
        with self.voiceover(text="读取 size 的值，并加上 size_t 所占空间，更新 used_memory 的值") as _:
            self.play(temp_size.animate.move_to(DOWN * 2))
            temp = Content("32 + 8").move_to(DOWN * 2)
            self.play(Transform(temp_size, temp))
            temp = Content("40").move_to(DOWN * 2)
            self.play(Transform(temp_size, temp))
        with self.voiceover(text="最后再调用 free 函数释放内存") as _:
            self.wait(1)
            self.play(FadeOut(temp_size))
            self.play(
                FadeOut(squares),
                FadeOut(size),
                FadeOut(VGroup(*text_list)),
            )
            self.play(FadeOut(pointer))

class Thanks(VoiceoverScene):
    def construct(self):
        self.wait(2)
        thanks = ChapterTitle("感谢观看！")
        self.play(Write(thanks))
        self.wait(4)
