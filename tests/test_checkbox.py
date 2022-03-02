from functools import partial
from unittest.mock import Mock

import pytest

from demo.models import Band
from adminfilters.checkbox import ChoicesCheckboxFilter
from adminfilters.utils import get_query_string


@pytest.fixture
def fixtures(db):
    from demo.factories import BandFactory
    BandFactory(name='RockBand', genre=1)
    BandFactory(name='BluesBand', genre=2)
    BandFactory(name='SoulBand', genre=3)
    BandFactory(name='OtherBand', genre=4)
    BandFactory(name='NoneBand', genre=None)


@pytest.mark.parametrize('filter_value,expected', [({}, ['BluesBand', 'NoneBand', 'OtherBand', 'RockBand', 'SoulBand']),
                                                   ({'genre__in': '1'}, ['RockBand']),
                                                   ({'genre__in': '1,2'}, ['BluesBand', 'RockBand']),
                                                   ({'genre__in': '1,2', 'genre__isnull': '1'}, ['BluesBand', 'NoneBand', 'RockBand']),
                                                   ({'genre__isnull': '1'}, ['NoneBand']),
                                                   ])
def test_queryset(fixtures, filter_value, expected):
    f = ChoicesCheckboxFilter(Band._meta.get_field('genre'), None, filter_value, None, None, 'genre')
    result = f.queryset(None, Band.objects.order_by('name'))
    value = list(result.order_by('name').values_list('name', flat=True))
    assert value == expected


def test_choices(fixtures):
    params = {'genre__in': '1,2'}
    f = ChoicesCheckboxFilter(Band._meta.get_field('genre'), None, params, None, None, 'genre')
    cl = Mock(get_query_string=partial(get_query_string, Mock(GET=params)), params=params)
    choices = list(f.choices(cl))
    assert len(choices) == 6
    assert choices[0] == {'display': 'All', 'query_string': '?', 'selected': False, 'to_remove': 'genre__in&genre__isnull'}
    assert choices[1] == {'display': 'None', 'query_string': '?genre__isnull=1', 'selected': False, 'to_remove': 'genre__in'}
    assert choices[2] == {'display': 'Rock', 'query_string': '?genre__in=2', 'selected': True, 'to_remove': 'genre__isnull'}
    assert choices[3] == {'display': 'Blues', 'query_string': '?genre__in=1', 'selected': True, 'to_remove': 'genre__isnull'}
    assert choices[4] == {'display': 'Soul', 'query_string': '?genre__in=1%2C2%2C3', 'selected': False, 'to_remove': 'genre__isnull'}
    assert choices[5] == {'display': 'Other', 'query_string': '?genre__in=1%2C2%2C4', 'selected': False, 'to_remove': 'genre__isnull'}
