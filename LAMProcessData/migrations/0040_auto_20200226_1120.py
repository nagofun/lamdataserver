# Generated by Django 2.2 on 2020-02-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0039_auto_20200223_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process_accumulatedata_date_mission',
            name='K',
        ),
        migrations.RemoveField(
            model_name='process_accumulatedata_date_mission',
            name='P',
        ),
        migrations.RemoveField(
            model_name='process_accumulatedata_date_mission',
            name='index_date',
        ),
        migrations.RemoveField(
            model_name='process_accumulatedata_date_mission',
            name='index_date_int',
        ),
        migrations.RemoveField(
            model_name='process_accumulatedata_date_mission',
            name='minute_index',
        ),
        migrations.RemoveField(
            model_name='process_cncdata_date_mission',
            name='Z_value',
        ),
        migrations.RemoveField(
            model_name='process_cncdata_date_mission',
            name='index_date',
        ),
        migrations.RemoveField(
            model_name='process_cncdata_date_mission',
            name='index_date_int',
        ),
        migrations.RemoveField(
            model_name='process_cncdata_date_mission',
            name='layer_thickness',
        ),
        migrations.RemoveField(
            model_name='process_cncdata_date_mission',
            name='minute_index',
        ),
        migrations.AddField(
            model_name='process_accumulatedata_date_mission',
            name='M1',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process_accumulatedata_date_mission',
            name='M2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process_accumulatedata_date_mission',
            name='data_file',
            field=models.FileField(default=None, upload_to='./media/analyse/CNCData/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='process_accumulatedata_date_mission',
            name='l',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process_accumulatedata_date_mission',
            name='tm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process_cncdata_date_mission',
            name='data_file',
            field=models.FileField(default=1, upload_to='./media/analyse/CNCData/'),
            preserve_default=False,
        ),
    ]