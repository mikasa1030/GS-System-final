from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', '等待中'),
        ('processing', '进行中'),
        ('completed', '已完成'),
        ('failed', '失败'),
    ]
    
    MODE_CHOICES = [
        ('normal', '常规'),
        ('derain', '去雨'),
    ]

    name = models.CharField(max_length=255, verbose_name="任务名称")
    dataset = models.CharField(max_length=255, verbose_name="数据集")
    scene = models.CharField(max_length=255, verbose_name="场景")
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='normal', verbose_name="模式")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='processing', verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    # For result
    model_path = models.CharField(max_length=1024, blank=True, null=True, verbose_name="模型路径")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "重建任务"
        verbose_name_plural = "重建任务"

    def __str__(self):
        return self.name

class Annotation(models.Model):
    TYPE_CHOICES = [
        ('point', '点选'),
        ('box', '框选'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='annotations', null=True, blank=True)
    dataset = models.CharField(max_length=255)
    scene = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    data = models.JSONField(verbose_name="标注数据") # Store coordinates {x, y} or {startX, startY, ...}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "标注记录"
        verbose_name_plural = "标注记录"
