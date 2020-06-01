from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from utils.encrypt import uid
from utils.tencent.cos import upload_file
from web.forms.wiki import WikiModelForm
from web.models import Wiki


def wiki(request, project_id):
    """ wiki的首页 """
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')
    wiki_object = Wiki.objects.filter(id=wiki_id, project_id=project_id).first()

    return render(request, 'wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'wiki_form.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        # 判断用户是否已经选择父文章
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.tracer.project
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'wiki_form.html', {'form': form})


def wiki_catalog(request, project_id):
    if request.is_ajax():
        data = Wiki.objects.filter(project=request.tracer.project).values("id", 'title', 'parent_id').order_by(
            'depth', 'id')
        return JsonResponse({'status': True, 'data': list(data)})

    return JsonResponse({'status': False, 'data': '非法请求'})


def wiki_delete(request, project_id, wiki_id):
    """ 删除文章 """

    Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()

    url = reverse('wiki', kwargs={'project_id': project_id})
    return redirect(url)


def wiki_edit(request, project_id, wiki_id):
    """ 编辑文章 """
    wiki_object = Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_object:
        url = reverse('wiki', kwargs={'project_id': project_id})
        return redirect(url)
    if request.method == "GET":
        form = WikiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_form.html', {'form': form})

    form = WikiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.save()
        url = reverse('wiki', kwargs={'project_id': project_id})
        preview_url = "{0}?wiki_id={1}".format(url, wiki_id)
        return redirect(preview_url)

    return render(request, 'wiki_form.html', {'form': form})


@csrf_exempt
def upload(request, project_id):
    result = {
        'success': 0,
        'message': None,
        'url': None
    }
    img_obj = request.FILES.get('editormd-image-file')
    if not img_obj:
        result['message'] = '文件不存在'
        return JsonResponse(result)
    # 文件的对象上传到桶
    bucket = request.tracer.project.bucket

    body = img_obj
    ext = img_obj.name.rsplit('.')[-1]
    filename = '%s.%s' % (uid(request.tracer.user.mobile_phone), ext)

    url = upload_file(bucket, body, filename)
    result['success'] = 1
    result['url'] = url

    return JsonResponse(result)
