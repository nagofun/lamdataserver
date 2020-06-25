# Generated by Django 2.2 on 2020-06-23 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0082_auto_20200622_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='product_code',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='零件编号'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='reporter',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='汇报人'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='worksection_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='成形工段编号'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='writer',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='日志填报人'),
        ),
    ]
