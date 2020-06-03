from django.shortcuts import render


def dashboard(request, project_id):
    return render(request, 'dashboard.html')


def issues(request, project_id):
    return render(request, 'issues.html')


def statistics(request, project_id):
    return render(request, 'statistics.html')


def setting(request, project_id):
    return render(request, 'setting.html')
