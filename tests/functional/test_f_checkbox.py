import pytest
from demo.utils import ChangeListWrapper, Checkbox
from selenium.webdriver.common.by import By


def get_elements(selenium):
    container = selenium.find_element(By.ID, 'field-genre')
    return [container,
            ChangeListWrapper.find_in_page(selenium)]


@pytest.mark.selenium
def test_checkbox_simple_filter(admin_site_band):
    container, cl = get_elements(admin_site_band.driver)
    rock = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "Rock")]]'))
    rock.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'Rock'}


@pytest.mark.selenium
def test_checkbox_complex_filter(admin_site_band):
    container, cl = get_elements(admin_site_band.driver)
    rock = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "Rock")]]'))
    rock.check()
    container, cl = get_elements(admin_site_band.driver)
    blues = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "Blues")]]'))
    blues.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'Rock', 'Blues'}


@pytest.mark.selenium
def test_checkbox_none_filter(admin_site_band):
    from demo.factories import BandFactory
    BandFactory(name='NoneBand', genre=None)

    container, cl = get_elements(admin_site_band.driver)
    rock = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "Rock")]]'))
    rock.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'Rock'}
    container, cl = get_elements(admin_site_band.driver)
    none = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "None")]]'))
    none.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'-'}


@pytest.mark.selenium
def test_checkbox_all_filter(admin_site_band):
    container, cl = get_elements(admin_site_band.driver)
    rock = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "Rock")]]'))
    rock.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'Rock'}
    container, cl = get_elements(admin_site_band.driver)
    none = Checkbox(container.find_element(By.XPATH, '//label[text()[contains(., "All")]]'))
    none.check()
    container, cl = get_elements(admin_site_band.driver)
    assert set(cl.get_values(col=2)) == {'Rock', 'Blues', 'Soul', 'Other'}
