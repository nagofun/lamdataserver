# Generated by Django 2.2 on 2020-03-14 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0048_auto_20200314_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_HeatTreatment',
        ),
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_LAM',
        ),
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_PhyChemTest',
        ),
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_RawStockSendRetrieve',
        ),
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_Scheduling',
        ),
        migrations.RemoveField(
            model_name='lamproductionworktype',
            name='selectable_Weighing',
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_HeatTreatment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_LAM',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_PhyChemTest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_RawStockSendRetrieve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_Scheduling',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lam_techinst_serial',
            name='selectable_Weighing',
            field=models.BooleanField(default=False),
        ),
    ]
