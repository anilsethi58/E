from django.shortcuts import render
from django.views.generic import (TemplateView, DetailView,
                                    ListView, CreateView,
                                    UpdateView,DeleteView,FormView)
from .models import Standard, Subject, Lesson
from django.urls import reverse_lazy
from .forms import LessonForm
# from .forms import CommentForm,ReplyForm, LessonForm

from django.http import HttpResponseRedirect



class StandardListView(ListView):
    context_object_name = 'standards'
    model = Standard
    template_name = 'cources/standard_list_view.html'

class SubjectListView(DetailView):
    context_object_name = 'standards'
    # extra_context = {
    #     'slots': TimeSlots.objects.all()
    # }
    model = Standard
    template_name = 'cources/subject_list_view.html'

class LessonListView(DetailView):
    context_object_name = 'subjects'
    model = Subject
    template_name = 'cources/lesson_list_view.html'

class LessonDetailView(DetailView):
    context_object_name = 'lessons'
    model = Lesson
    template_name = 'cources/lesson_detail_view.html'


class LessonCreateView(CreateView):
    # fields = ('lesson_id','name','position','image','video','ppt','Notes')
    form_class = LessonForm
    context_object_name = 'subject'
    model= Subject
    template_name = 'cources/lesson_create.html'

    def get_success_url(self):
        self.object = self.get_object()
        standard = self.object.standard
        return reverse_lazy('cources:lesson_list',kwargs={'standard':standard.slug,
                                                             'slug':self.object.slug})
    
    def form_valid(self, form, *args, **kwargs):
        self.object = self.get_object()
        fm = form.save(commit=False)
        fm.created_by = self.request.user
        fm.Standard = self.object.standard
        fm.subject = self.object
        fm.save()
        return HttpResponseRedirect(self.get_success_url())
    
class LessonUpdateView(UpdateView):
    fields = ('name','position','video','ppt','Notes')
    model= Lesson
    template_name = 'cources/lesson_update.html'
    context_object_name = 'lessons'

class LessonDeleteView(DeleteView ,FormView):
    model= Lesson
    context_object_name = 'lessons'
    template_name = 'cources/lesson_delete.html'



    def get_success_url(self):
        print(self.object)
        standard = self.object.Standard
        subject = self.object.subject
        return reverse_lazy('cources:lesson_list',kwargs={'standard':standard.slug,'slug':subject.slug})