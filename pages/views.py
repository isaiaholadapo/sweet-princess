from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import ContactForm

# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'pages/home.html'


class ContactView(SuccessMessageMixin, generic.CreateView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_view')
    success_message = 'Message has been sent successfully'
