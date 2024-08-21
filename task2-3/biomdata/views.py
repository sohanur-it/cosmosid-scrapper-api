from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Taxonomy
from .serializers import TaxonomySerializer
from rest_framework.response import Response
from rest_framework import status

class TaxonomyViewSet(viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        """
        Handles GET requests for retrieving a single taxonomy by its primary key.
        """
        try:
            taxonomy = self.get_queryset().get(pk=pk)
        except Taxonomy.DoesNotExist:
            return Response({"error": "Taxonomy not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(taxonomy)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Handles GET requests for retrieving all taxonomies.
        """
        paginator = self.paginate_queryset(self.get_queryset())
        if paginator is not None:
            serializer = self.get_serializer(paginator, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Handles POST requests for creating a new taxonomy.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Handles PUT requests for updating an existing taxonomy by its primary key.
        """
        try:
            taxonomy = self.get_queryset().get(pk=pk)
        except Taxonomy.DoesNotExist:
            return Response({"error": "Taxonomy not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(taxonomy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Handles DELETE requests for deleting a taxonomy by its primary key.
        """
        try:
            taxonomy = self.get_queryset().get(pk=pk)
        except Taxonomy.DoesNotExist:
            return Response({"error": "Taxonomy not found"}, status=status.HTTP_404_NOT_FOUND)
        
        taxonomy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
