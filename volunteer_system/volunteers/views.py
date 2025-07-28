from django.shortcuts import render, get_object_or_404
from .models import Activity, Volunteer
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  
import json

def activity_list(request):
    return render(request, 'volunteers/index.html')

def activity_list_api(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    
    activities = Activity.objects.filter(is_active=True)
    
    if search:
        activities = activities.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    if category:
        activities = activities.filter(category=category)
        
    activities_data = list(activities.values('id', 'title', 'description', 'date', 'location', 'slots', 'category'))
    
    for activity in activities_data:
        activity['get_category_display'] = Activity.objects.get(id=activity['id']).get_category_display()

    categories_data = dict(Activity.CATEGORY_CHOICES)
    
    data = {
        'activities': activities_data,
        'categories': categories_data
    }
    return JsonResponse(data)

def activity_detail_api(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, is_active=True)
    return JsonResponse({
        'id': activity.id,
        'title': activity.title,
        'description': activity.description,
        'date': activity.date,
        'location': activity.location,
        'slots': activity.slots,
        'category': activity.category,
        'get_category_display': activity.get_category_display()
    })

@csrf_exempt  
def volunteer_signup(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, is_active=True)

    # 活动人数是否已满
    if activity.volunteer_set.count() >= activity.slots:
        return JsonResponse({'success': False, 'message': '抱歉，该活动报名人数已满。'}, status=400)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')

            if not name or not phone:
                return JsonResponse({'success': False, 'message': '请填写完整信息'}, status=400)

            Volunteer.objects.create(
                activity=activity,
                name=name,
                phone=phone
            )

            return JsonResponse({'success': True, 'message': '报名成功！'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求数据'}, status=400)

    return JsonResponse({'success': False, 'message': '只接受POST请求'}, status=405)