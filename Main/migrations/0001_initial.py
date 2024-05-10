# Generated by Django 5.0 on 2024-02-26 12:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AptitudeQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1024)),
                ('option_a', models.CharField(max_length=1024)),
                ('option_b', models.CharField(max_length=1024)),
                ('option_c', models.CharField(max_length=1024)),
                ('option_d', models.CharField(max_length=1024)),
                ('correct_option', models.IntegerField(choices=[(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D')])),
            ],
            options={
                'verbose_name': 'Aptitude Test Question',
                'verbose_name_plural': 'Aptitude Test Questions',
            },
        ),
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('email', models.EmailField(max_length=254)),
                ('date_of_birth', models.DateField()),
                ('previous_jobs', models.CharField(max_length=1024)),
                ('qualification', models.CharField(choices=[('SSCE', 'Senior Secondary Certificate'), ('DEG', 'University Degree'), ('MAS', 'Masters Degree'), ('PHD', 'Doctorate of Philosophy (PhD.)')], max_length=1024)),
                ('hobbies', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('description', models.TextField()),
                ('wages', models.DecimalField(decimal_places=2, max_digits=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='PersonalityQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name': 'Personality Test Question',
                'verbose_name_plural': 'Personality Test Questions',
            },
        ),
        migrations.CreateModel(
            name='AptitudeAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField()),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aq_attempts', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aq_attempts', to='Main.aptitudequestion')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(choices=[(0, 'Very Bad'), (1, 'Bad'), (2, 'Neutral'), (3, 'Good'), (4, 'Very Good')])),
                ('completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pq_attempts', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pq_attempts', to='Main.personalityquestion')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.PositiveSmallIntegerField()),
                ('aptitude_test_result', models.PositiveSmallIntegerField()),
                ('personality_type', models.ImageField(upload_to='')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.job', verbose_name='Role Applied')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Candidate Name')),
            ],
        ),
        migrations.AddConstraint(
            model_name='aptitudeattempt',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='unique_user_question'),
        ),
    ]
