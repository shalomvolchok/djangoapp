from django.views.generic import TemplateView

class HomeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['msg']="HELLO WORLD"
        return context    
    
