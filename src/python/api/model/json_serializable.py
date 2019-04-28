import json
import collections


class JsonClassSerializable(json.JSONEncoder):
    REGISTERED_CLASS = {}

    def register(ctype):
        JsonClassSerializable.REGISTERED_CLASS[ctype.__name__] = ctype

    def default(self, obj):
        if isinstance(obj, collections.Set):
            return dict(_set_object=list(obj))
        if isinstance(obj, JsonClassSerializable):
            jclass = {}
            jclass["name"] = type(obj).__name__
            jclass["dict"] = obj.__dict__
            return dict(_class_object=jclass)
        else:
            return json.JSONEncoder.default(self, obj)

    def json_to_class(self, dct):
        if '_set_object' in dct:
            return set(dct['_set_object'])
        elif '_class_object' in dct:
            cclass = dct['_class_object']
            cclass_name = cclass["name"]
            if cclass_name not in self.REGISTERED_CLASS:
                raise RuntimeError(
                    "Class {} not registered in JSON Parser"
                        .format(cclass["name"])
                )
            instance = self.REGISTERED_CLASS[cclass_name]()
            instance.__dict__ = cclass["dict"]
            return instance
        return dct

    def tojson(self, pretty=False):

        raw_dict = self.__dict__
        filtered_dict = {k: raw_dict[k] for k in self.serializables if k in raw_dict}

        return json.dumps(
            filtered_dict,
            cls=JsonClassSerializable,
            indent=(4 if pretty else None),
            sort_keys=True
        )

    def dump(self, file):
        with open(file, 'w') as outfile:
            json.dump(
                self.__dict__, outfile,
                cls=JsonClassSerializable,
                indent=4,
                sort_keys=True
            )

    def load(self, file):
        try:
            with open(file, 'r') as infile:
                self.__dict__ = json.load(
                    infile,
                    object_hook=self.json_to_class
                )
        except FileNotFoundError:
            print("Persistence load failed "
                  "'{}' do not exists".format(file)
                  )

    def fromjson(self, string):
        self.__dict__ = json.loads(
            string,
            object_hook=self.json_to_class
        )

    # def __init__(self, **kwargs):
    #     for key in kwargs:
    #         setattr(self, key, kwargs[key])

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
