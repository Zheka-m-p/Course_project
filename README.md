# Курсовой проект. Разработка на Python

# Технический анализ данных при помощи алгоритмов

> В проекте реализованы алгоритмы поиска, сортировки и кэширования для работы с большим объемом данных (архив за 5 лет) по котировкам акция компаний из S&P 500.
> 

- Для считывания данных используется библиотека `pandas`.
- Для сортировки котировок, тикеров компаний и дат используется метод быстрой сортировки *Quick Sort*.
- Поиск запрашиваемых клиентом данных ведется на отсортированных данных через алгоритм бинарного поиска.
- Реализован механизм кэширования для экономии вычислительного ресурса, если запрос от пользователя повторяется.

Проект оформлен в виде poetry-пакета со скриптами, позволяющими пользователю получать сортированную выборку данных и осуществлять поиск данных.

## Реализация

<aside>
💡 Не забывайте практиковаться в работе из командной строки.

</aside>

Создайте с помощью `poetry` пакет для проекта.

Инициализируйте git репозиторий.  

<aside>
💡 Не забывайте делать частые комиты с осмысленными названиями.

</aside>

Добавьте в *pyproject.toml* в раздел `[tool.poetry.scripts]` точки входа

- `get-sorted`
- `get-banch`

> Про добавление скриптов [тут](https://www.notion.so/2fcd1584f4224f6582a9220f9d112bbe?pvs=21).
> 

Взаимодействие с пользователем ведется интерактивно через командную строку. По результату взаимодействия определяются входные параметры для соответствующих функций. Запуск из командной строки и результаты приведены ниже:

```bash
~$ poetry run get-sorted
Сортировать по цене 
открытия (1)
закрытия (2)
максимум [3]
минимум (4)
объем (5)

Порядок по убыванию [1] / возрастанию (2): 1
Ограничение выборки [10]: 50
Название файла для сохранения результата [dump.csv]: result.csv
```

При запросе данных пользователю отображаются опции. В `[]` скобках указано значение, которое будет использоваться по-умолчанию, если пользователь ничего не введет и нажмет `Enter`. В `()` скобках указываются другие доступные опции.

По итогу интерактивного взаимодействия выше, работает вызов такой реализованной функции:

```python
select_sorted(sort_columns=['high'], order='desc', limit=50, filename='result.csv')
# записывает в result.csv данные из анализируемого файла, 
# отсортированные по колонке 'high'
# в порядке убывания
# первые 50 записей
```

Запуск скрипта для получения выборки по дате:

```bash
~$ poetry run get-banch
Дата в формате yyyy-mm-dd [all]: 2017-08-08
Тикер [all]: PCLN
Файл [dump.csv: 20170808PCLN.csv
```

При работе скрипта `get-by-date` если пользователь не ввел дату, используются все даты. Если не ввел тикер, берутся данные для всех тикеров.

Результат интерактивного взаимодействия, приведенного выше - срабатывание функции получения выборки со следующими входными параметрами:

```python
get_by_date(date="2017-08-08", name="PCLN", filename='20170808PCLN.csv')
# сохраняет в файл все данные для тикера "PCLN" за 2017-08-08
```

Пример взаимодействия, если надо сохранить данные только под одному тикеру:

```bash
~$ poetry run get-banch
Дата в формате yyyy-mm-dd [all]: 
Тикер [all]: PCLN
Файл [dump.csv: PCLN.csv
```

Надо получить данные по торгам всеми тикерами за определенный день:
