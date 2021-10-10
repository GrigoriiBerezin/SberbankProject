from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename="messages")

urlpatterns = router.urls
