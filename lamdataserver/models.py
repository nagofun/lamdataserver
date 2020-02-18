# -*- coding: gbk -*-

from django.db import models

# Create your models here.
#
# class Gender(models.Model):
# 	name = models.CharField(max_length=32)
#
#
# class userinfo(models.Model):
# 	nid = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=30, verbose_name='用户名', editable=False)
# 	# email = models.EmailField(db_index=True)
# 	# memo = models.TextField()
# 	# img = models.ImageField(upload_to='upload')
# 	user_type = models.ForeignKey("UserType", null=True, blank=True)
# 	gender_choices = (
# 		(0, "男"),
# 		(1, "女"),
# 	)
# 	gender = models.IntegerField(choices=gender_choices, default=1)
#
#
# class UserType(models.Model):
# 	name = models.CharField(max_length=32)
#
# 	def __str__(self):
# 		return self.name