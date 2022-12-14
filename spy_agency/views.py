from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic
from .models import SpyUser, Hit, Assignment, HitmanUser, BossUser,HitmanAssignedBoss
from .forms import HitForm, CustomUserCreationForm, CustomUserChangeForm, CreateAssignForm
from django.views.generic import  View
from django.db.models import Subquery
from django.views.generic.edit import UpdateView


def home_view(request):
    return render(request, 'home.html')


class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save(commit=False)
            user_type = request.POST.get("user_type")
            user = self.object
            self.object.save()
            if user_type == SpyUser.HITMAN:
                HitmanUser.objects.create(admin=user)
            elif user_type == SpyUser.BOSS:
                BossUser.objects.create(admin=user)
        return redirect('login')


def hits_view(request):
    user = request.user
    if user.is_authenticated:
        assignments = Assignment.objects.filter(assignee=user)
        if user.user_type == "2":
            assignments = Assignment.objects.filter(assignee__in=Subquery(
                            HitmanAssignedBoss.objects.filter(
                                boss__admin=user).values('hitman')))
        elif user.is_superuser:
            assignments = Assignment.objects.all()
        return render(request, 'hits.html', {'assignments': assignments})
    else:
        return redirect('login')


def hits_list(request):
    if request.user.is_superuser:
        hits = Hit.objects.all()
        return render(request, 'hits_list.html', {'hits': hits})
    else:
        return redirect('login')
    

class HitDetailsView(View):
    def get(self, request, pk):
        if request.user.user_type != "1":
            hit = Hit.objects.get(id=pk)
            context = {"hit": hit}
            return render(request, "hit_detail.html", context)
        else:
            return redirect('home')


def create_hit_view(request):
    user = request.user
    if user.user_type != "1":
        if request.method == 'POST':
            form = HitForm(request.POST)
            if form.is_valid():
                hit = form.save(commit=False)
                hit.creator = request.user
                hit.save()
                return redirect('home')
        else:
            form = HitForm()
            return render(request, 'create_hit.html', {'form': form})
    else:
        return redirect('hits')


def create_assignment_view(request):
    user = request.user
    if user.user_type != "1":
        if request.method == 'POST':
            form = CreateAssignForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = CreateAssignForm()
            return render(request, 'create_assignment.html', {'form': form})
    else:
        return redirect('hits')


def hitmen_view(request):
    User = get_user_model()
    user = request.user
    if user.user_type != "1":
        if user.user_type == "2":
            hitmen = User.objects.filter(id__in=Subquery(
                            HitmanAssignedBoss.objects.filter(
                                boss__admin=user).values('hitman')))
            print(hitmen)
        elif user.is_superuser:
            hitmen = User.objects.all()
        return render(request, 'hitmen.html', {'hitmen': hitmen})
    else:
        return redirect('home')


class HitmenDetailsView(View):
    def get(self, request, pk):
        if request.user.user_type != "1":
            User = get_user_model()
            user = User.objects.get(id=pk)
            context = {"user": user}
            return render(request, "hitmen_detail.html", context)
        else:
            return redirect("home")


class AssignmentUpdateView(UpdateView):
    model = Assignment
    fields = ['assignee', 'status_type']
    template_name_suffix = '_update_form'
    success_url ="/"

class HitUpdateView(UpdateView):
    model = Hit
    fields = ['description', 'target']
    template_name_suffix = '_update_form'
    success_url ="/"



class HitmenUpdateView(UpdateView):
    model = SpyUser
    fields = ['status_type']
    template_name_suffix = '_update_form'
    success_url ="/"
    def get(self, request, pk):
        if not request.user.is_superuser:
            return redirect("home")
