from django.shortcuts import render


def page_not_found(request, exception):
    """Display custom page if page not found."""
    return render(
        request,
        'misc/404.html',
        {
            'path': request.path,
            'exception': exception,
        },
        status=404
    )
