import pytest
from urllib.parse import quote
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_valuefilter(live_server, selenium):
    from demo.models import Artist
    artist_name = Artist.objects.all()[:1][0].name
    count = Artist.objects.filter(name=artist_name).count()
    assert Artist.objects.all().count() > count, "Too few Artists for ValueFilter test"  # Sanity check

    selenium.get(live_server.url)
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])

    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name_name__negate"]//input')
    input_.send_keys(artist_name)
    selenium.find_element(By.XPATH, '//*[@id="name_name__negate"]/h3').click()  # Simulate onblur()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name_name__negate"]//input')

    assert f'{count} artist' in selenium.page_source
    assert input_.get_attribute('value') == artist_name
    assert f'name={quote(artist_name)}' in selenium.current_url


@pytest.mark.selenium
def test_multivaluefilter(live_server, selenium):
    from demo.models import Country
    country_names = [country.name for country in Country.objects.all()[:2]]
    count = Country.objects.filter(name__in=country_names).count()
    assert Country.objects.all().count() > count, "Too few Countries for MultiValueFilter test"  # Sanity check

    selenium.get(live_server.url)
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])

    selenium.wait_for(By.LINK_TEXT, 'Countrys').click()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name__in"]//textarea')
    input_.send_keys(','.join(country_names))
    selenium.find_element(By.XPATH, '//*[@id="name__in"]//a').click()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name__in"]//textarea')

    assert f'{count} countrys' in selenium.page_source
    assert input_.get_attribute('value') == ','.join(country_names)
    assert f'name__in={",".join([quote(c) for c in country_names])}' in selenium.current_url


@pytest.mark.selenium
def test_multivaluefilter_exclude(live_server, selenium):
    from demo.models import Country
    country_names = [country.name for country in Country.objects.all()[:2]]
    count = Country.objects.filter(name__in=country_names).count()
    assert Country.objects.all().count() > count, "Too few Countries for MultiValueFilter test"  # Sanity check

    selenium.get(live_server.url)
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])

    selenium.wait_for(By.LINK_TEXT, 'Countrys').click()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name__in"]//textarea')
    input_.send_keys(','.join(country_names))
    selenium.find_element(By.XPATH, '//*[@id="name__in"]//input').click()
    selenium.find_element(By.XPATH, '//*[@id="name__in"]//a').click()
    textarea = selenium.wait_for(By.XPATH, '//*[@id="name__in"]//textarea')
    exclude = selenium.wait_for(By.XPATH, '//*[@id="name__in"]//input')

    from django.utils.http import urlencode
    assert f'{count} countrys' not in selenium.page_source
    assert textarea.get_attribute('value') == ','.join(country_names)
    assert exclude.get_attribute('value') == 'on'
    assert f'name__in={",".join([quote(c) for c in country_names])}' in selenium.current_url
    assert 'name__in__negate=true' in selenium.current_url
