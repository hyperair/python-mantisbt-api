from suds.client import Object as SudsObject


class TypeRegistry(object):
    def __init__(self, base_type):
        self.constructors = {}
        self.base_type = base_type

    def register_type(self, name):
        def decorator(constructor):
            self.constructors[name] = constructor
            return constructor

        return decorator

    def __getitem__(self, name):
        return self.constructors.get(name, self.base_type)


class MantisObject(object):
    def __new__(cls, obj, client, *args, **kwargs):
        if cls is MantisObject:
            if isinstance(obj, SudsObject):
                cls = registry[obj.__class__.__name__]

            elif isinstance(obj, list):
                return [cls(item, client) for item in obj]

            elif isinstance(obj, dict):
                return dict((k, cls(item, client))
                            for k, item in obj.iteritems())

        return object.__new__(cls, obj, client, *args, **kwargs)

    def __init__(self, obj, client):
        self._obj = obj
        self._client = client

    def __getattr__(self, attr):
        return MantisObject(getattr(self._obj, attr), self._client)


registry = TypeRegistry(MantisObject)


@registry.register_type("ProjectData")
class Project(MantisObject):
    def get_issues(self, page=1, window_size=100):
        return [MantisObject(issue, self._client)
                for issue in self._client.project_get_issues(self, page,
                                                             window_size)]
