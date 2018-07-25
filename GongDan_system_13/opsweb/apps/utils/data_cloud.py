# encoding: utf-8
from alisdk import ECSHandler
from tensdk import TenHandler
from cmdb.models import Host, Disk


def get_hosts_from_aliyun():
    """
    从阿里云获取ECS实例并入库
    :return:
    """
    ecs = ECSHandler('LTAIelGwFTF3eiVQ', 'VvEDjmx6GDWaxDtZlF9GVTyONsgyu7', 'cn-beijing')
    page = 1
    while True:
        instances, exception, next_page = ecs.get_instances(page)

        for instance in instances:
            disks = instance.pop('disks')
            instance['cloud_type'] = 'aliyun'
            try:
                host = Host.objects.create(**instance)
                for disk in disks:
                    instance = Disk()
                    instance.host = host
                    instance.disk_id = disk['disk_id']
                    instance.device = disk['device']
                    instance.size = disk['size']
                    instance.type = disk['type']
                    instance.creation_time = disk['creation_time']
                    instance.expired_time = disk['expired_time']
                    instance.save()
            except Exception as e:
                host = Host.objects.filter(instance_id=instance['instance_id']).update(**instance)
                for disk in disks:
                    instance = Disk.objects.filter(host=host).update(**disk)
        page += 1
        if not next_page:
            break
    return True


def get_hosts_from_qcloud():
    """
    从腾讯云获取ECS实例并入库
    :return:
    """
    ecs = TenHandler('', '', '', 'cvm')
    instances, is_success, next_page = ecs.get_instances(1)
    if is_success:
        page = 1
        while True:
            for instance in instances:
                disks = instance.pop('disks')
                instance['cloud_type'] = 'qcloud'
                try:
                    host = Host.objects.create(**instance)
                    for disk in disks:
                        instance = Disk()
                        instance.host = host
                        instance.disk_id = disk['disk_id']
                        instance.device = disk['device']
                        instance.size = disk['size']
                        instance.type = disk['type']
                        instance.creation_time = disk['creation_time']
                        instance.expired_time = disk['expired_time']
                        instance.save()
                except Exception as e:
                    host = Host.objects.filter(instance_id=instance['instance_id']).update(**instance)
                    for disk in disks:
                        instance = Disk.objects.filter(host=host).update(**disk)
            page += 1
            if not next_page:
                break
        return True


def get_hosts_from_cloud():
    """
    从阿里云和腾讯云上获取主机信息并入库
    :return:
    """
    aliyun_success = get_hosts_from_aliyun()
    qcloud_success = get_hosts_from_qcloud()
    if aliyun_success and qcloud_success:
        return True
    else:
        return False
