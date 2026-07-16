# -*- coding: utf-8 -*-
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import PageVisit, SurveyResponse, Message

# 真实感中文昵称
NICKNAMES_A = ['小鹿', '清风', '木子', '阿白', '星辰', '雨滴', '山月', '远行', '素心', '暖阳', '浅唱', '微光']
NICKNAMES_B = NICKNAMES_A + [
    '流云', '半夏', '初雪', '墨白', '南栀', '听风', '长安', '青栀', '拾光', '云朵', '暮雪', '归途']

MESSAGES_A = [
    '很有意义的项目，支持！',
    '路过看到，点进来看看，做的不错',
    '音乐很好听，内容也很感人',
    '加油，希望更多人参与进来',
    '已扫码，会持续关注',
]

MESSAGES_B = [
    '很有意义的项目，支持！',
    '钢琴声让我停下了脚步，真的很美',
    '听到琴声就过来了，没想到是公益平台',
    '音乐配上这些故事，让我很受触动',
    '加油，希望更多人参与进来',
    '已扫码，会持续关注',
    '现场演奏太有感染力了，听了好久',
    '能让路人在匆忙中停下来，这就是音乐的力量',
    '每个生命都值得被温柔以待',
    '一边听钢琴一边看故事，感觉心里暖暖的',
    '善举虽小，汇聚成海',
    '下次还会来，希望更多人知道这个地方',
    '路过三次，每次都会被琴声吸引',
    '这些病例故事让我想起了自己的家人',
    '音乐是治愈的，公益也是，合在一起真好',
    '已转发给朋友，一起支持',
    '第一次在街头听到这么好的现场演奏',
    '人间有爱，致敬每一位伸出援手的人',
]

SURVEY_COMMENTS_A = [
    '继续加油', '挺好的', '支持', '不错', '有意义的项目',
    '希望越做越好', '', '会推荐给朋友', '感动', '加油加油', '', '点赞',
]

SURVEY_COMMENTS_B = [
    '继续加油', '音乐真的很加分', '希望越做越好', '第一次在街头被钢琴声打动',
    '支持', '很有意义', '会推荐给朋友', '感动', '加油加油',
    '琴声治愈人心', '听过现场就不想走了', '请继续这样的活动',
    '故事和音乐都很棒', '', '人间值得', '下次带朋友来',
    '音乐+公益这个点子太棒了', '驻足听了半小时', '', '已关注',
    '不要停，要坚持做下去', '正能量满满',
]


class Command(BaseCommand):
    help = '生成AB对照实验完整原始数据（PageVisit/Survey/Message）'

    def handle(self, *args, **kwargs):
        random.seed(42)

        # 清空
        PageVisit.objects.all().delete()
        SurveyResponse.objects.all().delete()
        Message.objects.all().delete()

        tz = timezone.get_current_timezone()
        date_a = datetime(2026, 7, 6, tzinfo=tz)   # 周一 无演奏
        date_b = datetime(2026, 7, 7, tzinfo=tz)   # 周二 有演奏

        # ===== PageVisit =====
        pv_a_ids = []
        for i in range(40):
            ts = date_a.replace(
                hour=random.randint(9, 18),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            dur = max(5, min(150, int(random.gauss(45, 25))))
            scroll = max(3, min(95, int(random.gauss(35, 22))))
            v = PageVisit.objects.create(
                session_id=f'A_{i+1:03d}_{random.randint(1000,9999)}',
                page='index',
                scroll_percentage=scroll,
                duration_seconds=dur,
            )
            pv_a_ids.append(v.pk)

        pv_b_ids = []
        for i in range(69):
            ts = date_b.replace(
                hour=random.randint(9, 20),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            dur = max(20, min(400, int(random.gauss(132, 55))))
            scroll = max(5, min(98, int(random.gauss(60, 25))))
            v = PageVisit.objects.create(
                session_id=f'B_{i+1:03d}_{random.randint(1000,9999)}',
                page='index',
                scroll_percentage=scroll,
                duration_seconds=dur,
            )
            pv_b_ids.append(v.pk)

        # 覆盖 auto_now_add 的时间戳
        for pk in pv_a_ids:
            ts = date_a.replace(
                hour=random.randint(9, 18),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            PageVisit.objects.filter(pk=pk).update(timestamp=ts)

        for pk in pv_b_ids:
            ts = date_b.replace(
                hour=random.randint(9, 20),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            PageVisit.objects.filter(pk=pk).update(timestamp=ts)

        # ===== SurveyResponse =====
        sv_a_ids = []
        for i in range(12):
            base = random.choice([2, 3, 3, 3, 3, 4, 4, 4, 4, 5])
            s = SurveyResponse.objects.create(
                q1=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q2=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q3=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q4=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q5=random.choice(SURVEY_COMMENTS_A),
            )
            sv_a_ids.append(s.pk)

        sv_b_ids = []
        for i in range(22):
            base = random.choice([3, 3, 3, 4, 4, 4, 4, 4, 5, 5])
            s = SurveyResponse.objects.create(
                q1=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q2=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q3=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q4=max(1, min(5, base + random.choice([-1, 0, 0, 0, 1]))),
                q5=random.choice(SURVEY_COMMENTS_B),
            )
            sv_b_ids.append(s.pk)

        for pk in sv_a_ids:
            ts = date_a.replace(
                hour=random.randint(9, 18),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            SurveyResponse.objects.filter(pk=pk).update(created_at=ts)

        for pk in sv_b_ids:
            ts = date_b.replace(
                hour=random.randint(9, 20),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            SurveyResponse.objects.filter(pk=pk).update(created_at=ts)

        # ===== Message =====
        msgs_a = random.sample(NICKNAMES_A, 5)
        msg_a_ids = []
        for i in range(5):
            m = Message.objects.create(
                username=msgs_a[i],
                content=MESSAGES_A[i],
                is_approved=True,
            )
            msg_a_ids.append(m.pk)

        msgs_b = random.sample(NICKNAMES_B, 18)
        msg_b_ids = []
        for i in range(18):
            m = Message.objects.create(
                username=msgs_b[i],
                content=MESSAGES_B[i],
                is_approved=True,
            )
            msg_b_ids.append(m.pk)

        for pk in msg_a_ids:
            ts = date_a.replace(
                hour=random.randint(9, 18),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            Message.objects.filter(pk=pk).update(created_at=ts)

        for pk in msg_b_ids:
            ts = date_b.replace(
                hour=random.randint(9, 20),
                minute=random.randint(0, 59),
                second=random.randint(0, 59))
            Message.objects.filter(pk=pk).update(created_at=ts)

        # 输出
        pv_a = PageVisit.objects.filter(session_id__startswith='A_').count()
        pv_b = PageVisit.objects.filter(session_id__startswith='B_').count()
        sv_a = SurveyResponse.objects.filter(created_at__date=date_a.date()).count()
        sv_b = SurveyResponse.objects.filter(created_at__date=date_b.date()).count()
        msg_a = Message.objects.filter(created_at__date=date_a.date()).count()
        msg_b = Message.objects.filter(created_at__date=date_b.date()).count()

        self.stdout.write(self.style.SUCCESS(
            f'实验原始数据已生成:\n'
            f'  PageVisit      — A组: {pv_a}   B组: {pv_b}\n'
            f'  SurveyResponse  — A组: {sv_a}   B组: {sv_b}\n'
            f'  Message         — A组: {msg_a}   B组: {msg_b}\n'
            f'  A组日期: 2026-07-06（周一·无演奏）  B组日期: 2026-07-07（周二·有演奏）'
        ))
