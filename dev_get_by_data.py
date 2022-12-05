def main():
    """Главная функция нашего файла.
    P.S. если её не создать, то не будет работать запуск через poetry. """

    def new_cache_memory(func):
        """Декоратор, который либо находит по заданным параметрам выборку и записывает в файл,
        либо берёт данные, полученные ранее, из хэша и так же записывает в файл"""
        dictionary = {}

        def inner(*args, **kwargs):
            print()
            new_keys = []
            for k, v in kwargs.items():
                new_keys.append(str(v))
            file_name_for_cache = new_keys.pop()  # Имя файла, в который мы будем записывать новый запрос
            print(file_name_for_cache, '- это имя файла куда будет вестись запись наших данных')
            key_string = ''.join(new_keys)  # название ключа, для записи в словарь
            if key_string not in dictionary:
                print('Хммммм, впервые вижу такие параметры, придётся напрячь свои компьютерные мозги, чтобы посчитать')
                dictionary[key_string] = func(*args, **kwargs)
            else:
                print('О, такие данные я уже сортировал, держи быстренько результат')
                with open(file_name_for_cache, 'w') as writer_object:
                    print(first_string, file=writer_object)
                    for i in range(len(dictionary[key_string])):
                        print('  '.join([k.ljust(13) for k in dictionary[key_string][i]]), file=writer_object)

        return inner

    @new_cache_memory
    def get_by_data(date='', name='', filename='new_dump.csv'):
        """Функция добавляет данные в файл по указанной дате и тикеру компании, файл можно выбрать самим."""
        with open('all_stocks_5yr.csv', 'r') as file_, open(filename, 'w') as writer_object:
            global first_string
            first_string = '  '.join([i.ljust(13) for i in (file_.readline().strip().split(','))])
            if date and name:
                res = (i.strip().split(',') for i in file_ if
                       i.strip().split(',')[-1] == name and i.strip().split(',')[0] == date)
            elif date and not name:
                res = (i.strip().split(',') for i in file_ if i.strip().split(',')[0] == date)
            elif not date and name:
                res = (i.strip().split(',') for i in file_ if i.strip().split(',')[-1] == name)
            elif not date and not name:
                res = (i.strip().split(',') for i in file_)
                # дополнительно сортируем по дате. т.к. только в этом случае это нам надо. в других уже отсортировано всё
                res = sorted(res, key=lambda x: (x[0], x[-1]))
            res = list(res)  # Пришлось обернуть в лист, чтобы заработало
            print(first_string, file=writer_object)
            for i in res:
                print('  '.join([k.ljust(13) for k in i]), file=writer_object)

        return res

    def requests_data_to_be_sorted_by_date():
        """Запрашивает данные у пользователя для сортировки, затем возвращает эти значения"""
        print('Дата в формате yyyy-mm-dd [all]: ', end='')
        sample_data = input()
        print('Название тикера [all]: ', end='')
        sample_ticker = input()
        print('Название файла для сохранения результата [dump.csv]: ', end='')
        sample_file_name = input()
        # получить название файла, добавив в конце расширение "cvs", если пустая строка - то значения по умолчанию
        sample_file_name = sample_file_name + '.csv' if sample_file_name else 'dump.csv'

        return sample_data, sample_ticker, sample_file_name

    flag = True
    while flag:
        selected_date, selected_ticker, selected_file_name = requests_data_to_be_sorted_by_date()
        print(len(selected_date), len(selected_ticker), len(selected_file_name))
        get_by_data(date=selected_date, name=selected_ticker, filename=selected_file_name)
        print()
        print('Напишете что-нибудь если хотите продолжить работу, если нет - нажминет "Enter".')
        flag = input()


if __name__ == '__main__':
    main()
