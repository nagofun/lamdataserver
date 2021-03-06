# Generated by Django 2.2 on 2020-04-17 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0064_auto_20200417_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawstocksendretrieve',
            name='raw_stock_primaryretrieve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RawStock_RetrieveAsPrimaryFrom', to='LAMProcessData.RawStock'),
        ),
        migrations.AlterField(
            model_name='rawstocksendretrieve',
            name='raw_stock_secondaryretrieve',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='RawStock_RetrieveAssecondaryFrom', to='LAMProcessData.RawStock'),
        ),
    ]
