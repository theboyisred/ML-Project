# Generated by Django 5.0.2 on 2024-03-12 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_alter_result_experience'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('rank_score',)},
        ),
        migrations.AddField(
            model_name='result',
            name='rank_score',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=16),
            preserve_default=False,
        ),
    ]