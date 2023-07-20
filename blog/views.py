from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.views import View
from .forms import PostForm, CommentForm
from .models import Post, Comment

import os
from django.conf import settings
from django.http import JsonResponse


# def upload_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         print(image)
#         # Save the image or process it as needed
#         # Here, we'll just return the URL where the image is stored
#         image_url = '/static/' + image.name
#         return JsonResponse({'image_url': image_url})
#     return JsonResponse({'error': 'Invalid request'}, status=400)


def upload_image(request, post_id=None):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        print('URL : ', settings.MEDIA_URL)
        print('ROOT : ', settings.MEDIA_ROOT)
        # Generate a unique filename for the uploaded image
        filename = image.name
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        local_path = 'http://127.0.0.1:8000/media'
        # upload_path = os.path.join(local_path, 'uploads', filename)

        # Save the image to the static folder
        with open(upload_path, 'wb') as file:
            for chunk in image.chunks():
                file.write(chunk)

        # Create the URL for the uploaded image
        image_url = local_path + '/uploads/' + filename

        return JsonResponse({'image_url': image_url})

    return JsonResponse({'error': 'Invalid request'}, status=400)


class PostList(View):
    def get(self, request):
        # sort 방법 추출
        if request.GET.get('sort'):
            sort = request.GET.get('sort')
        else:
            sort = 'created_at'
        # post 데이터 by ORM
        posts = Post.objects.all()
        posts_sorted = sorted(
            posts, key=lambda x: getattr(x, sort), reverse=True)

        # 페이지당 보여줄 포스트 수
        posts_per_page = 6

        # 현재 페이지 번호 가져오기
        page_number = request.GET.get('page', 1)

        # Paginator 객체 생성
        paginator = Paginator(posts_sorted, posts_per_page)

        try:
            # 현재 페이지에 해당하는 포스트 가져오기
            page = paginator.page(page_number)
        except InvalidPage:
            # 유효하지 않은 페이지 번호일 경우 첫 번째 페이지로 이동
            page = paginator.page(1)

        context = {
            "posts": page,
            "sort": sort,
        }
        return render(request, "blog/post_list.html", context)


class PostListHot(View):
    def get(self, request):
        # sort 방법 추출
        if request.GET.get('sort'):
            sort = request.GET.get('sort')
        else:
            sort = 'created_at'
        # post 데이터 by ORM
        posts = Post.objects.filter(likes__gte=5)
        posts_sorted = sorted(
            posts, key=lambda x: getattr(x, sort), reverse=True)

        # 페이지당 보여줄 포스트 수
        posts_per_page = 6

        # 현재 페이지 번호 가져오기
        page_number = request.GET.get('page', 1)

        # Paginator 객체 생성
        paginator = Paginator(posts_sorted, posts_per_page)

        try:
            # 현재 페이지에 해당하는 포스트 가져오기
            page = paginator.page(page_number)
        except InvalidPage:
            # 유효하지 않은 페이지 번호일 경우 첫 번째 페이지로 이동
            page = paginator.page(1)

        context = {
            "posts": page,
            "sort": sort,
        }
        return render(request, "blog/post_list.html", context)


class PostListCategory(View):
    def get(self, request, category):
        # sort 방법 추출
        if request.GET.get('sort'):
            sort = request.GET.get('sort')
        else:
            sort = 'created_at'
        # post 데이터 by ORM
        posts = Post.objects.filter(category=category)
        print(posts)
        posts_sorted = sorted(
            posts, key=lambda x: getattr(x, sort), reverse=True)

        # 페이지당 보여줄 포스트 수
        posts_per_page = 6

        # 현재 페이지 번호 가져오기
        page_number = request.GET.get('page', 1)

        # Paginator 객체 생성
        paginator = Paginator(posts_sorted, posts_per_page)

        try:
            # 현재 페이지에 해당하는 포스트 가져오기
            page = paginator.page(page_number)
        except InvalidPage:
            # 유효하지 않은 페이지 번호일 경우 첫 번째 페이지로 이동
            page = paginator.page(1)

        context = {
            "posts": page,
            "sort": sort,
        }
        return render(request, "blog/post_list.html", context)


class PostWrite(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request):
        form = PostForm
        context = {
            "form": form,
        }
        # return render(request, "django_tuieditor/editor.html")
        return render(request, "blog/post_write.html", context)

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.content = request.POST['content']
            post.save()
            return redirect("blog:list")
        return redirect("blog:list")


class PostDetail(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        post.views += 1
        post.save()
        context = {
            "post": post,
            "comment_form": CommentForm,
        }
        print(post_id)
        return render(request, "blog/post_detail.html", context)


class PostEdit(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(instance=post)
        context = {
            "form": form,
            "post": post,
        }
        return render(request, "blog/post_edit.html", context)

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = PostForm(request.POST, instance=post)
        print(form)
        if form.is_valid():
            form.content = request.POST['content']
            form.save()
            return redirect("blog:detail", post_id=post_id)
        return redirect("blog:list")


class PostDelete(View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.delete()
        return redirect("blog:list")


class PostSearch(View):
    def get(self, request):
        query = request.GET.get('q')
        opt = request.GET.get('q-opt')

        # 빈 쿼리 또는 select 에러 시 전체 list
        if not query or opt not in '1234':
            return redirect('blog:list')

        # select에 따른 qeury 결과
        if opt == '1':  # 제목/내용
            result = list(Post.objects.filter(
                Q(content__icontains=query) | Q(title__icontains=query)).order_by('-created_at'))
        elif opt == '2':  # 댓글
            comments = list(Comment.objects.filter(
                content__icontains=query).order_by('-created_at'))
            result = [comment.post for comment in comments]
        elif opt == '3':  # 카테고리
            pass
        elif opt == '4':  # 태그
            pass
        else:
            result = None

        # rusult에 따른 context
        if result:
            context = {
                'posts': result
            }
        else:
            context = {
                'posts': None,
                'query': True,
            }
        return render(request, "blog/post_list.html", context)


class PostLike(View):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if not post:
            return render(request, 'blog/post_error.html', {'error': '존재하지 않는 페이지입니다'})
        post.views -= 1
        post.likes += 1
        post.save()
        return redirect('blog:detail', post_id)


# Comment
class CommentWrite(LoginRequiredMixin, View):
    login_url = 'user:login'

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.writer = request.user
            comment.save()
            return redirect("blog:detail", post_id=post_id)


class CommentDelete(View):
    def post(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        post = comment.post
        comment.delete()
        return redirect("blog:detail", post_id=post.pk)
