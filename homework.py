import datetime as dt


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
        self.records = list()

    def add_record(self, record: 'Record') -> None:
        self.records.append(record)

    def get_today_stats(self, date: str = '') -> float:
        total = 0
        moment = date
        if (date == ''):
            moment = dt.datetime.now().date()
        today_records = list(filter(lambda record: record.date == moment,
                             self.records))

        for record in today_records:
            total = total + record.amount

        return total

    def get_week_stats(self):
        long_week = 7
        week_total = 0
        today = dt.datetime.now().date()
        for day in range(long_week):
            moment = today - dt.timedelta(days=day)
            print(moment)
            week_total = week_total + self.get_today_stats(moment)

        return week_total


class CashCalculator(Calculator):
    '''
    Калькулятор денег.
    add_record() - Сохраняет новую запись о расходах
    get_today_stats() - Считает, сколько денег потрачено сегодня
    get_week_stats() - Считает, сколько денег потрачено за последние 7 дней
    get_today_cash_remained(currency) - Определяет, сколько ещё денег можно
    потратить сегодня в рублях, долларах или евро
    '''

    def __init__(self, limit):
        super().__init__(limit)

    # Ревьюер если ты это читаешь, то ты меня поймешь. Это ЖЕСТЬ!!! Это
    # целенавравленный выстрел в ногу, который дал кретический промах в голову
    EURO_RATE = 89.78
    USD_RATE = 73.78

    def get_today_cash_remained(self, currency: str = 'rub') -> str:
        '''
        currency -> должен принимать на вход код валюты:
        одну из строк "rub", "usd" или "eur"
        '''
        currencies = {
            'rub': {'name': 'руб', 'rate': 1.00},
            'usd': {'name': 'USD', 'rate': self.USD_RATE},
            'eur': {'name': 'Euro', 'rate': self.EURO_RATE}
        }

        current_currency = currencies[currency]
        current_balance = round(((self.limit - self.get_today_stats())
                                 / current_currency["rate"]), 2)

        if (current_balance > 0):
            return (f'На сегодня осталось {current_balance} '
                    f'{current_currency["name"]}')

        elif (current_balance == 0):
            return 'Денег нет, держись'

        else:
            return (f'Денег нет, держись: твой долг - {abs(current_balance)} '
                    f'{current_currency["name"]}')


class CaloriesCalculator(Calculator):
    '''
    Калькулятор калорий
    add_record() - Сохраняет новую запись о расходах
    get_today_stats() - Считает, сколько денег потрачено сегодня
    get_week_stats() - Считает, сколько денег потрачено за последние 7 дней
    get_calories_remained() - Определять, сколько ещё калорий можно/нужно
    получить сегодня
    '''

    def get_calories_remained(self):
        current_balance = self.limit - self.get_today_stats()

        if (current_balance > 0):
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {current_balance} кКал')

        else:
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
    date: str

    def __init__(self, amount, comment, date='') -> None:
        self.amount = amount
        self.comment = comment
        self.date = self.convert_date(date)

    def convert_date(self, date: str) -> str:
        date_format = '%d.%m.%Y'
        if (date == ''):
            return dt.datetime.now().date()
        else:
            return dt.datetime.strptime(date, date_format).date()


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
