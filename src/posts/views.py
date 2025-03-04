from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings
from posts.models import Post, Keyword

BASE_DIR = settings.BASE_DIR

class HomePageView(ListView):
    """Home view for the blog app."""
    model = Post
    template_name = str(BASE_DIR) + '/posts/templates/posts/blog_home.html'
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-id"

    def get_context_data(self, **kwargs):
        """Add the keywords when fetching context"""
        context = super().get_context_data(**kwargs)

        # Fetch all keywords for selection box
        context["available_keywords"] = Keyword.objects.all().order_by("name")
    
        return context

    def get_queryset(self):
        """Make sure I can filter on keyword and use the AND/OR setting"""
        queryset = super().get_queryset()
        
        # Get keywords / filter mode / text search from query parameters
        keywords_str = self.request.GET.get("keywords", '')
        filter_mode = self.request.GET.get("filter_mode", '')
        text_search = self.request.GET.get("search", "").strip()
        
        # Keyword filtering
        if keywords_str:
            keywords_list = keywords_str.split(',')
            
            # Filter by based on the filter mode
            if filter_mode == 'OR':
                queryset = queryset.filter(keywords__name__in=keywords_list)
            elif filter_mode == 'AND':
                for keyword in keywords_list:
                    queryset = queryset.filter(keywords__name=keyword)

        # Text based (slow) filtering
        if text_search:
            queryset = queryset.filter(content__icontains=text_search)

        
        
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = str(BASE_DIR) + '/posts/templates/posts/post_detail.html'