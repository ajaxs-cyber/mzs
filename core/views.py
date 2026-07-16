from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Case, Message, SurveyResponse, PageVisit, ExperimentMetric
from .forms import RegisterForm, ProfileForm


def index(request):
    """首页"""
    cases = Case.objects.all()
    return render(request, 'index.html', {'cases': cases})


def stats_page(request):
    """统计看板"""
    return render(request, 'stats.html')


# ===== 留言板 API =====

def get_messages(request):
    messages = Message.objects.filter(is_approved=True)[:50]
    data = [{
        'id': m.id,
        'username': m.username,
        'content': m.content,
        'created_at': timezone.localtime(m.created_at).strftime('%m-%d %H:%M'),
    } for m in messages]
    return JsonResponse({'messages': data})


@csrf_exempt
def create_message(request):
    if request.method == 'POST':
        username = request.POST.get('username', '匿名').strip() or '匿名'
        content = request.POST.get('content', '').strip()
        if not content or len(content) > 500:
            return JsonResponse({'ok': False, 'error': '内容为空或超过500字'}, status=400)
        msg = Message.objects.create(username=username, content=content)
        return JsonResponse({'ok': True, 'id': msg.id})
    return JsonResponse({'ok': False, 'error': '仅支持POST'}, status=405)


# ===== 救助病例 API =====

def get_cases(request):
    cases = Case.objects.all()
    data = [{
        'id': c.id,
        'title': c.title,
        'name': c.name,
        'disease': c.disease,
        'story': c.story,
        'result': c.result,
        'image_url': c.image.url if c.image else '',
    } for c in cases]
    return JsonResponse({'cases': data})


# ===== 问卷 API =====

@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        try:
            sr = SurveyResponse.objects.create(
                q1=int(request.POST.get('q1', 0)),
                q2=int(request.POST.get('q2', 0)),
                q3=int(request.POST.get('q3', 0)),
                q4=int(request.POST.get('q4', 0)),
                q5=request.POST.get('q5', '').strip(),
            )
            return JsonResponse({'ok': True, 'id': sr.id})
        except (ValueError, TypeError):
            return JsonResponse({'ok': False, 'error': '评分无效'}, status=400)
    return JsonResponse({'ok': False, 'error': '仅支持POST'}, status=405)


# ===== 访问追踪 API =====

@csrf_exempt
def track_visit(request):
    """记录 PV/UV -- 每次页面加载调用"""
    if request.method == 'POST':
        session_id = request.POST.get('session_id', '')
        page = request.POST.get('page', 'index')
        if session_id:
            PageVisit.objects.create(session_id=session_id, page=page)
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


@csrf_exempt
def track_scroll(request):
    """更新滚动完成率"""
    if request.method == 'POST':
        session_id = request.POST.get('session_id', '')
        pct = int(request.POST.get('scroll_percentage', 0))
        if session_id:
            visit = PageVisit.objects.filter(session_id=session_id).last()
            if visit and pct > visit.scroll_percentage:
                visit.scroll_percentage = pct
                visit.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


@csrf_exempt
def track_duration(request):
    """更新停留时长"""
    if request.method == 'POST':
        session_id = request.POST.get('session_id', '')
        seconds = int(request.POST.get('duration_seconds', 0))
        if session_id:
            visit = PageVisit.objects.filter(session_id=session_id).last()
            if visit:
                visit.duration_seconds = seconds
                visit.save()
        return JsonResponse({'ok': True})
    return JsonResponse({'ok': False}, status=405)


# ===== 统计 API =====

def get_stats(request):
    """返回六大指标"""
    visits = PageVisit.objects.all()
    uv = visits.values('session_id').distinct().count()
    pv = visits.count()
    avg_duration = visits.aggregate(avg=Avg('duration_seconds'))['avg'] or 0
    avg_scroll = visits.aggregate(avg=Avg('scroll_percentage'))['avg'] or 0
    message_count = Message.objects.filter(is_approved=True).count()
    survey_count = SurveyResponse.objects.count()

    return JsonResponse({
        'uv': uv,
        'pv': pv,
        'avg_duration_seconds': round(avg_duration, 1),
        'avg_scroll_percentage': round(avg_scroll, 1),
        'message_count': message_count,
        'survey_count': survey_count,
    })


# ===== AB对照实验 =====

def experiment_page(request):
    """AB对照实验看板"""
    return render(request, 'experiment.html')


def get_experiment_data(request):
    """返回AB对照实验指标"""
    metrics = ExperimentMetric.objects.all()
    data = [{
        'metric_name': m.metric_name,
        'value_a': m.value_a,
        'value_b': m.value_b,
    } for m in metrics]
    return JsonResponse({'metrics': data})


# ===== 用户认证 =====

def register_view(request):
    """用户注册"""
    if request.user.is_authenticated:
        return redirect('profile')
    errors = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('profile')
        errors = {k: v[0] for k, v in form.errors.items()}
    return render(request, 'register.html', {'errors': errors})


def login_view(request):
    """用户登录"""
    if request.user.is_authenticated:
        return redirect('profile')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'profile')
            return redirect(next_url)
        error = '用户名或密码不正确'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """退出登录"""
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def profile_view(request):
    """个人中心"""
    success = ''
    error = ''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            profile.bio = form.cleaned_data['bio']
            profile.phone = form.cleaned_data['phone']
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
            success = '资料已更新'
        else:
            error = '请检查输入内容'
    return render(request, 'profile.html', {
        'profile': request.user.profile,
        'user': request.user,
        'success': success,
        'error': error,
    })
