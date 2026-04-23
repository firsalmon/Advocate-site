from django.urls import path
from mainsite import views

app_name = "mainsite"
urlpatterns = [
    path(
        '',
        views.static_page,
        {
            'template_name': 'home', 
            'title': 'Адвокат Шайдоров М.С.',
            'description': 'desc'
        },
        name = 'home'
    ),
    
    path(
        'about/',
        views.static_page,
        {
            'template_name': 'about',
            'title': 'Об адвокате | Адвокат Шайдоров М.С.',
            'description': 'desc'
        },
        name='about'
    ),

    path(
        'service/',
        views.static_page,
        {
            'template_name': 'service', 
            'title': 'Услуги | Адвокат Шайдоров М.С.',
            'description': 'desc'
        },
        name='service'
    ),

    path(
        'sendform/',
        views.leadForm,
        name='sendform'
    ),
]