def main():
    """Главная функция нашего файла.
    P.S. если её не создать, то не будет работать запуск через poetry. """

    def cache_memory(func):
        """Декоратор, который либо находит по заданным параметрам выборку и записывает в файл,
        либо берёт данные, полученные ранее, из хэша и так же записывает в файл"""
        dictionary = {}

        def inner(*args, **kwargs):
            print()
            new_keys = []
            for k, v in kwargs.items():
                new_keys.append(str(v))
            sample_length = kwargs['limit']  # Нужное значение кол-ва строк для записи в файл, при заполнении из хэша
            file_name_for_cache = new_keys.pop()  # Имя файла, в который мы будем записывать новый запрос
            print(file_name_for_cache, '- это имя файла куда будет вестись запись наших данных')
            key_string = ''.join(new_keys)
            if key_string not in dictionary:
                print('Хммммм, впервые вижу такие параметры, придётся напрячь свои компьютерные мозги, чтобы посчитать')
                dictionary[key_string] = func(*args, **kwargs)
            else:
                print('О, такие данные я уже сортировал, держи быстренько результат')
                with open(file_name_for_cache, 'w') as writer_object:
                    print(first_string, file=writer_object)
                    for i in range(sample_length):
                        print('  '.join([k.ljust(13) for k in dictionary[key_string][i]]), file=writer_object)

        return inner

    @cache_memory
    def select_sorted(sort_columns=['high'], limit=10, group_by_name=False, order='desc', filename='dump.csv'):
        """Сортирует файл по заданым аргументам и выводит результат в файл 'dump.csv'"""
        dict_sort_columns = {'date': 0, 'open': 1, 'high': 2, 'low': 3, 'close': 4, 'volume': 5}
        index_sort_columns = dict_sort_columns[
            sort_columns[0]]  # получаем индекс столбца, по которому будем сортировать
        with open('all_stocks_5yr.csv', 'r') as file_:
            global first_string
            first_string = '  '.join([i.ljust(13) for i in (file_.readline().strip().split(','))])

            # считываем из файла и создаем генераторное вырежение состоящее из списков, игнорируем строки
            # с пустыми ячейкамим в выбранном нами столбце, по которому будет вестись сортировка
            if group_by_name:
                ans = (i.strip().split(',') for i in file_ if
                       i.strip().split(',')[
                           -1] == group_by_name)  # генераторное выражение,если нужна группировка по имемни
            else:
                ans = (i.strip().split(',') for i in file_ if i.strip().split(',')[index_sort_columns] != '')

            # выбираем лямба-функцию для ключа сортиривки в зависимости то того, по какому столбцу будем сортировать
            if index_sort_columns == 0:
                lambda_for_keys = lambda x: x[index_sort_columns]
            else:
                lambda_for_keys = lambda x: float(x[index_sort_columns])

            # выбираем направление сортировки, desk -  по убыванию, иначе - по возрастанию
            if order == 'desc':
                res = sorted(ans, key=lambda_for_keys, reverse=True)
            else:
                res = sorted(ans, key=lambda_for_keys)  # работае такое вариант, но проблема с пустой строкой

        with open(filename, 'w') as write_object:
            print(first_string, file=write_object)
            for i in range(limit):
                print('  '.join([k.ljust(13) for k in res[i]]), file=write_object)

        return res

    def requests_data_for_sorting():  # запросить данные для сортировки
        """Запрашивает у пользователя данные для того, чтобы в будущем их использовать для сортировки
         и получения нужнымх нам значений. Выводит значение по умолчанию  если были введены некоррекнтры данные
         или нажата клавиша Enter"""
        text = "Сортировать по цене\nоткрытия (1)\nзакрытия (2)\nмаксимум [3]\nминимум (4)\nобъем (5)"
        print(text)
        dict_sort_columns = {'1': ['open'], '2': ['close'], '3': ['high'], '4': ['low'], '5': ['volume']}
        choice_sort_column_selection = dict_sort_columns.setdefault(input(), ['high'])
        print('Порядок по убыванию [1] / возрастанию (2): ', end='')
        dict_sort_direction = {'1': 'desc', '2': 'asc'}
        choice_sort_direction = dict_sort_direction.setdefault(input(), 'desc')
        print('Ограничение выборки [10]: ', end='')
        try:  # получаем чисило или же значение по умолчанию
            value_limit = int(input())
        except ValueError:
            value_limit = 10
        print('Название файла для сохранения результата [dump.csv]: ', end='')
        file_name = input()
        # получить название файла, добавив в конце расширение "cvs", если пустая строка - то значения по умолчанию
        file_name = file_name + '.csv' if file_name else 'dump.csv'

        return choice_sort_column_selection, choice_sort_direction, value_limit, file_name

    flag = True
    while flag:
        sort_column, sort_diection, numbers_of_lines, file_name = requests_data_for_sorting()  # данны для сортировки от чел-ка.
        select_sorted(sort_columns=sort_column, order=sort_diection, limit=numbers_of_lines, filename=file_name)
        print()
        print('Напишете что-нибудь если хотите продолжить работу, если нет - нажминет "Enter".')
        flag = input()


if __name__ == '__main__':
    main()
