from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from .models import Thread, ChatMessage
admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage
# class ThreadForm(ModelForm):
#     class Meta:
#         model = Thread
#         fields =["first_person", "second_person"]
#     def clean(self):
#         super(ThreadForm, self).clean()
#         first_person = self.cleaned_data.get('first_person')
#         second_person = self.cleaned_data.get('second_person')
#         lookup = Q(first_person=first_person) & Q(second_person=second_person) | Q(first_person=second_person) & Q(second_person=first_person)
#         # lookup = Q(lookup1 | lookup2)
#         qs = Thread.objects.filter(lookup)
#         if qs.exists():
#             self._errors['first_person'] = self.error_class([
#                 'Already exist'])
#             raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)