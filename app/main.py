import os
import waitress
from flask import Flask, render_template, request
from app.tariff import Tariff, TariffManager


def start():
    app = Flask(__name__)

    manager = TariffManager()

    my_online = Tariff('Мой Онлайн', price=290, hit=True, gb=15, gb_unlim=['vk', 'fb', 'ok', 'wapp', 'vb', 'tam', 'inst'], minutes=400)
    unlim = Tariff('Безлимит', price=350, gb=-1, minutes=500, sms=50)
    classic = Tariff('Классический', price=0, minutes_unlim_tele2=False)

    black = Tariff('Беспредельно черный', price=310, gb=30, minutes=200, minutes_unlim_tele2=False, sms=200, archived=True)
    city = Tariff('Сити', minutes_unlim_tele2=False, archived=True)

    manager.add(my_online)
    manager.add(unlim)
    manager.add(classic)

    manager.add(black)
    manager.add(city)

    @app.route('/')
    def index():
        return list_tariffs('actual')

    @app.route('/archived')
    def archived():
        return list_tariffs('archived')

    def list_tariffs(status):
        method = getattr(manager, status);
        tariffs = method()

        period_ru = {
            'month': 'месяц',
            'day': 'день',
            'minute': 'минута'
        }

        return render_template('index.html', tariffs=tariffs, status=status, period_ru=period_ru)

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()
