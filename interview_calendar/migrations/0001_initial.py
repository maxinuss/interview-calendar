""" Migrations """

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """ Initial migrations"""
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('candidate', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='interview_calendar.Candidate'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterviewInterviewer',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('interview', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='interview_calendar.Interview'
                )),
                ('interviewer', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='interview_calendar.Interviewer'
                )),
            ],
        ),
        migrations.CreateModel(
            name='InterviewerSlot',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('interviewer', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='interview_calendar.Interviewer'
                )),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateSlot',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('candidate', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='interview_calendar.Candidate'
                )),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
