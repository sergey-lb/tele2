from app.tariff import Tariff, TariffManager


def test_create_tariff():

    name = 'Мой Онлайн'
    data = {
        'price': 10,
        'price_period': 'day',
        'gb': 100,
        'minutes': 1000,
        'sms': 10000,
        'hit': False,
        'gb_unlim': ['vk', 'fb', 'ok', 'wapp', 'vb', 'tam', 'inst'],
        'minutes_unlim_tele2': False,
        'archived': True
    }

    tariff = Tariff(
        name,
        **data
    )

    assert tariff.name == name
    for key,val in data.items():
        assert getattr(tariff, key) == val


def test_tariff_manager():
    manager = TariffManager()

    my_online = Tariff('Мой Онлайн', price=290, hit=True, gb=15,
                       gb_unlim=['vk', 'fb', 'ok', 'wapp', 'vb', 'tam', 'inst'], minutes=400)
    unlim = Tariff('Безлимит', price=350, gb=-1, minutes=500, sms=50)
    classic = Tariff('Классический', price=0, minutes_unlim_tele2=False)

    black = Tariff('Беспредельно черный', price=310, gb=30, minutes=200, minutes_unlim_tele2=False, sms=200,
                   archived=True)
    city = Tariff('Сити', minutes_unlim_tele2=False, archived=True)

    expected_actual = [my_online, unlim, classic]
    expected_archived = [black, city]

    manager.add(my_online)
    manager.add(unlim)
    manager.add(classic)

    manager.add(black)
    manager.add(city)

    actual = manager.actual()
    archived = manager.archived()

    assert actual == expected_actual
    assert archived == expected_archived
