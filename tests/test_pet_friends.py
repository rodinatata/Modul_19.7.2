from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends() # инициализация библиотеки в переменную


def test_get_api_key_for_valid_user_passed(email=valid_email, password=valid_password):
    """ Тест на авторизацию с валидными данными: api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправка запроса и сохранение полученного ответа с кодом статуса в status, а текста ответа в result
    status, result = pf.get_api_key(email, password) # вызов метода из библиотеки

    # Сравнение полученных данных с ОР
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key_passed(filter=''):
    """ Тест на получения списка всех питомцев. Ответ на запрос возвращает не пустой список."""

    # -, т.к. статус не нужен, получение ключа и сохранение в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter) # Доступное значение параметра filter-'my_pets' или ''

    # Сравнение полученных данных с ОР
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_new_pet_with_valid_data_passed(name='Котик', animal_type='кот',
                                     age='4', pet_photo='images/cat.jpeg'):
    """Тест на возможность добавления питомца с корректными данными"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сравнение полученного ответа с ОР
    assert status == 200
    assert result['name'] == name


def test_delete_self_pet_passed():
    """Тест на возможность удаления питомца"""

    # Запрос ключа auth_key и списка своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список своих питомцев пуст, то добавляем нового и запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Тестокот", "кот", "3", "images/cat1.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # id первого питомца из списка (последнего добавленного) и запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрос списка своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверка, что статус ответа = 200, и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_self_pet_info_passed(name='Кекс', animal_type='Котэ', age=5):
    """Тест на возможность обновления информации о питомце"""

    # Получение ключа auth_key и списка своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем имя, тип и возраст первого в списке питомца (последнего добавленного)
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверка, что статус ответа = 200, и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если спиок питомцев пуст, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пуст")


# ТЕСТ 01
def test_post_add_new_pet_simple_with_valid_data_passed(name='Бархатный Животик', animal_type='кот', age='4'):
    """Тест на возможность добавления питомца без фото с корректными данными"""

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)

    # Сравнение полученного ответа с ОР
    assert status == 200
    assert result['name'] == name


# ТЕСТ 02
def test_post_add_pet_photo_passed(pet_photo='images/cat1.jpeg'):
    """Тест на возможность добавления фото питомца"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получение ключа auth_key и списка своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото для последнего созданного питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверка, что фото успешно добавлено
        assert status == 200
    else:
        # Если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пуст")


# ТЕСТ 03
def test_get_api_key_for_invalid_user_failed(email=valid_email, password=valid_password):
    """ Тест на авторизацию с невалидными данными (логином или паролем)"""

    # Отправка запроса и сохранение полученного ответа с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password) # вызов метода из библиотеки

    # Проверка, что авторизация не удалась
    assert status == 401


# ТЕСТ 04
def test_post_add_new_pet_with_invalid_auth_key_passed(name='Пушистик', animal_type='пес',
                                     age='2', pet_photo='images/dog.jpeg'):
    """Тест на невозможность добавления питомца с корректными данными и неверным ключом авторизации"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Неверный ключ авторизации
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729hdyrmcls87563snt65'}

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверка, что ключ не принят и питомец не добавлен
    assert status == 403


# ТЕСТ 05
def test_post_add_new_pet_without_auth_key_passed(name='Пэтти', animal_type='кошка',
                                     age='1', pet_photo='images/cat1.jpeg'):
    """Тест на невозможность добавления питомца с корректными данными и пустым ключом авторизации"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пустой ключ авторизации
    auth_key = {'key': ''}

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверка, что ключ не принят и питомец не добавлен
    assert status == 403


# ТЕСТ 06
def test_post_add_new_pet_simple_with_invalid_name_failed(name='97)._#@1', animal_type='кот', age='4'):
    """Тест на невозможность добавления питомца с указанием невалидного имени питомца - цифры и символы"""

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)

    # Сравнение полученного ответа с ОР
    assert status != 200


# ТЕСТ 07
def test_post_add_new_pet_simple_without_name_failed(name=None, animal_type='кот', age='4'):
    """Тест на невозможность добавления питомца без указания его имени"""

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet_simple(auth_key, name, animal_type, age)

    # Сравнение полученного ответа с ОР
    assert status != 200


# ТЕСТ 08
def test_post_add_new_pet_with_invalid_animal_type_failed(name='Друг', animal_type='97)._#@1',
                                              age='3', pet_photo='images/dog.jpeg'):
    """Тест на невозможность добавления питомца с указанием невалидного значения породы - цифры и символы"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сравнение полученного ответа с ОР
    assert status != 200

# ТЕСТ 09
def test_post_add_new_pet_without_animal_type_failed(name='Друг', animal_type=None,
                                              age='3', pet_photo='images/dog.jpeg'):
    """Тест на невозможность добавления питомца без указания его породы"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сравнение полученного ответа с ОР
    assert status != 200


# ТЕСТ 10
def test_post_add_new_pet_with_invalid_age_failed(name='Друг', animal_type='Каталонская овчарка',
                                              age='-7', pet_photo='images/dog.jpeg'):
    """Тест на невозможность добавления питомца c указанием невалидного значения возраста - отрицательного"""

    # Получение полного пути изображения питомца и сохранение в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрос ключа api и сохранение в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сравнение полученного ответа с ОР
    assert status != 200
