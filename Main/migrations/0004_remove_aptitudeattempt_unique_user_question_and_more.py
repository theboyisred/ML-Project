# Generated by Django 5.0 on 2024-02-26 17:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_personalityquestion_tag_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='aptitudeattempt',
            name='unique_user_question',
        ),
        migrations.AddField(
            model_name='aptitudeattempt',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Main.job'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalityattempt',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Main.job'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='aptitudeattempt',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='unique_user_aptitude_question'),
        ),
        migrations.AddConstraint(
            model_name='personalityattempt',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='unique_user_personality_question'),
        ),
    ]