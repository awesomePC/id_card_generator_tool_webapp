from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import redirect
from django.shortcuts import render
from tasks.models import Tasks
from dataset.models import Dataset


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""
class ViewData(TemplateView):
    template_name = 'pages/dataset/generate_dataset.html'
    
    def dispatch(self, request, id, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            return super(ViewData, self).get(request, *args, **kwargs)
                    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Call the base implementation first to get a context
        context = KTLayout.init(context)
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
        return context

