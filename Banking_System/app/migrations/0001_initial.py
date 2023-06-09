# Generated by Django 4.1.2 on 2023-03-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FullName', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254)),
                ('Mobile', models.PositiveIntegerField()),
                ('AdharNo', models.PositiveIntegerField()),
                ('Address', models.TextField()),
                ('DOB', models.DateField()),
                ('Age', models.IntegerField()),
                ('Gender', models.CharField(max_length=10)),
                ('Image', models.FileField(max_length=250, upload_to='RegisterImg/')),
                ('UserName', models.CharField(max_length=25)),
                ('Password', models.CharField(max_length=25)),
            ],
        ),
    ]
