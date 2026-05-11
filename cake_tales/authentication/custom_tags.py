from django.template import Library

register = Library()

@register.simple_tag
def square_num(num):

    return num**2

@register.simple_tag
def allowed_roles(request,roles):

    roles = eval(roles)

    return request.user and request.user.is_authenticated and request.user.role in roles 