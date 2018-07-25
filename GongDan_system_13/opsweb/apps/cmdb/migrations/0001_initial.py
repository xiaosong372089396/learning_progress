# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-15 08:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disk_id', models.CharField(blank=True, max_length=22, null=True, verbose_name='\u78c1\u76d8ID')),
                ('device', models.CharField(blank=True, max_length=15, null=True, verbose_name='\u6240\u5c5eInstance\u7684Device\u4fe1\u606f')),
                ('size', models.IntegerField(verbose_name='\u78c1\u76d8\u5927\u5c0f\uff0c\u5355\u4f4dGB')),
                ('type', models.CharField(choices=[('system', '\u7cfb\u7edf\u76d8'), ('data', '\u6570\u636e\u76d8')], default='data', max_length=6, verbose_name='\u78c1\u76d8\u7c7b\u578b')),
                ('creation_time', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('expired_time', models.DateTimeField(verbose_name='\u8fc7\u671f\u65f6\u95f4')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u5165\u5e93\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u78c1\u76d8',
                'verbose_name_plural': '\u78c1\u76d8',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloud_type', models.CharField(choices=[('aliyun', '\u963f\u91cc\u4e91'), ('qcloud', '\u817e\u8baf\u4e91')], default='aliyun', max_length=20, verbose_name='\u4e91\u4e3b\u673a\u7c7b\u578b')),
                ('instance_id', models.CharField(max_length=22, unique=True, verbose_name='\u5b9e\u4f8bID')),
                ('instance_name', models.CharField(max_length=22, verbose_name='\u5b9e\u4f8b\u7684\u663e\u793a\u540d\u79f0')),
                ('description', models.CharField(blank=True, max_length=128, null=True, verbose_name='\u5b9e\u4f8b\u7684\u63cf\u8ff0')),
                ('image_id', models.CharField(max_length=50, verbose_name='\u955c\u50cfID')),
                ('region_id', models.CharField(max_length=30, verbose_name='\u5b9e\u4f8b\u6240\u5c5e\u5730\u57dfID')),
                ('zone_id', models.CharField(max_length=30, verbose_name='\u5b9e\u4f8b\u6240\u5c5e\u53ef\u7528\u533a')),
                ('cpu', models.IntegerField(verbose_name='CPU\u6838\u6570')),
                ('memory', models.IntegerField(verbose_name='\u5185\u5b58\u5927\u5c0f\uff0c\u5355\u4f4d: GB')),
                ('instance_type', models.CharField(max_length=30, verbose_name='\u5b9e\u4f8b\u8d44\u6e90\u89c4\u683c')),
                ('status', models.CharField(choices=[('Running', '\u8fd0\u884c\u4e2d'), ('Starting', '\u542f\u52a8\u4e2d'), ('Stopping', '\u505c\u6b62\u4e2d'), ('Stopped', '\u5df2\u505c\u6b62')], default='Running', max_length=8, verbose_name='\u5b9e\u4f8b\u72b6\u6001')),
                ('hostname', models.CharField(blank=True, max_length=23, null=True, verbose_name='\u5b9e\u4f8b\u673a\u5668\u540d\u79f0')),
                ('public_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u516c\u7f51IP')),
                ('private_ip', models.GenericIPAddressField(verbose_name='\u79c1\u7f51IP')),
                ('os_type', models.CharField(default='linux', max_length=10, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b')),
                ('os_name', models.CharField(default='', max_length=20, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u540d\u79f0')),
                ('instance_charge_type', models.CharField(choices=[('PrePaid', '\u9884\u4ed8\u8d39'), ('PostPaid', '\u540e\u4ed8\u8d39')], default='PrePaid', max_length=8, verbose_name='\u5b9e\u4f8b\u7684\u4ed8\u8d39\u65b9\u5f0f')),
                ('creation_time', models.DateTimeField(verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('expired_time', models.DateTimeField(verbose_name='\u8fc7\u671f\u65f6\u95f4')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u5165\u5e93\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u4e3b\u673a',
                'verbose_name_plural': '\u4e3b\u673a',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u4e1a\u52a1\u7ebf\u540d\u79f0')),
                ('module_letter', models.CharField(max_length=32, verbose_name='\u5b57\u6bcd\u7b80\u79f0')),
                ('dev_interface', models.ManyToManyField(related_name='dev', to=settings.AUTH_USER_MODEL, verbose_name='\u4e1a\u52a1\u8d1f\u8d23\u4eba')),
                ('op_interface', models.ManyToManyField(related_name='op', to=settings.AUTH_USER_MODEL, verbose_name='\u8fd0\u7ef4\u8d1f\u8d23\u4eba')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Product', verbose_name='\u4e0a\u7ea7\u4e1a\u52a1\u7ebf')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='business_line',
            field=models.ManyToManyField(blank=True, to='cmdb.Product', verbose_name='\u4e1a\u52a1\u7ebf'),
        ),
        migrations.AddField(
            model_name='disk',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Host', verbose_name='\u4e3b\u673a'),
        ),
    ]