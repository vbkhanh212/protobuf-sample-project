from rest_framework.renderers import BaseRenderer

class ProtobufRenderer(BaseRenderer):
    media_type = 'application/x-protobuf'
    format = 'protobuf'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
            
        return data.SerializeToString()
    