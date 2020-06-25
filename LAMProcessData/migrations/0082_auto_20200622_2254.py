# Generated by Django 2.2 on 2020-06-22 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0081_lamprocess_dingdingrecord_acquisition_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='评论信息'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='事件描述'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='product',
            field=models.ManyToManyField(blank=True, null=True, to='LAMProcessData.LAMProduct', verbose_name='零件实例'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='product_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='零件编号'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='reporter',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='汇报人'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='work_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LAMProcessData.Worksection', verbose_name='成形工段实例'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='worksection_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='成形工段编号'),
        ),
        migrations.AlterField(
            model_name='lamprocess_dingdingrecord',
            name='writer',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='日志填报人'),
        ),
    ]
