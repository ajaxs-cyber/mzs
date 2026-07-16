# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import ExperimentMetric


class Command(BaseCommand):
    help = '导入AB对照实验数据（钢琴演奏 vs 无钢琴演奏）'

    def handle(self, *args, **kwargs):
        ExperimentMetric.objects.all().delete()

        data = [
            (1, '路过人数', '500', '510'),
            (2, '驻足人数', '60', '94'),
            (3, '驻足率', '12.0%', '18.4%'),
            (4, '扫码人数', '40', '69'),
            (5, '扫码率', '8.0%', '13.5%'),
            (6, '访客数', '40', '69'),
            (7, '停留时长', '45 秒', '132 秒'),
            (8, '问卷人数', '12', '22'),
            (9, '问卷完成率', '30.0%', '31.9%'),
            (10, '留言人数', '5', '18'),
            (11, '留言率', '12.5%', '26.1%'),
        ]

        for order, name, val_a, val_b in data:
            ExperimentMetric.objects.create(
                metric_name=name,
                value_a=val_a,
                value_b=val_b,
                order=order,
            )

        self.stdout.write(self.style.SUCCESS(
            f'已导入 {len(data)} 条AB对照实验数据'
        ))
