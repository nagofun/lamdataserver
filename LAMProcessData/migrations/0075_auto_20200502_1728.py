# Generated by Django 2.2 on 2020-05-02 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0074_auto_20200502_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nondestructivetest_mission',
            name='quality_reviewsheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LAMProcessData.QualityReviewSheet', verbose_name='不合格品审理单'),
        ),
    ]
