# Generated by Django 2.1 on 2018-08-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_telephonebill'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.IntegerField(null=True)),
                ('destination', models.IntegerField(null=True)),
            ],
        ),
    ]
