# Generated by Django 2.2 on 2020-03-12 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0044_auto_20200229_2358'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModulePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('SystemInformation', '基础信息'), ('Technique', '技术管理'), ('Quality', '质量管理'), ('Manufacture', '生产管理'), ('Operator.LAM', '激光成形操作者'), ('Operator.HT', '热处理操作者'), ('Operator.STOREROOM', '库房管理者'), ('Operator.INSP', '检验者')),
            },
        ),
        migrations.AlterField(
            model_name='process_cncdata_mission',
            name='accumulate_data_file',
            field=models.FileField(null=True, upload_to='./analyse/ACCUMULATEDATA/'),
        ),
    ]
