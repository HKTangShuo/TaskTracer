from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from utils.tencent.cos import delete_file, delete_file_list, credential
from web import models
from web.forms.file import FolderModelForm
from web.models import Project


def file(request, project_id):
    """ 文件列表 & 添加文件夹 """

    parent_object = None
    folder_id = request.GET.get('folder', "")
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(id=int(folder_id), file_type=2,
                                                             project=request.tracer.project).first()

    # GET 查看页面
    if request.method == "GET":

        breadcrumb_list = []
        parent = parent_object
        while parent:
            # breadcrumb_list.insert(0, {'id': parent.id, 'name': parent.name})
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
            parent = parent.parent

        # 当前目录下所有的文件 & 文件夹获取到即可
        queryset = models.FileRepository.objects.filter(project=request.tracer.project)
        if parent_object:
            # 进入了某目录
            file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')
        else:
            # 根目录
            file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')
        form = FolderModelForm(request, parent_object)

        context = {
            'form': form,
            "file_object_list": file_object_list,
            "breadcrumb_list": breadcrumb_list,
            'folder_object': parent_object
        }
        return render(request, 'file.html', context)


def file_delete(request, project_id):
    """ 删除文件 """
    fid = request.GET.get('fid')

    # 删除数据库中的 文件 & 文件夹 （级联删除）
    delete_object = models.FileRepository.objects.filter(id=fid, project=request.tracer.project).first()
    if delete_object.file_type == 1:
        # 删除文件（数据库文件删除、cos文件删除、项目已使用空间容量还回去）
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()
        request.tracer.project.use_space -= delete_object.file_size
        request.tracer.project.save()

        # cos中删除文件
        delete_file(request.tracer.project.bucket, settings.BUCKET_REGION, delete_object.key)

        # 在数据库中删除当前文件
        delete_object.delete()

        return JsonResponse({'status': True})
    # 删除文件夹（找到文件夹下所有的文件->数据库文件删除、cos文件删除、项目已使用空间容量还回去）
    # delete_object
    # 找他下面的 文件和文件夹
    # models.FileRepository.objects.filter(parent=delete_object) # 文件 删除；文件夹 继续向里查

    total_size = 0
    key_list = []

    folder_list = [delete_object, ]
    for folder in folder_list:
        child_list = models.FileRepository.objects.filter(project=request.tracer.project, parent=folder).order_by(
            '-file_type')
        for child in child_list:
            if child.file_type == 2:
                folder_list.append(child)
            else:
                # 文件大小汇总
                total_size += child.file_size

                # 删除文件
                key_list.append({"Key": child.key})

    # cos 批量删除文件
    if key_list:
        delete_file_list(request.tracer.project.bucket, request.tracer.project.region, key_list)

    # 归还容量
    if total_size:
        request.tracer.project.use_space -= total_size
        request.tracer.project.save()

    # 删除数据库中的文件
    delete_object.delete()
    return JsonResponse({'status': True})


def cos_credential(request, project_id):


    # 容量限制 单文件 总容量
    data = credential(request.tracer.project.bucket, settings.BUCKET_REGION)
    return JsonResponse(data)


def file_post(request):
    return None


def file_download(request):
    return None
