from .models import Document, Section, Subsection, Para, Img
from .serializers import DocumentSerializer, SectionSerializer, SubsectionSerializer, ParaSerializer, ImgSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import get_storage_class
import json

# instance of the current storage class
media_storage = get_storage_class()()


def jsondata(doc):
	document_dict = {}

	document_dict["Document_name"] = doc.document_name
	document_dict["Athour_name"] = doc.document_author
	document_dict["Section"] = []

	for section in Section.objects.filter(document=doc):
		section_dict = {}

		section_dict["section_heading"] = section.Section_Heading
		section_dict["section_content"] = []

		for subsection in Subsection.objects.filter(Section=section):
			subsection_dict = {}

			subsection_dict["Sub_section_heading"] = subsection.Subsection_heading
			subsection_dict["Sub_section_sequence"] = subsection.Subsection_sequence
			subsection_dict["Sub_section_content"] = []
			subsection_content_dict = {}
			subsection_content_dict["Paragraph"] = []
			subsection_content_dict["Image"] = []

			for para in Para.objects.filter(Subsection=subsection).order_by("para_number"):
				para_dict = {}
				para_dict["para_heading"] = para.Para_heading
				para_dict["para_content"] = para.Para_content

				subsection_content_dict["Paragraph"].append(para_dict)

			for img in Img.objects.filter(Subsection=subsection).order_by("img_number"):
				img_dict = {}
				img_dict["img_heading"] = img.Img_heading
				img_dict["img_path"] = img.Img_Data.url

				subsection_content_dict["Image"].append(img_dict)
			
			subsection_dict["Sub_section_content"].append(subsection_content_dict)
			section_dict["section_content"].append(subsection_dict)

		document_dict["Section"].append(section_dict)

	return document_dict

class DocumentViewSet(viewsets.ModelViewSet):
	serializer_class = DocumentSerializer
	queryset = Document.objects.all()
	lookup_field = "id"

	@action(detail=True, methods=["GET"])
	def edit(self, request, id=None, *args, **kwargs):
		doc = self.get_object()
		doc_data = jsondata(doc)
		return Response(doc_data, status=200)
	

class SectionViewSet(viewsets.ModelViewSet):
	serializer_class = SectionSerializer
	queryset = Section.objects.all()
	lookup_field = "Section_id"
	
	def get_queryset(self):
		return Section.objects.filter(document=self.kwargs['document_id'])

	def create(self, request, *args, **kwargs):
		request.data['document'] = self.kwargs['document_id']
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=201, headers=headers)

	# def perform_create(self, serializer):
	# 	print("We in yo!")
	# 	current_doc = Document.objects.get(id=self.kwargs['document_id'])
	# 	serializer.save(document=current_doc)

class SubsectionViewSet(viewsets.ModelViewSet):
	serializer_class = SubsectionSerializer
	queryset = Subsection.objects.all()
	lookup_field = "Subsection_id"

	def get_queryset(self):
		return Subsection.objects.filter(Section=self.kwargs['section_Section_id'])

	def create(self, request, *args, **kwargs):
		request.data['Section'] = self.kwargs['section_Section_id']
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=201, headers=headers)

	# @action(detail=True, methods=["POST"])
	# def copy_para(self, request, *args, **kwargs):
	# 	# data = request.data
	# 	print(request.data)
	# 	para = Para.objects.get(Para_id=request.data["Para_id"])
	# 	serializer = ParaSerializer(para)
	# 	copy_para_data = serializer.data
	# 	copy_para_data["Subsection"] = self.kwargs['Subsection_id']
	# 	copy_para_data["Para_id"] = None
	# 	copy_serializer = ParaSerializer(data=copy_para_data)
	# 	if copy_serializer.is_valid():
	# 		copy_serializer.save()
	# 		return Response(copy_serializer.data, status=201)
	# 	else:
	# 		return Response(copy_serializer.errors, status=400)


class ParaViewSet(viewsets.ModelViewSet):
	serializer_class = ParaSerializer
	queryset = Para.objects.all()
	lookup_field = "Para_id"

	def get_queryset(self):
		return Para.objects.filter(Subsection=self.kwargs['subsection_Subsection_id'])

	def create(self, request, *args, **kwargs):
		request.data['Subsection'] = self.kwargs['subsection_Subsection_id']
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=201, headers=headers)
	
	@action(detail=True, methods=["GET"])
	def copy(self, request, Para_id, *args, **kwargs):
		para = Para.objects.get(Para_id=Para_id)
		serializer = ParaSerializer(para)
		return Response(serializer.data)

	# def update(self, request, *args, **kwargs): # HOW TO USE PATCH instead of PUT
	# 	request.data['Subsection'] = self.kwargs['subsection_Subsection_id']

	
class ImgViewSet(viewsets.ModelViewSet):
	serializer_class = ImgSerializer
	queryset = Img.objects.all()
	lookup_field = "Img_id"

	def get_queryset(self):
		return Img.objects.filter(Subsection=self.kwargs['subsection_Subsection_id'])

	def create(self, request, *args, **kwargs):
		request.data['Subsection'] = self.kwargs['subsection_Subsection_id']
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=201, headers=headers)

