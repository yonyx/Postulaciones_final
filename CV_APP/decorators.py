from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def administrador_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_administrador,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def coordinacion_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_coordinacion or u.is_coordinacion2,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def rector_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_rector,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def psicologa_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_psicologa,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def monica_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_monica,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator