import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
    # products - список продукции
    # id - номер товара
    # name - наименование
    # provider - автодиллер
    # price - цена
    # generation - поколение
    # guarantee period  - гарантийный срок
    # count - число позиций на складе
products = [{
    "id": 0,
    "name": "Киа Сид",
    "provider": "Киа Моторс",
    "price": 1280450.90,
    "generation": "3",
    "guarantee_period": 5,
    "count": 4
}, {
    "id": 1,
    "name": "Киа Рио",
    "provider": "Киа Моторс",
    "price": 1083600.90,
    "generation": "3",
    "guarantee_period": 5,
    "count": 3
}, {
    "id": 2,
    "name": "Патриот",
    "provider": "УАЗ",
    "price": 1183200.90,
    "generation": "3",
    "guarantee_period": 3,
    "count": 10
}, {
    "id": 3,
    "name": "Веста",
    "provider": "АвтоВАЗ",
    "price": 983700.90,
    "generation": "1",
    "guarantee_period": 5,
    "count": 12
}, {
    "id": 4,
    "name": "Рено Дастер",
    "provider": "РеноАвто",
    "price": 1340370.90,
    "generation": "2",
    "guarantee_period": 7,
    "count": 4
}, {
    "id": 5,
    "name": "Икс Рей",
    "provider": "АвтоВАЗ",
    "price": 999070.90,
    "generation": "1",
    "guarantee_period": 5,
    "count": 2
}, {
    "id": 6,
    "name": "Ларгус",
    "provider": "АвтоВАЗ",
    "price": 823990.40,
    "generation": "1",
    "guarantee_period": 5,
    "count": 9
}]


# перенос веб-приложения flask, использующего веб-сервер uWSGI, на веб-сервер ASGI (uvicorn)
app = FastAPI()
@app.post("/docs", status_code=200, description="Описание интерфейса")
def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url,title="Swagger UI")


# Добавление пользовательского интерфейса Swagger в app
@app.get("/find_name", status_code=200, description="Поиск по названию")
def find_name_(name: str = None):
    if name:
        for i in range(len(products)):
            if name == products[i]["name"]:
                return ">>>", products[i]
    return "не найдено"


@app.get("/api/status", status_code=200, description="Поиск минимального, максимального или среднего для числовых полей. Укажите min/max/average")

async def min_max_average(guarantee_period: str = None, count: str = None, price: str = None):
    empty_list = [] # Создаем пустой список, куда будем сохранять значения
    # Каждое поле заполнять не обязательно, поэтому проверяем на наличие значений
    if price:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["price"]) # Заполняем пустой списо _are значениями цены из products

        if price == "min":
            empty_list.append({"price": min(_are)})
        if price == "max":
            empty_list.append({"price": max(_are)})
        if price == "average":
            empty_list.append({"price": sum(_are) / len(_are)})

    if count:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["count"])

        if count == "min":
            empty_list.append({"count": min(_are)})
        if count == "max":
            empty_list.append({"count": max(_are)})
        if count == "average":
            empty_list.append({"count": sum(_are) / len(_are)})

    if guarantee_period:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["guarantee_period"])

        if count == "min":
            empty_list.append({"guarantee_period": min(_are)})
        if count == "max":
            empty_list.append({"guarantee_period": max(_are)})
        if count == "average":
            empty_list.append({"guarantee_period": sum(_are) / len(_are)})

    return empty_list

@app.put("/api/change", status_code=200, description="Изменить данные о товаре")
async def changing(id: int, name: str = None, provider: str = None,
price: float = None, generation: str = None, guarantee_period: int = None, count: int = None):
    global products
    # Ввод id обязателен
    for i in range(len(products)):
        if products[i]["id"] == id:
            # Проверяем каждый параметр товара на наличие значения, если оно имеется, то изменяем
            if name:
                products[i]['name'] = name
            if provider:
                products[i]['provider'] = provider
            if price:
                products[i]['price'] = price
            if generation:
                products[i]['generation'] = generation
            if guarantee_period:
                products[i]['guarantee_period'] = guarantee_period
            if count:
                products[i]['count'] = count
            return {">>>": "Данные изменены"}
    return {">>>": "Товар не найден"}


@app.put("/api/add", status_code=200, description="Добавить товар. Необходимо ввести все параметры товара")
async def adding(id: int, name: str, provider: str, price: float, generation: str, guarantee_period: int,
count: float): # Получаем на вход все параметры товара
    global products # Объявляем products глобально, чтобы ее обновления вступали в силу и вне функции
    products.append({"id": id,
            "name": name,
            "provider": provider,
            "price": price,
            "generation": generation,
            "guarantee_period": guarantee_period,
            "count": count})
    return {">>>": "Товар добавлен"}


@app.delete("/api/delete", status_code=200, description="Удалить товар по id")
async def del_id(id: int):
    global products
    for i in range(len(products)):
        if products[i]["id"] == id:
            products.pop(i) # Функция, которая удаляет из списка значение по заданному индексу
            return {">>>": "Товар удален"}
    return {">>>": "Товар не найден"}


@app.get("/api/find", status_code=200, description="Найти товар по id. Введите all чтобы показать все товары")
async def find_id(id: str): # Получим на вход id в виде строки
    if id == "all": # Если пользователь хочет вывести все товары
        _are = {" ": []} # Создаем еще один список, чтобы вывести все единицы товара
        for i in range(len(products)):
            _are[" "].append(products[i])
        return _are
    else:
        for i in range(len(products)):
            if products[i]["id"] == int(id): # Ищем товар, с id, которое было указано и выводим его
                return {">>>": products[int(id)]}
    return {">>>": "Товар не найден"}

    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=5000) # port 8000 нужен, чтобы не было пересечений ссылок
# Запуск приложения, как веб-сервер ASG