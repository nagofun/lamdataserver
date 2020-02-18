# Generated by Django 2.2 on 2020-02-12 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0021_auto_20200210_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process_Realtime_FineData_By_WorkSectionID_6',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquisition_timestamp', models.PositiveIntegerField(null=True)),
                ('oxygen_value', models.IntegerField(null=True)),
                ('laser_power', models.IntegerField(null=True)),
                ('X_value', models.FloatField(null=True)),
                ('Y_value', models.FloatField(null=True)),
                ('Z_value', models.FloatField(null=True)),
                ('ScanningRate_value', models.FloatField(null=True)),
                ('FeedRate_value', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
