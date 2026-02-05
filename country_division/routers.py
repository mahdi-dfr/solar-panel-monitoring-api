from rest_framework.routers import DefaultRouter

from country_division.views import ProvinceViewSet, CityViewSet, CountyViewSet, DistrictViewSet, VillageViewSet

router = DefaultRouter()
router.register('province', ProvinceViewSet, basename='province')
router.register('city', CityViewSet, basename='city')
router.register('county', CountyViewSet, basename='county')
router.register('district', DistrictViewSet, basename='district')
router.register('village', VillageViewSet, basename='village')

urlpatterns = [] + router.urls
