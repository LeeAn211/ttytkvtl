from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('bai-viet/<slug:slug>/', views.article_detail, name='article_detail'),
    path('bai-viet-sidebar/<slug:slug>/', views.sidebar_post_detail, name='sidebar_post_detail'),   
    path('menu/<int:menu_id>/', views.menu_articles_view, name='menu_articles'),
    path('bai-viet-chu-de/<slug:slug>/', views.category_articles_view, name='category_articles'),
    path('bang-gia/', views.service_list, name='banggia'),
    path("lien-he/", views.contact_view, name="lienhe"),
    path("gioi-thieu/", views.about_view, name="gioithieu"),
    path("so-do/", views.sodo_view, name="sodo"),
    path('item/', views.item_posts, name='item_posts')

  

    
 
]


