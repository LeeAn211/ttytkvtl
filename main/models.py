from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.paginator import Paginator
from django.shortcuts import render
from autoslug import AutoSlugField
from unidecode import unidecode

# =========================
# CHỦ ĐỀ RIÊNG (CATEGORY)
# =========================
def vn_slugify(value):
    """Chuyển tiếng Việt → không dấu rồi slugify."""
    return slugify(unidecode(value))

class Category(models.Model):
    name = models.CharField("Tên chủ đề", max_length=200)
    slug = AutoSlugField(
        populate_from='name',
        slugify=vn_slugify,        # 👈 dùng hàm slugify tự định nghĩa
        unique=True,
        always_update=False
    )
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    is_visible = models.BooleanField(default=True, verbose_name="Hiển thị")

    class Meta:
        verbose_name = "Chủ đề"
        verbose_name_plural = "Danh sách chủ đề"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_articles', args=[self.slug])


# =========================
# MENU CHÍNH (MENU ITEM)
# =========================
class MenuItem(models.Model):
    LINK_TYPE_CHOICES = [
        ('internal', 'Liên kết bài viết nội bộ'),
        ('external', 'Liên kết ngoài'),
        ('named', 'Liên kết theo name'),       # ✅ thêm
    ]


    name = models.CharField("Tên menu", max_length=200)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Menu cha"
    )

    # Loại liên kết
    link_type = models.CharField(
        max_length=10,
        choices=LINK_TYPE_CHOICES,
        default='internal',
        verbose_name="Loại liên kết"
    )

    # Nếu là external → nhập link ngoài
    external_url = models.URLField(
        "Liên kết ngoài",
        max_length=500,
        blank=True,
        null=True,
        help_text="Nếu chọn liên kết ngoài, nhập URL tại đây"
    )
    named_url = models.CharField(
    "Tên urlpattern",
    max_length=100,
    blank=True,
    null=True,
    help_text="Nhập name của url trong urls.py"
)

    # Nếu là internal → chọn 1 hoặc nhiều bài viết
    articles = models.ManyToManyField(
        'Article',
        blank=True,
        related_name='menu_items',
        verbose_name="Bài viết liên kết"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    is_visible = models.BooleanField(default=True, verbose_name="Hiển thị trên menu")

    class Meta:
        verbose_name = "Mục menu"
        verbose_name_plural = "Các mục menu"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Trả về URL phù hợp:
        - Nếu là external → trả external_url
        - Nếu là internal → trả về trang hiển thị bài viết liên quan
        """
        if self.link_type == 'external' and self.external_url:
            return self.external_url
        elif self.link_type == 'named' and self.named_url:
            return reverse(self.named_url)
        return reverse('menu_articles', args=[self.id])


# =========================
# BÀI VIẾT CHÍNH
# =========================
def vn_slugify(value):
    """Chuyển tiếng Việt → không dấu rồi slugify."""
    return slugify(unidecode(value))

class Article(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles',
        verbose_name="Chủ đề riêng"
    )
    title = models.CharField(max_length=255, verbose_name="Tiêu đề")
    slug = AutoSlugField(
        populate_from='title',     # ✅ Sửa lại: dùng field title
        slugify=vn_slugify,
        unique=True,
        always_update=False
    )
    content = RichTextUploadingField(verbose_name="Nội dung", blank=True, null=True)

    image = models.ImageField(
        upload_to='articles/images/',
        null=True,
        blank=True,
        verbose_name="Hình minh họa"
    )
    attachment = models.FileField(
        upload_to='articles/files/',
        null=True,
        blank=True,
        verbose_name="Tệp đính kèm"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    published = models.BooleanField(default=True, verbose_name="Đã xuất bản")

    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Danh sách bài viết"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])
    


# =========================
# SIDEBAR
# =========================


class SideBar(models.Model):
    POSITION_CHOICES = [
        ('left', 'Bên trái'),
        ('right', 'Bên phải'),
    ]

    title = models.CharField(max_length=100, verbose_name="Tiêu đề Sidebar")
    image = models.ImageField(
        upload_to='sidebar_images/',
        null=True,
        blank=True,
        verbose_name="Hình đại diện"
    )
    url = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Liên kết khi click"
    )
    position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        default='left',
        verbose_name="Vị trí hiển thị"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Sidebar"
        verbose_name_plural = "Danh sách Sidebar"
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_link(self):
        return self.url or "#"
    
    def get_main_posts(self):
    # lấy các bài không gắn vào SideBarItem
        return self.posts.filter(item__isnull=True)



class SideBarItem(models.Model):
    sidebar = models.ForeignKey(
        SideBar,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Sidebar"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Mục cha"
    )
    title = models.CharField(max_length=100, verbose_name="Tiêu đề mục con")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name="Liên kết")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Mục con trong Sidebar"
        verbose_name_plural = "Danh sách mục con"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.sidebar.title})"

    def get_url(self):
        if self.url:
            return self.url
        first_post = self.posts.first()
        return first_post.get_absolute_url() if first_post else "#"


class SideBarPost(models.Model):
    sidebar = models.ForeignKey(
        SideBar,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Sidebar"
    )
    item = models.ForeignKey(
        SideBarItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="Mục con"
    )
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Tiêu đề bài viết")
    slug = AutoSlugField(
        populate_from='title',        # ✅ sửa lại: slug tự sinh từ title
        slugify=vn_slugify,           # hàm slugify tiếng Việt tự định nghĩa
        unique=True,
        always_update=False
    )
    content = RichTextUploadingField(verbose_name="Nội dung", blank=True, null=True)
    image = models.ImageField(upload_to='sidebar_posts/', null=True, blank=True, verbose_name="Hình minh họa")
    external_url = models.URLField(blank=True, null=True, verbose_name="Đường dẫn ngoài")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Bài viết Sidebar"
        verbose_name_plural = "Danh sách bài viết Sidebar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Bài viết không tiêu đề"

    def get_absolute_url(self):
        return self.external_url if self.external_url else reverse('sidebar_post_detail', args=[self.slug])


# =========================
# BANNER
# =========================
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tiêu đề")
    image = models.ImageField(upload_to='banners/', verbose_name="Ảnh banner")
    url = models.URLField(blank=True, null=True, verbose_name="Liên kết khi click")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Danh sách Banner"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else "Banner"
# =========================
# PageView
# =========================

class PageView(models.Model):
    """
    Lưu lượt truy cập từng trang
    """
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Địa chỉ IP")
    user_agent = models.CharField(max_length=255, blank=True, verbose_name="Trình duyệt")
    path = models.CharField(max_length=255, verbose_name="Đường dẫn truy cập")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian truy cập")

    class Meta:
        verbose_name = "Lượt truy cập"
        verbose_name_plural = "Thống kê lượt truy cập"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ip_address} - {self.path} ({self.created_at:%d/%m/%Y %H:%M})"


# =========================
# RunningText chữ chạy
# =========================
class RunningText(models.Model):
    content = models.CharField(
        max_length=255,
        verbose_name="Nội dung chữ chạy"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Hiển thị"
    )

    class Meta:
        verbose_name = "Chữ chạy (marquee)"
        verbose_name_plural = "Chữ chạy (marquee)"

    def __str__(self):
        # Hiển thị một phần nội dung trong admin list
        return self.content[:50]
# =========================
# CarouselImage
# =========================    
class CarouselImage(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Tiêu đề ảnh",
        blank=True
    )
    caption = models.TextField(
        verbose_name="Mô tả/ngắn gọn",
        blank=True
    )
    image = models.ImageField(
        upload_to='carousel/',
        verbose_name="Ảnh"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Thứ tự sắp xếp"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Hiển thị"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Ảnh Carousel"
        verbose_name_plural = "Ảnh Carousel"

    def __str__(self):
        return self.title or f"Ảnh {self.pk}"
    
# =========================
# ServiceCategory
# =========================   
class Service(models.Model):
    order = models.PositiveIntegerField(default=0, verbose_name="STT")
    code = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Mã tương đương"
    )
    name = models.CharField(max_length=255, verbose_name="Tên dịch vụ")
    price_bhyt = models.IntegerField(verbose_name="Mức giá BHYT thanh toán")
    price_non_bhyt = models.IntegerField(verbose_name="Mức giá không thuộc BHYT")
    description = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        verbose_name = "Dịch vụ"
        verbose_name_plural = "Dịch vụ"
        ordering = ['order']

    def __str__(self):
        return self.name
# =========================
# ContactInfo
# =========================  

class ContactInfo(models.Model):
    title = models.CharField(
        max_length=100,
        default="Thông tin liên hệ",
        verbose_name="Tiêu đề"
    )
    address = models.CharField(max_length=255, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=50, verbose_name="Điện thoại")
    email = models.EmailField(verbose_name="Email")
    working_hours = models.CharField(max_length=100, verbose_name="Giờ làm việc")
    map_iframe = models.TextField(
        verbose_name="Google Maps iframe",
        help_text="Dán toàn bộ mã iframe nhúng bản đồ Google Maps"
    )

    class Meta:
        verbose_name = "Thông tin liên hệ"
        verbose_name_plural = "Thông tin liên hệ"

    def __str__(self):
        return self.title

# =========================
class ScheduleCategory(models.Model):
    main_title = models.CharField(
        "Tiêu đề chung",
        max_length=255,
        default="LỊCH KHÁM BỆNH",
        help_text="Ví dụ: LỊCH KHÁM BỆNH / THỜI GIAN LÀM VIỆC"
    )
    title = models.CharField("Tiêu đề khối", max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['main_title', 'order']  # ✅ quan trọng

    def __str__(self):
        return self.title

    @property
    def ordered_items(self):
        # luôn trả về items đã sắp xếp
        return self.items.order_by('order')


class ScheduleItem(models.Model):
    category = models.ForeignKey(
        ScheduleCategory,
        on_delete=models.CASCADE,
        related_name='items'
    )
    label = models.CharField("Tiêu đề dòng", max_length=255)
    content = models.TextField("Nội dung chi tiết")
    order = models.PositiveIntegerField(default=0)
    is_red = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']   # ✅ quan trọng

    def __str__(self):
        return f"{self.label}: {self.content[:30]}"