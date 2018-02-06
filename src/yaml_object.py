class YamlObject:
    class Field:
        def __init__(self, data):
            self.name = ''
            self.type = ''
            self.parse_data(data)

        def parse_data(self, data):
            self.name, props = data.popitem()

            while len(props) > 0:
                name, val = props.popitem()
                if name == 'type':
                    self.type = val

    def __init__(self, data):
        self.class_name = ''
        self.fields = []
        self.parse_data(data)

    def parse_data(self, data):
        self.class_name, fields = data.popitem()

        name, props = fields.popitem()

        if name == 'fields':
            for f in props:
                self.fields.append(YamlObject.Field(f))
