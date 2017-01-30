from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, 'api-categories')

urlpatterns = router.urls