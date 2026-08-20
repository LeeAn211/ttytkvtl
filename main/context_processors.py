from .models import MenuItem, SideBar, Banner, PageView, CarouselImage, ScheduleCategory,ScheduleItem
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render
from django.db.models import Prefetch
from collections import defaultdict



def menu_items(request):
    menu = MenuItem.objects.filter(parent__isnull=True)
    return {'menu_items': menu}

def sidebars(request):
    return {
        'left_sidebars': SideBar.objects.filter(position='left'),
        'right_sidebars': SideBar.objects.filter(position='right'),
    }

def common_data(request):
    return {
        'now': timezone.localtime(timezone.now()),
    }

def global_context(request):
    """Tự động truyền menu, sidebar, banners và thời gian hiện tại đến mọi template"""
    return {
        # Menu chính
        'menu_items': MenuItem.objects.filter(parent__isnull=True),

        # Sidebars
        'sidebar_left': SideBar.objects.filter(position='left').order_by('order'),
        'sidebar_right': SideBar.objects.filter(position='right').order_by('order'),
        


        # Banner
        'banners': Banner.objects.filter(is_active=True).order_by('order'),

       
        # Thời gian hiện tại
        'now': datetime.now()
    }


def pageview_stats(request):
    today = timezone.now().date()
    return {
        'total_views': PageView.objects.count(),
        'today_views': PageView.objects.filter(created_at__date=today).count()
    }



def schedule_context(request):
    cats = (
        ScheduleCategory.objects
        .prefetch_related(
            Prefetch('items',
                     queryset=ScheduleItem.objects.order_by('order'))
        )
        .order_by('main_title', 'order')   # ✅ sắp xếp ngay tại query
    )

    groups = defaultdict(list)
    for c in cats:
        groups[c.main_title].append(c)

    # ⚠️ CHỐT: chuyển về list đã sắp xếp theo main_title để đảm bảo
    sorted_groups = {
        k: sorted(v, key=lambda x: x.order)
        for k, v in sorted(groups.items(), key=lambda kv: kv[0])
    }

    return {'schedule_groups': sorted_groups}

def sidebars_context(request):
    """
    Trả về toàn bộ dữ liệu Sidebar kèm item và post
    để dùng ở mọi template (ví dụ sidebar-left, sidebar-right, breadcrumb…)
    """
    left_sidebars = SideBar.objects.filter(position='left').prefetch_related(
        'items__posts'
    )
    right_sidebars = SideBar.objects.filter(position='right').prefetch_related(
        'items__posts'
    )
    return {
        'left_sidebars': left_sidebars,
        'right_sidebars': right_sidebars,
    }