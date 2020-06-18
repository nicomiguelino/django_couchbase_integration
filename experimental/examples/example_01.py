import uuid

from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

"""Improvement Items
- You could let marshmallow do the serialization/deserialization. Refer to
  https://marshmallow.readthedocs.io/en/stable/ for documentation.
- Add support for flushing buckets.
"""

class CouchbaseConfig:
    USERNAME = 'Administrator'
    PASSWORD = 'Administrator'
    URL = 'couchbase://localhost'
    BUCKET_NANE = 'django'


class CouchbaseHelper:
    password_authenticator = PasswordAuthenticator(CouchbaseConfig.USERNAME, CouchbaseConfig.PASSWORD)
    cluster_options = ClusterOptions(password_authenticator)

    cluster = Cluster(CouchbaseConfig.URL, cluster_options)
    bucket = cluster.bucket(CouchbaseConfig.BUCKET_NANE)
    collection = bucket.default_collection()

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())


class User(CouchbaseHelper):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.email = kwargs.get('email', None)
        self.interests = kwargs.get('interests', None)

    def save(self):
        self.collection.upsert(str(uuid.uuid4()), {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'interests': self.interests
        })


def run():
    user = User(
        first_name='Lindsey', last_name='Jordan',
        email='lindsey.jordan@snailmail.com',
        interests=[
            'Indie Music',
            'Ice Hockey'
        ]
    )

    user.interests.append('Guitars')
    user.save()
