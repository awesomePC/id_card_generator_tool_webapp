from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.shortcuts import redirect
from django.shortcuts import render
from tasks.models import Tasks
from dataset.models import Dataset, DatasetPastedBgMeta


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""
class PasteData(TemplateView):
    template_name = 'pages/dataset/paste_dataset.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            if request.method == 'POST':
                name = request.POST["data_set"]
                count = request.POST["data_count"]
                res_dataset_id = request.POST["select_dataset"]
                desc = request.POST["description"]
                generate_data = Dataset(
                    name = name,
                    count = count,
                    type = "pasted",
                    desc = desc
                )
                generate_data.save()

                #DatasetPastedBgMeta
                datasetpastedbgmeta = DatasetPastedBgMeta(
                    dataset_id = generate_data.id,
                    reference_dataset_id = res_dataset_id
                )
                datasetpastedbgmeta.save()
                ## TODO: redirect to dataset view -- pass id of dataset so it will be auto selected
                return redirect('dataset:view_dataset', id = generate_data.id)
            else:
                return super(PasteData, self).get(request, *args, **kwargs)
                    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Call the base implementation first to get a context
        context = KTLayout.init(context)
        userId=self.request.session.get('user',None)['id']
        context['datasets'] = list(Dataset.objects.values("id", "name"))
        return context