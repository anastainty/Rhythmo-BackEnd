from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

class SendMessageAPIView(APIView):
    def post(self, request):
        message = request.data.get('message', None)
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        channel_layer = get_channel_layer()
        try:
            async_to_sync(channel_layer.group_send)(
                'chat_room',
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
            return Response({"message": "Message sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)