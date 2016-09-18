from django import template

# from webshop.forms import ParameterValueFormSet, ParameterOrderRangeFormSet
#
register = template.Library()


#
#
# @register.simple_tag(takes_context=True)
# def get_values_formset(context, code):
#     if context.get('{}_value_formset'.format(code)):
#         return context['{}_value_formset'.format(code)]
#     return ParameterValueFormSet(instance=context['parameter'], prefix=code)
#
#
# @register.simple_tag(takes_context=True)
# def get_ranges_formset(context, code):
#     if context.get('{}_range_formset'.format(code)):
#         return context['{}_range_formset'.format(code)]
#     return ParameterOrderRangeFormSet(instance=context['parameter'], prefix=code)


@register.filter
def inline(data):
    return data.replace('\r', '').replace('\n', '').replace('"', "'").strip()
