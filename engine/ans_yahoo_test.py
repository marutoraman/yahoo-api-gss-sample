from engine.yahoo import YahooAPI

def test_yahoo():
    res = YahooAPI.fetch_item("5702017035949")
    print(res.__dict__)

    assert res.name