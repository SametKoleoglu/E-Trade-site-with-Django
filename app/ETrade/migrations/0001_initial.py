# Generated by Django 5.0.4 on 2024-04-04 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100)),
                ('iamge', models.ImageField(blank=True, null=True, upload_to='brand_images')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DiskQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disk_quantity', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processor_model', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RamSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ram_size', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images')),
                ('price', models.FloatField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.brand')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.color')),
                ('disk_quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.diskquantity')),
                ('processor_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.processormodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ram_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.ramsize')),
                ('use_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ETrade.usetype')),
            ],
        ),
    ]
