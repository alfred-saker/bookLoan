# Generated by Django 5.0.4 on 2024-05-11 00:02

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_emprunt_borrow_date_emprunt_return_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('borrow_date', models.DateField(default=django.utils.timezone.now)),
                ('return_date', models.DateField(default=django.utils.timezone.now)),
                ('books', models.ForeignKey(default='9dfdd4c2-0247-48b0-8450-fb6d726ed545', on_delete=django.db.models.deletion.CASCADE, to='backend.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Emprunt',
        ),
    ]