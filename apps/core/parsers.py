import json
from django.http import QueryDict
from rest_framework.parsers import MultiPartParser, DataAndFiles


class MultipartJsonParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if not isinstance(value, str):
                data[key] = value
                continue
            if '{' in value or '[' in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        qdict = QueryDict('', mutable=True)
        qdict.update(data)

        return DataAndFiles(qdict, result.files)
