# Generated by Django 4.2.16 on 2024-10-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rating_comment_alter_rating_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pickup',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
