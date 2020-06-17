from django.shortcuts import render
from django.views import View

from .cbmodels import UserCouchbaseModel

class IndexView(View):
    def get(self, request):
        user_couchbase_model = UserCouchbaseModel()
        user_couchbase_model.insert_sample_values()
        user = user_couchbase_model.get_data('u:0002').content

        return render(request, 'main/index.html', user)
