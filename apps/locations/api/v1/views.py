from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404


from apps.locations.api.v1.permissions import LocationPermission
from apps.locations.models import Location
from apps.locations.api.v1.serializers import LocationSerializer




class LocationView(APIView):
    permission_classes = [LocationPermission]

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Location created successfully."
                },
                status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class LocationDetailView(APIView):
    permission_classes = [LocationPermission]

    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location)

        return Response(serializer.data, status.HTTP_200_OK)


    def put(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Location updated successfully."
                },
                status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message":"Location updated successfully."
                },
                status.HTTP_200_OK
            )

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        location = get_object_or_404(Location, pk=pk)

        location.delete()

        return Response(
            {
                "message":"Location deleted successfully."
            },
            status.HTTP_200_OK
        )
        

