from django.http import JsonResponse
from django.shortcuts import render

from web import models
from web.forms.project import ProjectModelForm


def project_list(request):
    """ 项目列表 """
    if request.method == "GET":
        project_dict = {'star': [], 'my': [], 'join': []}

        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append(row)
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
        # 验证通过：项目名、颜色、描述 + creator谁创建的项目？
        form.instance.creator = request.tracer.user
        # 创建项目
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})
