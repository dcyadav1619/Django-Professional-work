#from django.shortcuts import render
# Create your views here.
from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.request import HttpRequest as HttpRequest
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
#CRUD
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class HomePage(ListView):
    http_method_names = ["get"]
    template_name = "homepage.html"
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.all().order_by('-id')[:30] 

class PostDetailView(DetailView):
    http_method_names=['get']
    template_name = "detail.html"
    model = Post
    context_object_name = "post"

class CreateNewPost(LoginRequiredMixin,CreateView):
    model=Post
    template_name="create.html"
    fields = ['text']
    success_url = '/'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)
    



