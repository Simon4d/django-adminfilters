import pytest
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_valuefilter(live_server, selenium):
    from demo.models import Artist
    count = Artist.objects.filter(name="Angus").count()  # Sanity check

    selenium.get(live_server.url)
    dim = selenium.get_window_size()
    selenium.set_window_size(1100, dim['height'])

    selenium.wait_for(By.LINK_TEXT, 'Artists').click()
    assert f'{count} artist' not in selenium.page_source

    input_ = selenium.wait_for(By.XPATH, '//*[@id="name_name__negate"]//input')
    input_.send_keys('Angus')
    selenium.find_element(By.XPATH, '//*[@id="name_name__negate"]/h3').click()  # Simulate onblur()
    input_ = selenium.wait_for(By.XPATH, '//*[@id="name_name__negate"]//input')

    assert f'{count} artist' in selenium.page_source
    assert input_.get_attribute('value') == 'Angus'
    assert 'name=Angus' in selenium.current_url
