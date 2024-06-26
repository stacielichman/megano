# Generated by Django 5.0.3 on 2024-05-18 09:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0031_alter_profile_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phone",
            field=models.CharField(
                blank=True,
                default=1,
                max_length=17,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+?1?\\d{9,15}$",
                    )
                ],
            ),
            preserve_default=False,
        ),
    ]
