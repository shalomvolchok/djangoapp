from django.core.urlresolvers import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.utils.safestring import mark_safe
 
def add_link_field(target_model=None, field='', app='', field_name='link',
                   link_text=unicode, short_description=None):
    """
    decorator that automatically links to a model instance in the admin;
    inspired by http://stackoverflow.com/questions/9919780/how-do-i-add-a-link-from-the-django-admin-page-of-one-object-
    to-the-admin-page-o
    :param target_model: modelname.lower or model
    :param field: fieldname
    :param app: appname
    :param field_name: resulting field name
    :param link_text: callback to link text function
    :param short_description: list header
    :return:
    """
    import logging
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
 
        def link(self, instance):
            app_name = app or instance._meta.app_label

            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
 
            # manyrelatedmanager with one result?
            if link_obj.__class__.__name__ == "RelatedManager":
                try:
                    link_obj = link_obj.get()
                except MultipleObjectsReturned:
                    return u"multiple, can't link"
                except link_obj.model.DoesNotExist:
                    return u""
            logging.debug(instance.id)
            url = reverse(reverse_path, args = (link_obj.id,))
            return mark_safe(u"<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = short_description or (reverse_name + ' link')
        setattr(cls, field_name, link)
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + \
            [field_name]
        return cls
    return add_link