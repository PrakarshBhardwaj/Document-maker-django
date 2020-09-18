from rest_framework import serializers
from main.models import Document, Section, Subsection, Para, Img

class DocumentSerializer(serializers.ModelSerializer):
    # sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ("id", "document_name", "document_author", "Creation_date")

    # def create(self, validated_data):


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ("Section_id", "Section_Heading", "document")


class ParaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Para
        fields = ("__all__")


class SubsectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subsection
        # fields = ("Subsection_id", "Subsection_heading", "Section")
        fields = ("__all__")


class ImgSerializer(serializers.ModelSerializer):

    class Meta:
        model = Img
        fields = ("__all__")

