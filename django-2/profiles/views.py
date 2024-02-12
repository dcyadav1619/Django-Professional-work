from typing import Any
from django.contrib.auth.models import User
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import DetailView,View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse,HttpResponseBadRequest
# Create your views here.
from myapp.models import Post
from follower.models import Follower

class PostDetailView(DetailView):
    http_method_names = ['get']
    template_name = "profiles/details.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_post'] = Post.objects.filter(author=user).count()
        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, follow_by=self.request.user).exists()
        return context

class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self,request,*args,**kwargs):
        data = request.POST.dict()
        print("--------",data)
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data.")
        try:
            other_user = User.objects.get(username=data(['username']))
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing data.")
        if data['action']=="follow":
            #follow
            follower,created=Follower.ojecects.get_or_create(
                followed_by = request.user,
                following = other_user
            )
        else:
            #unfollow
            try:
                follower = Follower.objects.get(
                    followed_by = request.user,
                    following = other_user,
                )
            except Follower.DoesNotExit:
                follower=None

        return JsonResponse({
            'done':True,
            'wording':"Unfollow" if data['action']=="follow" else "Unfollow"
        })
