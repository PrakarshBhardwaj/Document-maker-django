"""adoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_nested import routers
from . import views

router = routers.SimpleRouter()
router.register(r'documents', views.DocumentViewSet)

section_router = routers.NestedSimpleRouter(router, r'documents', lookup='document')
section_router.register(r'sections', views.SectionViewSet, basename="sections")

subsection_router = routers.NestedSimpleRouter(section_router, r"sections", lookup="section")
subsection_router.register(r'subsections', views.SubsectionViewSet, basename="subsections")

para_router = routers.NestedSimpleRouter(subsection_router, r"subsections", lookup="subsection")
para_router.register(r'paragraphs', views.ParaViewSet, basename="para")

images_router = routers.NestedSimpleRouter(subsection_router, r"subsections", lookup="subsection")
images_router.register(r'images', views.ImgViewSet, basename="images")


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(section_router.urls)),
    path(r'', include(subsection_router.urls)),
    path(r'', include(para_router.urls)),
    path(r'', include(images_router.urls)),
]
