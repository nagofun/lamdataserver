# Generated by Django 2.2 on 2020-02-23 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0037_auto_20200223_0020'),
    ]

    operations = [
        migrations.AddField(
            model_name='lamprocessparameteraccumulatecell',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lamprocessparameters',
            name='accumulate_cell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AccuCell_Parameter', to='LAMProcessData.LAMProcessParameterAccumulateCell'),
        ),
    ]