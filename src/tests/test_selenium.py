def test_selenium_foundable_process(selenium):
    urls = selenium.get_process_urls([
        "https://www2.tjal.jus.br/cpopg/open.do", 
        "https://www2.tjal.jus.br/cposg5/open.do"
        ], '0710802-55.2018.8.02.0001')

    assert len(urls) == 2

def test_selenium_not_foundable_process(selenium):
    urls = selenium.get_process_urls([
        "https://www2.tjal.jus.br/cpopg/open.do", 
        "https://www2.tjal.jus.br/cposg5/open.do"
        ], '0210802-55.2018.8.02.0001')

    assert len(urls) == 0