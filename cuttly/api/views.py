from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


from .serializers import *
from .tasks import call_task


class UserCreationView(GenericAPIView):
    """
        View for creating users.
    """

    serializer_class = UserCreateSerializer

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=201)
        return Response({"ERR_CODE": "BODY_NOT_VALID", "info": "Body is not full or invalid"}, status=400)


class URLView(viewsets.ViewSet, GenericAPIView):
    """
        URL view for interaction with urls

            GET: get info about single url
            POST: create url
            PATCH: update url (change original url), can do only owner of url
            DELETE: delete url, can do only owner of url
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = URLSerializer

    def post(self, request):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.validated_data['creator'] = user.id
            call_task(serializer.validated_data)
            return Response("Cutted URL you will receive on your email", status=201)
        return Response({"ERR_CODE": "BODY_NOT_VALID", "info": "Body is not full or invalid"}, status=400)

    def get(self, request, id):
        user = request.user
        url = URL.objects.filter(id=id).first()
        if url is None:
            return Response({"ERR_CODE": "NOT_FOUND", "info": "URL with given id does not exists"}, status=404)
        serializer = self.serializer_class(url)
        return JsonResponse(serializer.data, status=200)

    def patch(self, request, id):
        user = request.user
        data = request.data
        url = URL.objects.filter(id=id).first()
        if url is None:
            return Response({"ERR_CODE": "NOT_FOUND", "info": "URL with given id does not exists"}, status=404)
        if not user.is_owner(id):
            return Response({"ERR_CODE": "NOT_OWNER", "info": "Permission denied."
                                                              " You're not owner of this url."},
                            status=403)
        serializer = self.serializer_class(url, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return Response({"ERR_CODE": "BODY_NOT_VALID", "info": "Body is not full or invalid"}, status=400)

    def delete(self, request, id):
        user = request.user
        url = URL.objects.filter(id=id).first()
        if url is None:
            return Response({"ERR_CODE": "NOT_FOUND", "info": "URL with given id does not exists"}, status=404)
        if not user.is_owner(id):
            return Response({"ERR_CODE": "NOT_OWNER", "info": "Permission denied."
                                                              " You're not owner of this url."},
                            status=403)
        url.delete()
        return Response({"status": f"deleted {id}"}, status=200)


class MyURLsView(GenericAPIView):
    """
        My URLs view for getting all urls created by user

            GET: get info about all urls that user created
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = URLSerializer

    def get(self, request):
        user = request.user
        urls = URL.objects.filter(creator=user)
        serializer = self.serializer_class(urls, many=True)
        return JsonResponse(serializer.data, safe=False)


class CuttedView(GenericAPIView):
    """
        View for redirecting cutted url to it`s original.
    """

    def get(self, request, id):
        url = URL.objects.filter(id=id).first()
        if url is None:
            return Response({"ERR_CODE": "NOT_FOUND", "info": "URL does not exists"}, status=404)
        return HttpResponseRedirect(redirect_to=url.original_url)
