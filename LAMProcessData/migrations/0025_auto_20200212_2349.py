# Generated by Django 2.2 on 2020-02-12 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0024_auto_20200212_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryparameter_id',
            name='note',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_1',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_2',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_3',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_4',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_5',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
        migrations.AlterIndexTogether(
            name='process_realtime_finedata_by_worksectionid_6',
            index_together={('process_mission', 'acquisition_timestamp')},
        ),
    ]