# Generated by Django 5.1.2 on 2024-10-16 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Course Title",
                        max_length=255,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Course Description", verbose_name="Описание курса"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Course Preview",
                        null=True,
                        upload_to="lms/courses",
                        verbose_name="Превью курса",
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Lesson Title",
                        max_length=255,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="Lesson Description", verbose_name="Описание урока"
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Lessons Preview",
                        null=True,
                        upload_to="lms/lessons",
                        verbose_name="Превью урока",
                    ),
                ),
                (
                    "video_url",
                    models.URLField(
                        blank=True,
                        help_text="Video URL",
                        null=True,
                        verbose_name="Ссылка на урок",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
                "ordering": ["course", "title"],
            },
        ),
    ]
