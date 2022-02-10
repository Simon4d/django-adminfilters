import json

from django import forms
from django.conf import settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.utils.translation import get_language

from adminfilters.mixin import MediaDefinitionFilter, SmartFieldListFilter


class ValueFilter(MediaDefinitionFilter, SmartFieldListFilter):
    template = 'adminfilters/value.html'
    toggleable = False
    filter_title = None
    lookup_name = 'exact'
    #
    button = True
    can_negate = True
    negated = False

    # path_separator = '-'
    # arg_separator = '|'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_negated_val = None
        self.model = model
        self.lookup_val = None
        self.lookup_kwarg = '%s__%s' % (field_path, self.lookup_name)
        self.lookup_kwarg_negated = '%s__negate' % self.lookup_kwarg
        self.parse_query_string(params)
        self.field_path = field_path
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = self._get_title()
        self.params = params
        self.query_values = []
        self.operator = '+'

    def js_options(self):
        return json.dumps(dict(button=self.button,
                               canNegate=self.can_negate,
                               negated=self.negated))

    def _get_title(self):
        if self.filter_title:
            return self.filter_title
        elif '__' in self.field_path:
            return self.field_path.replace('__', '->')
        return getattr(self.field, 'verbose_name', self.field_path)

    @classmethod
    def factory(cls, *, title=None, lookup_name='exact', **kwargs):
        kwargs['filter_title'] = title
        kwargs['lookup_name'] = lookup_name
        return type('ValueFilter', (cls,), kwargs)

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_negated]

    def value(self):
        return [
            self.lookup_val,
            self.lookup_negated_val == 'true'
        ]

    def parse_query_string(self, params):
        self.lookup_negated_val = params.get(self.lookup_kwarg_negated)
        self.lookup_val = params.get(self.lookup_kwarg, '')

    def queryset(self, request, queryset):
        target, exclude = self.value()
        if target:
            filters = {self.lookup_kwarg: target}
            if exclude:
                return queryset.exclude(**filters)
            else:
                return queryset.filter(**filters)
        return queryset

    def choices(self, changelist):
        self.query_string = changelist.get_query_string(remove=self.expected_parameters())
        return []

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = ('admin/js/vendor/select2/i18n/%s.js' % i18n_name,) if i18n_name else ()
        return forms.Media(
            js=('admin/js/vendor/jquery/jquery%s.js' % extra,
                ) + i18n_file + ('admin/js/jquery.init.js',
                                 'adminfilters/value%s.js' % extra,
                                 ),
            css={
                'screen': (
                    'admin/css/vendor/select2/select2%s.css' % extra,
                    'adminfilters/adminfilters.css',
                ),
            },
        )


class MultiValueFilter(ValueFilter):
    template = 'adminfilters/value_multi.html'
    separator = ','
    filter_title = None
    lookup_name = 'in'

    def parse_query_string(self, params):
        raw_values = params.get(self.lookup_kwarg, '').split(self.separator)
        self.lookup_negated_val = params.get(self.lookup_kwarg_negated)
        self.lookup_val = [e.strip() for e in raw_values if e.strip()]


TextFieldFilter = ValueFilter
ForeignKeyFieldFilter = TextFieldFilter
MultiValueTextFieldFilter = MultiValueFilter