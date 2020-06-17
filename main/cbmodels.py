from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator


class CouchbaseModel:
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


class UserCouchbaseModel(CouchbaseModel):
    def __init__(self):
        super(UserCouchbaseModel, self).__init__()

    def insert_sample_values(self):
        self.insert_data('u:0001', {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@couchbase.com',
            'hobbies': [
                'reading books',
                'playing guitar'
            ]
        })

        self.insert_data('u:0002', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@couchbase.com',
            'hobbies': [
                'watching television'
            ]
        })

    def insert_data(self, identifier, data):
        self.collection.upsert(identifier, data)

    def get_data(self, identifier):
        return self.collection.get(identifier)
