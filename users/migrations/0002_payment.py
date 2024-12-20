# Generated by Django 5.1.2 on 2024-10-17 17:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0002_alter_lesson_course"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                    "payment_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата платежа"
                    ),
                ),
                (
                    "cost",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Стоимость покупки"
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("cash", "cash"), ("online", "online")],
                        default="cash",
                        verbose_name="Способ оплаты",
                    ),
                ),
                (
                    "payment_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.course",
                        verbose_name="Оплаченный курс",
                    ),
                ),
                (
                    "payment_lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lms.lesson",
                        verbose_name="Оплаченный урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="За кого произведена оплата",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оплата",
                "verbose_name_plural": "Оплаты",
            },
        ),
    ]
