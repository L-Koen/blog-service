from django.shortcuts import render
from django.views.generic import ListView, DetailView
from posts.models import Post, Keyword


class HomePageView(ListView):
    """Home view for the blog app."""
    model = Post
    template_name = "posts/blog_home.html"
    context_object_name = "posts"
    paginate_by = 5
    ordering = "-id"

    def get_context_data(self, **kwargs):
        """Add the keywords when fetching context"""
        context = super().get_context_data(**kwargs)
        context["available_keywords"] = Keyword.objects.order_by("name")
    
        return context

    def get_queryset(self):
        """Make sure I can filter on keyword and use the AND/OR setting"""
        queryset = super().get_queryset()
        
        # Get keywords / filter mode / text search from query parameters
        keywords_str = self.request.GET.get("keywords", '')
        keywords_list = [kw.strip() for kw in keywords_str.split(",") if kw.strip()] 
        filter_mode = self.request.GET.get("filter_mode", "OR").upper()
        text_search = self.request.GET.get("search", "").strip()
        
        # Keyword filtering
        if keywords_list:            
            # Filter by based on the filter mode
            if filter_mode == "AND":
                for keyword in keywords_list:
                    queryset = queryset.filter(keywords__name=keyword)
            else: # Default to OR behavior
                queryset = queryset.filter(keywords__name__in=keywords_list).distinct()

        # Text based (slow) filtering
        if text_search:
            queryset = queryset.filter(content__icontains=text_search)        
        
        print(queryset)
        return queryset


class PostDetailView(DetailView):
    """View for displaying a single blog post."""
    model = Post
    template_name = "posts/post_detail.html"