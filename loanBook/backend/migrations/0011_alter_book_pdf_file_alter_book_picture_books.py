# Generated by Django 5.0.4 on 2024-05-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_alter_book_year_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='images/pdf_books/'),
        ),
        migrations.AlterField(
            model_name='book',
            name='picture_books',
            field=models.FileField(default='default_image.jpg', upload_to='images/picture_books/'),
        ),
    ]
