from django.template import Library

register = Library()

@register.filter(name='add_class')
def add_class(field, class_attr):
    return field.as_widget(attrs={'class': class_attr})
