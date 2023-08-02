from django import template

register = template.Library()


@register.filter(name='placeholder')
def placeholder(value, token):
    value.field.widget.attrs['placeholder'] = token
    return value
@register.filter(name='custom_class')
def form_field_class(form_field,className):
    form_field.field.widget.attrs['class']=className
    return form_field
