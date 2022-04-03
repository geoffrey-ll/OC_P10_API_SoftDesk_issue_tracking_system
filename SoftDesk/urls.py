"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
# from rest_framework import routers
from rest_framework_nested import routers


from projects.views import ContributorViewSet, ProjectViewSet


router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("projects/(?P<project_id>[^/.]+)/users", ContributorViewSet,
                basename="contributors")

# projects_router = routers.NestedSimpleRouter(router, "projects",
#                                              lookup="projects")
# projects_router.register("user", ContributorViewSet, basename="contributor")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
