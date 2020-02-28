# Generated by Django 2.2 on 2020-02-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0034_auto_20200219_2241'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_1',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_1',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_2',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_2',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_3',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_3',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_4',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_4',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_5',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_5',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_6',
        #     name='if_exec_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        # migrations.AddField(
        #     model_name='process_realtime_finedata_by_worksectionid_6',
        #     name='if_interrupt_intr',
        #     field=models.BooleanField(blank=True, null=True),
        # ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_1',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_1',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_1',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_1',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_2',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_2',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_2',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_2',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_3',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_3',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_3',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_3',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_4',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_4',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_4',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_4',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_5',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_5',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_5',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_5',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_6',
            name='FeedRate_value',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_6',
            name='ScanningRate_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_6',
            name='laser_power',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='process_realtime_finedata_by_worksectionid_6',
            name='oxygen_value',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_1',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_2',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_3',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_4',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_5',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_6',
            index_together={('process_mission', 'acquisition_timestamp', 'Z_value', 'laser_power', 'ScanningRate_value')},
        ),
    ]