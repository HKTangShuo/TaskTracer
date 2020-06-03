from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from utils.tencent.cos import create_bucket, create_bucket_name
from web import models
from web.forms.project import ProjectModelForm


def project_list(request):
    """ 项目列表 """
    if request.method == "GET":
        project_dict = {'star': [], 'my': [], 'join': []}

        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({"value": row, 'type': 'my'})
            else:
                project_dict['my'].append(row)

        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append(item.project)
            else:
                project_dict['join'].append(item.project)
        form = ProjectModelForm(request)

        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 为项目创建桶,名字不能重复
        # 手机号+时间戳+后缀名

        buckname = create_bucket_name(request, form.instance.name, settings.BUCKET_REGION)

        create_bucket(buckname)
        form.cleaned_data['name'] = buckname
        form.instance.region = settings.BUCKET_REGION

        form.instance.bucket = buckname

        # 验证通过：项目名、颜色、描述 + creator谁创建的项目？
        form.instance.creator = request.tracer.user
        # 创建项目

        form.save()

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_id, project_type):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """ 取消星标 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')

    return HttpResponse('请求错误')
