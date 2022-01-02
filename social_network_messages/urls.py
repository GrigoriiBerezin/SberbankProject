from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'messages', views.MessageViewSet, basename="messages")
router.register(r'cities', views.CityViewSet, basename="cities")

urlpatterns = router.urls
