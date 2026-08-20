from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Service
from .resources import ServiceResource
from .models import (
    Category,
    MenuItem,
    Article,
    SideBar,
    SideBarItem,
    SideBarPost,
    Banner,PageView, RunningText, CarouselImage, Service, ContactInfo, ScheduleCategory, ScheduleItem
)

# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_visible')
    list_filter = ('is_visible',)
    search_fields = ('name', 'slug')
    ordering = ('order', 'name')


# =========================
# MENU ITEM ADMIN
# =========================
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'link_type', 'order', 'is_visible')
    list_filter = ('link_type', 'is_visible')
    search_fields = ('name',)
    filter_horizontal = ('articles',)  # Cho phép chọn nhiều bài viết dễ dàng
    ordering = ['order']

admin.site.register(MenuItem, MenuItemAdmin)


# =========================
# ARTICLE ADMIN
# =========================
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Cột hiển thị trong danh sách
    list_display = ('title', 'category', 'published', 'created_at')
    # Bộ lọc bên phải
    list_filter = ('published', 'category', 'created_at')
    # Ô tìm kiếm
    search_fields = ('title', 'content')
    # Cho phép lọc theo mốc thời gian
    date_hierarchy = 'created_at'
    # Sắp xếp mặc định
    ordering = ('-created_at',)

   


# =========================
# SIDEBAR ADMIN
# =========================
class SideBarItemInline(admin.TabularInline):
    model = SideBarItem
    extra = 1


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'order')
    list_filter = ('position',)
    search_fields = ('title',)
    ordering = ['order']
    inlines = [SideBarItemInline]

admin.site.register(SideBar, SideBarAdmin)


# =========================
# SIDEBAR POST ADMIN
# =========================
@admin.register(SideBarPost)
class SideBarPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'sidebar', 'item', 'created_at')
    list_filter = ('sidebar', 'created_at')
    search_fields = ('title', 'slug', 'content')
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


# =========================
# BANNER ADMIN
# =========================
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ['order']

# =========================
#PageView ADMIN
# =========================
@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'created_at')
    list_filter = ('created_at', 'path')
    search_fields = ('ip_address', 'path')

# =========================
#RunningTex ADMIN
# =========================
@admin.register(RunningText)
class RunningTextAdmin(admin.ModelAdmin):
    list_display = ("content", "active")
    list_editable = ("active",)

# =========================
#CarouselImage ADMIN
# =========================
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')
    list_editable = ('order', 'active')

# =========================
#ServiceCategory ADMIN
# =========================

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        fields = (
            'id', 'order', 'code', 'name',
            'price_bhyt', 'price_non_bhyt', 'description'
        )
        import_id_fields = ('id',)  # dựa theo id để update nếu có

# Tích hợp vào admin
@admin.register(Service)
class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResource
    list_display = ('order', 'code', 'name', 'price_bhyt', 'price_non_bhyt')
    search_fields = ('name', 'code')
    ordering = ['order']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("title", "address", "phone", "email")   

# =========================
class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 1
    ordering = ('order',)
    fields = ('label', 'content', 'order', 'is_red')

@admin.register(ScheduleCategory)
class ScheduleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'main_title', 'order')
    list_editable = ('order',)
    list_filter = ('main_title',)
    ordering = ('main_title', 'order')
    inlines = [ScheduleItemInline]

@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'category', 'order', 'is_red')
    list_editable = ('order', 'is_red')
    list_filter = ('category', 'is_red')
    ordering = ('category', 'order')