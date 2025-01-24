from django.utils import timezone

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Category
from .utils import filter_published_posts

# Create your views here.


class IndexListView(ListView):
    """Обработка запроса для передачи списка постов"""

    model = Post
    queryset = filter_published_posts(Post.
                                      objects.select_related('category').all())
    paginate_by = 5
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    """Обрабатывает запрос по адресу posts/<int:id>/"""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        if (post.pub_date > timezone.now() or not post.is_published
                or (post.category and not post.category.is_published)):
            raise Http404("Публикация недоступна.")
        return post


class CategoryListView(ListView):
    """Обрабатывает запрос по адресу category/<slug:category_slug>/"""

    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category,
                                     slug=category_slug, is_published=True)
        return filter_published_posts(category.post_categories.select_related('category').all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return context
