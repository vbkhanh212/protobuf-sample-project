from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .ProtobufParser import ProtobufParser
from .ProtobufRenderer import ProtobufRenderer
from .proto import data_pb2 

def dict_to_proto(data):
    """Converts a standard Python dict to a Data Protobuf message."""
    proto_message = data_pb2.Data()
    for key, value in data.items():
        if key in proto_message.DESCRIPTOR.fields_by_name:
            setattr(proto_message, key, value)
    return proto_message
    
class DataView(APIView):
    parser_classes = [ProtobufParser, JSONParser] 
    renderer_classes = [ProtobufRenderer, JSONRenderer]

    def post(self, request):
        if isinstance(request.data, data_pb2.Data):
            received_message = request.data
            name = received_message.name
            age = received_message.age
            response_message = f"Protobuf received for client: {name}"
        else:
            name = request.data.get('name', 'Unknown')
            age = request.data.get('age', 'N/A')
            response_message = f"JSON received for user: {name}"

        if request.accepted_renderer.media_type == 'application/x-protobuf':
            response_proto_data = dict_to_proto({
                'name': name,
                'age': age,
            })
            return Response(response_proto_data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'success',
                'message': response_message,
            }, status=status.HTTP_200_OK)
        