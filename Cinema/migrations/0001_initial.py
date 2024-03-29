# Generated by Django 3.1.3 on 2020-12-02 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('rating', models.FloatField()),
                ('duration', models.TimeField()),
                ('date', models.DateTimeField()),
                ('image', models.FileField(default='default.png', upload_to='movie')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Cinema.genre')),
            ],
        ),
    ]
