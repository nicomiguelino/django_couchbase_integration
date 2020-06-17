from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

from django.shortcuts import render
from django.views import View

class CouchbaseHelper:
    CB_BUCKET_NAME = 'django'

    def __init__(self):
        self.cluster = None
        self.collection = None

        self.initialize_cluster()
        self.initialize_collection()

    def initialize_cluster(self):
        password_authenticator = PasswordAuthenticator(
            'Administrator', 'Administrator')
        cluster_options = ClusterOptions(password_authenticator)
        self.cluster = Cluster('couchbase://localhost', cluster_options)

    def initialize_collection(self):
        bucket = self.cluster.bucket(self.CB_BUCKET_NAME)

        try:
            self.cluster.query_indexes().create_primary_index(
                self.CB_BUCKET_NAME)
        except:
            pass

        self.collection = bucket.default_collection()

    def insert_data(self, identifier, data):
        self.collection.upsert(identifier, data)

    def get_data(self, identifier):
        return self.collection.get(identifier)



class IndexView(View):
    def get(self, request):
        couchbase_helper = CouchbaseHelper()

        couchbase_helper.insert_data('u:0001', {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@couchbase.com',
            'hobbies': [
                'reading books',
                'playing guitar'
            ]
        })

        couchbase_helper.insert_data('u:0002', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@couchbase.com',
            'hobbies': [
                'watching television'
            ]
        })

        jane_doe = couchbase_helper.get_data('u:0001')

        return render(request, 'main/index.html', jane_doe.content)
