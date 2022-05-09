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
from rest_framework_nested import routers


from projects.views import ContributorViewSet, CommentViewSet, IssueViewSet, \
    ProjectViewSet


router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")


projects_router = routers.NestedSimpleRouter(router, "projects",
                                             lookup="project")
projects_router.register("users", ContributorViewSet, basename="contributors")
projects_router.register("issues", IssueViewSet, basename="issues")


issues_router = routers.NestedSimpleRouter(projects_router, "issues",
                                           lookup="issue")
issues_router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("api/", include(projects_router.urls)),
    path("api/", include(issues_router.urls)),
]
