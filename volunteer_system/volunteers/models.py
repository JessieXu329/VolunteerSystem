from django.db import models

class Activity(models.Model):
    # 原有字段
    title = models.CharField(max_length=100, verbose_name="活动名称")
    description = models.TextField(verbose_name="活动描述")
    date = models.DateTimeField(verbose_name="活动日期")
    location = models.CharField(max_length=200, verbose_name="活动地点")
    slots = models.PositiveIntegerField(verbose_name="招募人数")
    
    # 新增筛选字段
    CATEGORY_CHOICES = [
        ('education', '教育'),
        ('environment', '环保'),
        ('health', '医疗健康'),
        ('community', '社区服务'),
        ('other', '其他'),
    ]
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other',
        verbose_name="活动类别"
    )
    is_active = models.BooleanField(default=True, verbose_name="活动有效")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return self.title

class Volunteer(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    phone = models.CharField(max_length=15, verbose_name="电话")
    notes = models.TextField(blank=True, null=True, verbose_name="备注")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="报名活动")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="报名时间")
    
    def __str__(self):
        return f"{self.name} - {self.activity.title}"