from django.views.generic import TemplateView

search = TemplateView.as_view(template_name='google_cse/search.html')
