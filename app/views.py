from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.forms import ModelForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import *
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class CreateForm(ModelForm):
        max_upload_limit = 2 * 1024 * 1024
        picture = forms.FileField(required=False, label='File to upload <= 2Mb')
        uploaded_field_name = 'picture'

        class Meta:
            model = ForumList
            fields = ['title', 'text', 'picture']

        def clean(self):
            cleaned_data = super().clean()
            pic = cleaned_data.get('picture')
            if pic is None:
                return
            if len(pic) > self.max_upload_limit:
                self.add_error('picture', 'File must be <= 2Mb')

        def save(self, commit=True):
            instance = super(CreateForm, self).save(commit=False)
            f = instance.picture
            if isinstance(f, InMemoryUploadedFile):
                bytearr = f.read()
                instance.content_type = f.content_type
                instance.picture = bytearr
            if commit:
                instance.save()
            return instance


class CommentsForm(forms.Form):
    comment = forms.CharField(required=True, max_length=1000, strip=True)


class MainView(ListView):
    model = ForumList
    template_name = 'app/main.html'

    def get(self, request):
        strval = request.GET.get("search", False)
        if strval:
            query = Q(title__contains=strval)
            query.add(Q(text__contains=strval), Q.OR)
            objects = ForumList.objects.filter(query).select_related().order_by('-updated_at')
        else:
            objects = ForumList.objects.all().order_by('-updated_at')

        if request.user.is_authenticated:
            rows = request.user.favorite_forum.values('id')
            favorites = [row['id'] for row in rows]
            cntx = {'forum_list': objects, 'favorites': favorites, 'search': strval}
        else:
            cntx = {'forum_list': objects, 'search': strval}
        return render(request, self.template_name, cntx)


class ForumDetailsView(DetailView):
    model = ForumList
    fields = '__all__'
    template_name = 'app/forum_details.html'

    def get(self, request, pk):
        x = ForumList.objects.get(id=pk)
        comments = Comments.objects.filter(forum=x).order_by('-updated_at')
        comment_form = CommentsForm()
        context = {'forum': x, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)


def stream_file(request, pk):
    pic = get_object_or_404(ForumList, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response


class CreateForum(LoginRequiredMixin, View):
    model = ForumList
    template_name = 'app/create_forum.html'
    success_url = reverse_lazy('app:main')

    def get(self, request, pk=None):
        form = CreateForm()
        cntx = {'form': form}
        return render(request, template_name=self.template_name, context=cntx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            cntx = {'form': form}
            return render(request, self.template_name, cntx)
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        return redirect(self.success_url)


class DeleteForum(LoginRequiredMixin, DeleteView):
    model = ForumList
    template_name = 'app/delete_forum.html'
    success_url = reverse_lazy('app:main')


class UpdateForum(LoginRequiredMixin, UpdateView):
    template_name = 'app/update_forum.html'
    success_url = reverse_lazy('app:main')

    def get(self, request, pk):
        pic = get_object_or_404(ForumList, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        cntx = {'form': form}
        return render(request, self.template_name, cntx)

    def post(self, request, pk=None):
        pic = get_object_or_404(ForumList, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)
        if not form.is_valid():
            cntx = {'form': form}
            return render(request, self.template_name, cntx)
        pic = form.save(commit=False)
        pic.save()
        return redirect(self.success_url)


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, pk):
        f = get_object_or_404(ForumList, id=pk)
        comment = Comments(comment=request.POST['comment'], commenter=request.user, forum=f)
        comment.save()
        return redirect(reverse('app:forum_details', args=[pk]))


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    fields = ['comment']

    def get_success_url(self):
            forum = self.object.forum
            return reverse('app:forum_details', args=[forum.id])


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'app/delete_comment.html'

    def get_success_url(self):
        forum = self.object.forum
        return reverse('app:forum_details', args=[forum.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavorite(LoginRequiredMixin, View):
    def post(self, request, pk):
        t =  get_object_or_404(ForumList, id=pk)
        fav = Fav(user=request.user, forum=t)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavorite(LoginRequiredMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(ForumList, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, forum=t).delete()
        except IntegrityError as e:
            pass
        return HttpResponse()
