from django.urls import path
from .views import home_page, category_page, test_page, question_page, test_results


urlpatterns = [
    path('', home_page, name='home'),
    path('<int:cat_id>/', category_page, name='category'),
    path('<int:cat_id>/<int:test_id>/', test_page, name='test_page'),
    path('<int:cat_id>/<int:test_id>/<int:quest_id>/', question_page, name='question_page'),
    path('<int:cat_id>/<int:test_id>/results/', test_results, name='test_results')
]
