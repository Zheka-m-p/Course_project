def main():
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

                # print('О, такие данные я уже сортировал, держи быстренько результат')
                # with open(file_name_for_cache, 'w') as writer_object:
                #     print(first_string, file=writer_object)
                #     for i in range(sample_length):
                #         print('  '.join([k.ljust(13) for k in dictionary[key_string][i]]), file=writer_object)

                print('О, такие данные я уже сортировал, держи быстренько результат')
                with open(file_name_for_cache, 'w') as writer_object:
                    print(first_string, file=writer_object)
                    # print(dictionary.values())
                    for i in range(len(dictionary[key_string])):
                        # print(i) # посмотреть. в чем ошибка при и
                        print('  '.join([k.ljust(13) for k in dictionary[key_string][i]]), file=writer_object)
                        # print('  '.join([k.ljust(13) for k in i]), file=writer_object)
                        # try:
                        #     print('  '.join([k.ljust(13) for k in dictionary[key_string][i]]), file=writer_object)
                        # except TypeError:
                        #     pass

        return inner


    @new_cache_memory  # противный декоратор, который не так работает, когда в одной сессии пытаешься взять данные из кэша.
    # Либо падает с ошибкой(если брать все значения без указывания даты или тикера), либо ничего не записывает.
    # ПОФИКШЕНО
    def get_by_data(date='', name='', filename='new_dump.csv'):
        """Функция добавляет данные в файл по указанной дате и тикеру компании, файл можно выбрать самим."""
        # dataset_name = dataset_name
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
                res = sorted(res, key=lambda x: (x[0], x[-1]))  # Если сохранять в тот же файл, то падает с ошибкой
            # print(type(res))
            res = list(res)  # Пришлось обернуть в лист, чтобы заработало
            # print(type(res))
            print(first_string, file=writer_object)
            for i in res:
                print('  '.join([k.ljust(13) for k in i]), file=writer_object)

        return res


    def requests_data_to_be_sorted_by_date():
        """Запрашивает данные у пользователя, чтобы потом сортировать по дате, тикеру или всё сразу, воз"""
        print('Дата в формате yyyy-mm-dd [all]: ', end='')
        sample_data = input()
        # sample_data = '' if
        print('Название тикера [all]: ', end='')
        sample_ticker = input()
        print('Название файла для сохранения результата [dump.csv]: ', end='')
        sample_file_name = input()
        # получить название файла, добавив в конце расширение "cvs", если пустая строка - то значения по умолчанию
        sample_file_name = sample_file_name + '.csv' if sample_file_name else 'dump.csv'  # обработано, но не работает

        return sample_data, sample_ticker, sample_file_name


    # selected_date, selected_ticker, selected_file_name = requests_data_to_be_sorted_by_date()
    # print(selected_date, selected_ticker, selected_file_name)
    # get_by_data(date=selected_date, name=selected_ticker, filename=selected_file_name)

    flag = True
    while flag:
        selected_date, selected_ticker, selected_file_name = requests_data_to_be_sorted_by_date()
        print(selected_date, ' - это наша дата для выборки')
        print(selected_ticker, ' - это наш тикер для выборки')
        print(selected_file_name, ' - это наш дата для записи выборки')
        print(len(selected_date), len(selected_ticker), len(selected_file_name))
        get_by_data(date=selected_date, name=selected_ticker, filename=selected_file_name)
        print()
        print('Напишете что-нибудь если хотите продолжить работу, если нет - нажминет "Enter".')
        flag = input()


if __name__ == '__main__':
    main()