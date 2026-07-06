from django.db import models


class Case(models.Model):
    """成功救助病例"""
    title = models.CharField(max_length=100, verbose_name="病例标题")
    name = models.CharField(max_length=50, verbose_name="患者称呼")
    disease = models.CharField(max_length=100, verbose_name="病情")
    story = models.TextField(verbose_name="救助故事")
    result = models.TextField(verbose_name="救助结果")
    image = models.ImageField(upload_to='cases/', verbose_name="照片")
    order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "救助病例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name} - {self.disease}"


class Message(models.Model):
    """留言板"""
    username = models.CharField(max_length=50, default="匿名", verbose_name="昵称")
    content = models.TextField(verbose_name="留言内容")
    is_approved = models.BooleanField(default=True, verbose_name="审核通过")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="留言时间")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.username}: {self.content[:30]}"


class SurveyResponse(models.Model):
    """反馈问卷"""
    q1 = models.IntegerField(verbose_name="这个页面让我愿意继续了解公益内容")
    q2 = models.IntegerField(verbose_name="我认为音乐与公益结合是有意义的")
    q3 = models.IntegerField(verbose_name="我愿意进一步了解这个平台")
    q4 = models.IntegerField(verbose_name="我愿意参与类似公益活动")
    q5 = models.TextField(verbose_name="请留下一句话", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        verbose_name = "问卷回复"
        verbose_name_plural = verbose_name


class PageVisit(models.Model):
    """页面访问追踪"""
    session_id = models.CharField(max_length=100, verbose_name="会话ID")
    page = models.CharField(max_length=50, verbose_name="页面")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")
    scroll_percentage = models.IntegerField(default=0, verbose_name="滚动百分比")
    duration_seconds = models.IntegerField(default=0, verbose_name="停留时长(秒)")

    class Meta:
        verbose_name = "页面访问"
        verbose_name_plural = verbose_name
