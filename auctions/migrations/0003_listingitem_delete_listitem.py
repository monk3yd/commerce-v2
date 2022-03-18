# Generated by Django 4.0.3 on 2022-03-18 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('starting_bid', models.FloatField()),
                ('img_url', models.URLField()),
                ('category', models.CharField(choices=[('default', '...'), ('electronics', 'Electronics'), ('home', 'Home'), ('toys', 'Toys'), ('fashion', 'Fashion')], max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='ListItem',
        ),
    ]