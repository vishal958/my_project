from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import Post, Comment, Preference
from .forms import CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required

posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]
# Create your views here.

''' Using HTTPresponse
def home(request):
    return HttpResponse('<h1>Hello World</h1>')


def about(request):
    return HttpResponse('<h1>Blog About</h1>')
'''


def home(request):
    context = {
        # 'posts': post
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        loggedInUserPreference = False
        if self.request.user.is_authenticated:
            loggedInUserPreference = Preference.objects.filter(user=self.request.user)
        pref= {}
        j=0
        if loggedInUserPreference:
            for preference in loggedInUserPreference:
                pref[preference.post.id]=preference.value
                j=j+1
            
             
        context['preference']=pref
        return context
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(FormMixin, DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        comments = Comment.objects.filter(post=self.object)
        loggedInUserPreference = False
        if self.request.user.is_authenticated:
            loggedInUserPreference = Preference.objects.filter(user=self.request.user,
                                                            post=self.object)
        # print(self.object.likes)
        if loggedInUserPreference:
            # For like=1 ,dislike =2 for each user.
            context['preference'] = (loggedInUserPreference[0].value)
        # Total number of comments to the Post.
        context['comments'] = comments
        # Total number of likes to the Post.
        context['likes'] = self.object.likes
        # Total number of likes to the Post.
        context['dislikes'] = self.object.dislikes
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def postpreference(request):
    if request.method == "GET":
        postid = request.GET['post_id']
        userpreference = request.GET['userpreference']
        object = get_object_or_404(Post, id=postid)
        obj = ''
        valueobj = ''
        try:
            obj = Preference.objects.get(
                user=request.user, post=object)
            valueobj = obj.value  # value of userpreference
            valueobj = int(valueobj)
            userpreference = int(userpreference)
            if valueobj != userpreference:
                obj.delete()
                upref = Preference()
                upref.user = request.user
                upref.post = object
                upref.value = userpreference
                if userpreference == 1 and valueobj != 1:
                    object.likes += 1
                    object.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    object.dislikes += 1
                    object.likes -= 1
                upref.save()
                object.save()
                return HttpResponse("Success!")  # Sending an success response
            elif valueobj == userpreference:
                obj.delete()
                if userpreference == 1:
                    object.likes -= 1
                elif userpreference == 2:
                    object.dislikes -= 1
                object.save()
                return HttpResponse("Success!")  # Sending an success response

        except Preference.DoesNotExist:
            upref = Preference()
            upref.user = request.user
            upref.post = object
            upref.value = userpreference
            userpreference = int(userpreference)
            if userpreference == 1:
                object.likes += 1
            elif userpreference == 2:
                object.dislikes += 1
            upref.save()
            object.save()
            return HttpResponse("Success!")  # Sending an success response
    else:
        object = get_object_or_404(Post, id=postid)
        # Sending an success response
        return HttpResponse("Request method is not a GET")
