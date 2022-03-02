import pytest
from demo.models import Band
from adminfilters.checkbox import ChoicesCheckboxFilter


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
