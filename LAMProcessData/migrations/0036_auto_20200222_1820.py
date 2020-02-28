# Generated by Django 2.2 on 2020-02-22 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0035_auto_20200222_1222'),
    ]

    operations = [
        migrations.CreateModel(
            name='LAMProcessParameterAccumulateCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('M1', models.FloatField(blank=True, null=True)),
                ('M2', models.FloatField(blank=True, null=True)),
                ('M3', models.FloatField(blank=True, null=True)),
                ('K', models.FloatField(blank=True, null=True)),
                ('alarm_value', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='lamprocessparameters',
            name='accumulate_cell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LAMProcessData.LAMProcessParameterAccumulateCell'),
        ),
    ]