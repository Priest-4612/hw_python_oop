import datetime as dt
from typing import Union


class Calculator:
    '''
    Калькулятор.
    add_record() - Сохраняет новую запись о расходах
    get_today_stats() - Считает, сколько денег потрачено сегодня
    get_week_stats() - Считает, сколько денег потрачено за последние 7 дней
    '''
    limit: float

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: 'Record') -> None:
        '''Сохраняет новую запись о расходах
        record -> принимает экземпляр класса Record
        '''
        self.records.append(record)

    def get_today_stats(self, date: Union[str, dt.date] = '') -> float:
        '''Рассчитывает, сколько денег потрачено за указанную дату
        date -> принимает дату в формате "str" или "dt.date"
        '''
        moment = date

        if date == '':
            moment = dt.date.today()

        return sum([rec.amount for rec in self.records if rec.date == moment])

    def get_balance_today(self) -> float:
        '''Рассчитывает остаток на сегодня'''
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        '''Рассчитывает расходы за неделю'''
        long_week = 7
        week_total = 0
        today = dt.datetime.today()

        for day in range(long_week):
            moment = today - dt.timedelta(days=day)
            week_total = week_total + self.get_today_stats(moment.date())

        return week_total


class CashCalculator(Calculator):
    '''
    Калькулятор денег.
    get_today_cash_remained(currency) - Рассчитывает, сколько ещё денег можно
    потратить сегодня в рублях, долларах или евро
    '''

    EURO_RATE: float = 89.78
    USD_RATE: float = 73.78

    def get_today_cash_remained(self, currency: str = 'rub') -> str:
        '''
        currency -> должен принимать на вход код валюты:
        одну из строк "rub", "usd" или "eur"
        '''
        currencies = {
            'rub': ['руб', 1.00],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]
        }

        if currency not in currencies.keys():
            return f'Мне неизвестна данная валюта {currency}'

        cur_name, cur_rate = currencies[currency]

        current_balance = round(self.get_balance_today() / cur_rate, 2)

        if current_balance > 0 :
            return (f'На сегодня осталось {current_balance} '
                    f'{cur_name}')

        if current_balance == 0 :
            return 'Денег нет, держись'

        return (f'Денег нет, держись: твой долг - {abs(current_balance)} '
                f'{cur_name}')


class CaloriesCalculator(Calculator):
    '''
    Калькулятор калорий
    get_calories_remained() - Рассчитывает, сколько ещё калорий можно/нужно
    получить сегодня
    '''

    def get_calories_remained(self):
        current_balance = self.get_balance_today()

        if (current_balance > 0):
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {current_balance} кКал')

        return 'Хватит есть!'


class Record:
    '''
    Класс для создания записей.
    amount -> число (денежная сумма или количество килокалорий);
    date -> дата создания записи (передаётся в явном виде в конструктор, либо
    присваивается значение по умолчанию — текущая дата);
    comment -> комментарий, поясняющий, на что потрачены деньги или откуда
    взялись калории;
    '''
    amount: float
    comment: str
    date: Union[str, dt.datetime]

    def __init__(self, amount, comment, date: Union[str, dt.datetime] ='') -> None:
        self.amount = amount
        self.comment = comment
        self.date = self.convert_date(date)

    def convert_date(self, date: Union[str, dt.date]) -> dt.date:
        if date == '' :
            return dt.date.today()

        date_format = '%d.%m.%Y'
        return dt.datetime.strptime(date, date_format).date()

if __name__ == '__main__':

    cash_calculator = CashCalculator(1000)
    # дата в параметрах не указана,
    # так что по умолчанию к записи
    # должна автоматически добавиться сегодняшняя дата
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(Record(amount=3000,
                                    comment='бар в Танин др',
                                    date='08.11.2019'))

    print(cash_calculator.get_today_cash_remained('rub'))
    print(cash_calculator.get_today_cash_remained('eur'))
    print(cash_calculator.get_today_cash_remained('usd'))
    print(cash_calculator.get_today_cash_remained('tug'))
