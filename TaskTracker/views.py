from django.http import HttpResponseNotFound


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found 404</h1> <a href='/'>На главную страницу</a>")