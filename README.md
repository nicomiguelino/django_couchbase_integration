# Inegrating Couchbase with Django

For the meantime, we will be integrating Couchbase Python SDK with Django since it's difficult to find an up-to-date ODM.


## Experimental Contents

**Disclaimer:** The contents in this repo are experimental and open for changes.

Here's the list of improvement items that we aim to fully implement in the future...
- Integrating [marshmallow](https://marshmallow.readthedocs.io/en/stable/) and [Couchbase Python client](https://github.com/couchbase/couchbase-python-client) with Django.
- Flushing buckets via Couchbase Python client.


## Adding a Couchbase Model

Here's a sample snippet to creating new Couchbase models. Take note that the new model should inherit from `CouchbaseModel` implemented in [main/cbmodels.py](/main/cbmodels.py).

```python
class CouchbaseModel:
    # Possible Improvement Item - We could get the bucket name from settings.py
    # via django.conf.settings (assuming that CB_BUCKET_NAME is specified in settings.py).
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
```

Here's another snippet showing a new Couchbase model.

```python
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
```


## Sample Output (Screenshots)

![screenshot_01](/images/screenshot_01.png)


## References

- [Couchbase - Install and Start Using the Python SDK with Couchbase Server](https://docs.couchbase.com/python-sdk/3.0/hello-world/start-using-sdk.html)
- [Official Marshmallow Documentation](https://marshmallow.readthedocs.io/en/stable/)
