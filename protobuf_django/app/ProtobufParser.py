from rest_framework.parsers import BaseParser
from rest_framework.exceptions import ParseError
from .proto import data_pb2 

class ProtobufParser(BaseParser):
    media_type = 'application/x-protobuf'

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            message = data_pb2.Data()
            
            data = stream.read()
            
            message.ParseFromString(data)
            
            return message
            
        except Exception as exc:
            raise ParseError(f'Protobuf parse error: {exc}')
