# Generated by Django 5.0.4 on 2024-05-14 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_borrow_delete_emprunt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='picture_books',
            field=models.FileField(blank=True, default='default_image.jpg', null=True, upload_to='images/picture_books/'),
        ),
    ]
