# Generated by Django 2.2 on 2020-04-04 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0061_auto_20200404_0824'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lamtechniqueinstruction',
            unique_together={('instruction_code', 'version_code', 'version_number')},
        ),
    ]