# Generated by Django 5.0.4 on 2024-05-15 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_alter_book_picture_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdf_books/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='picture_books',
            field=models.FileField(upload_to='picture_books/'),
        ),
    ]