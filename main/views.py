from django.views.generic import TemplateView
from blog.models import Blog
from user.models import Mailing


# Create your views here.
class SiteTemplate(TemplateView):
    template_name = 'main/general.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog_list'] = Blog.objects.order_by('?')[:3]
        context_data['mail_counts'] = Mailing.objects.all().count()
        context_data['active_mail_counts'] = Mailing.objects.filter(status=True).count()
        return context_data
