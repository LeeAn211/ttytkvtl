from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, SideBarPost, MenuItem, SideBar, Banner, Category, SideBarItem, ContactInfo
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Service
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import Service


# =========================
# TRANG CHỦ
# =========================
from django.shortcuts import render
from .models import Article, Category, MenuItem, SideBar, Banner, PageView, RunningText, CarouselImage, ScheduleCategory
from django.utils import timezone

def home(request):
    """
    Trang chủ hiển thị:
    - Banner
    - Menu chính
    - Tin nổi bật
    - Chủ đề riêng
    - Bài viết mới nhất
    - Sidebar trái/phải
    """
    # Menu chính (chỉ lấy menu cha)
    menu_items = MenuItem.objects.filter(
        parent__isnull=True,
        is_visible=True
    ).prefetch_related('children', 'articles')

    # Tin nổi bật: lấy 5 bài mới nhất
    top_articles = Article.objects.filter(
        published=True
    ).order_by('-created_at')[:5]

    # Chủ đề riêng
    categories = Category.objects.filter(is_visible=True).prefetch_related('articles')

    services = Service.objects.all()
   
    # chữ chạy
    running_texts = RunningText.objects.filter(active=True)

    carousel_images = CarouselImage.objects.filter(active=True).order_by('order')

    # Bài viết mới nhất (không giới hạn category)
    latest_articles = Article.objects.filter(
        published=True
    ).order_by('-created_at')[:5]

    
    # Banner
    banners = Banner.objects.filter(is_active=True).order_by('order')
     # Bài viết mới nhất (toàn bộ)
    all_articles = Article.objects.filter(published=True).order_by('-created_at')

      # ✅ Thêm phân trang, ví dụ 10 bài/trang
    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

  

    context = {
        'menu_items': menu_items,
        'top_articles': top_articles,          # Thêm dữ liệu tin nổi bật
        'categories': categories,
        'latest_articles': latest_articles,
        'banners': banners,
        'page_obj': page_obj,  
        "paginator": paginator,
        'running_texts': running_texts,
        'services': services,
        'carousel_images': carousel_images,
        
       
          
    }
    return render(request, 'main/home.html', context)



# =========================
# CHI TIẾT BÀI VIẾT
# =========================
def article_detail(request, slug):
    """
    Hiển thị chi tiết bài viết
    """
    article = get_object_or_404(Article, slug=slug, published=True)
    return render(request, 'main/article_detail.html', {
        'article': article
    })


# =========================
# CHI TIẾT BÀI VIẾT SIDEBAR
# =========================
def sidebar_post_detail(request, slug):
    """
    Hiển thị chi tiết bài viết trong sidebar
    """
    post = get_object_or_404(SideBarPost, slug=slug)
    sidebar_items = SideBarItem.objects.all()   # hoặc lọc theo điều kiện bạn muốn

    return render(request, 'main/sidebar_post_detail.html', {
        'post': post,
        
    })


# =========================
# HIỂN THỊ BÀI VIẾT LIÊN KẾT MENU
# =========================
def menu_articles_view(request, menu_id):
    """
    - Nếu menu là external → redirect sang link ngoài
    - Nếu internal → hiển thị các bài viết thuộc menu đó
    """
    menu_item = get_object_or_404(MenuItem, id=menu_id)

    # Nếu menu là external → redirect ra ngoài
    if menu_item.link_type == 'external' and menu_item.external_url:
        return redirect(menu_item.external_url)

    # Nếu menu là internal → hiển thị danh sách bài viết
    articles = menu_item.articles.filter(published=True).order_by('-created_at')
    # ✅ Thêm phân trang:
    paginator = Paginator(articles, 5)   # 10 bài / trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/menu_articles.html', {
        'menu_item': menu_item,
        'articles': articles,
        'page_obj': page_obj,  # truyền page_obj thay vì articles
        "paginator": paginator,
    })


# =========================
# HIỂN THỊ BÀI VIẾT THEO CHỦ ĐỀ RIÊNG
# =========================
def category_articles_view(request, slug):
    """
    Hiển thị bài viết theo chủ đề riêng
    """
    category = get_object_or_404(Category, slug=slug, is_visible=True)
    articles = category.articles.filter(published=True).order_by('-created_at')

    # ✅ Thêm phân trang:
    paginator = Paginator(articles, 5)   # 10 bài / trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/category_articles.html', {
        'category': category,
        'articles': articles,
        'page_obj': page_obj,
        "paginator": paginator,  # truyền page_obj thay vì articles
    })

# =========================
# HIỂN THỊ Bang giá dịch vụ
# =========================




def service_list(request):
    q = request.GET.get("q", "").strip()  # Lấy từ khóa, bỏ khoảng trắng
    services = Service.objects.all()
    if q:
        services = services.filter(name__icontains=q)

    # Phân trang: 100 dịch vụ mỗi trang
    paginator = Paginator(services, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "q": q,
        "paginator": paginator,
    }
    return render(request, "main/price_list.html", context)


def contact_view(request):
    contact = ContactInfo.objects.first()   # lấy bản ghi đầu tiên
    return render(request, "main/includes/contact.html", {"contact": contact})

def about_view(request):
    return render(request, "main/about.html")

def sodo_view(request):
    return render(request, "main/sodo.html")


def item_posts(request, item_id):
    """
    Hiển thị tất cả bài viết thuộc 1 mục con (SideBarItem)
    """
    item = get_object_or_404(SideBarItem, id=item_id)
    posts = item.posts.all()   # hoặc .filter(...) nếu cần sắp xếp
    return render(request, 'main/sidebar_post_detail.html', {
        'item': item,
        'posts': posts,
    })