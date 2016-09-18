from django import template

register = template.Library()


def get_parameters(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "get_parameters tag takes at least 1 argument")
    if len(args) > 2:
        return GetParametersNode(args[1].strip(), args[2].strip())
    return GetParametersNode(args[1].strip())


def del_parameters(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "get_parameters tag takes at least 1 argument")
    return DelParametersNode(args[1].strip())


class GetParametersNode(template.Node):
    def __init__(self, field, value=None):
        if value:
            self.field = template.Variable(field)
            self.value = template.Variable(value)
        else:
            self.field = field
            self.value = value

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()

        if self.value:
            field = str(self.field.resolve(context))
            value = str(self.value.resolve(context))
        else:
            field = self.field
            value = self.value
        if field in getvars:
            if value:
                getvars.setlist(field, [v for v in getvars.getlist(field) if v != value])
                if len(getvars[field]) < 1:
                    del getvars[field]
            else:
                del getvars[field]

        if len(getvars.keys()) > 0:
            if self.value:
                get_params = "%s" % getvars.urlencode()
            else:
                get_params = "%s&" % getvars.urlencode()
        else:
            get_params = ''

        return get_params


class DelParametersNode(template.Node):
    def __init__(self, fields):
        self.fields = template.Variable(fields)

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()

        fields = tuple(set([i['product_parameter'] for i in self.fields.resolve(context)]))
        for field in fields:
            if str(field) in getvars:
                del getvars[str(field)]

        if len(getvars.keys()) > 0:
            get_params = "%s" % getvars.urlencode()
        else:
            get_params = ''

        return get_params


get_parameters = register.tag(get_parameters)
del_parameters = register.tag(del_parameters)
