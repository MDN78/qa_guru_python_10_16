## Pytest, параметры

### Содержание лекции:

1. Аргументы запуска. Собираем фикстуры, марки и другую полезную информацию для отладки
2. Марки. Пропускаем тесты правильно
3. Параметризация. На тесте, на фикстуре. Переопределение параметров

## Homework

- Реализовать автотест для github.com, который заходит на страницу, ищет кнопку Sign In, и нажимает на нее (
  авторизоваться не нужно);

- Параметризовать тест различным размером окна браузера;

- Обратите внимание, что для мобильной версии сайта потребуется другой автотест из-за изменения структуры локаторов;

- Сделайте два варианта пропуска неподходящих параметров и тестов.


1. Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот);

2. Переопределите параметр с помощью indirect;

3. Сделайте разные фикстуры для каждого тест

## Аргументы запуска

``` command
pytest --co (pytest --collect-only) # позволяет вывести все доступные тесты в директории/проекте
pytest -k "вхождение строки любого теста" # запуск конкретного теста
pytest -m "марка теста" # запуск тестов с определённой маркой
pytest --markers # вывод всех доступных марок в проекте
pytest --fixtures # выводит список всех доступных фикстур
pytest --durations=x # вывод x самых долгих тестов
pytest -l (pytest --showlocals) # выводит локальные переменные в тестах
pytest --setup-plan # тесты не запускает, но выводит план запуска тестов
pytest -v (pytest --verbose) # выводит более подробную информацию о тестах
pytest -s # выводит вывод тестов в реальном времени
pytest -rfEX # выводит только ошибки и отчёт о тестах
```

## Задаем по умолчанию для всех тестов определенные параметры
Для этого в файле `pytest.ini` нужно добавить следующие строки:

```ini
[pytest]
addopts = -v -l --durations=10
```  

Или в файле `pyproject.toml` если используется poetry в проекте:
```ini
[tool.pytest.ini_options]
addopts = "-v -l --durations=10"
```
Теперь при запуске тестов, будут использоваться параметры `-v -l --durations=10` по умолчанию.

## Marks

Марки буквально позволяют маркировать тесты, разделять их на группы, управлять отдельными тестами и группами.

Краткий список марок:

Марка `skip` позволяет пропустить тест и не выполнять его содержимое. С помощью аргумента reason следует указывать
причину пропуска;

```python
@pytest.mark.skip()
@pytest.mark.skip(reason="Этот тест еще не завершен")
```

skipif - пропуск по условию. Лучше всего описывать в виде переменной принимает True/False

```python 
is_linux = True


@pytest.mark.skipif(True)
@pytest.mark.skipif(is_linux)
@pytest.mark.skipif(is_linux, reason='Тест пропущен так как условие is_skip = True')
```

```python
pytestmark = pytest.mark.skip(reason="Когда нужно пропустить весь файл")
```

Марка `xfail` позволяет указать, что тест заведомо может не работать. При этом тест запустится. Причину также указывают
с помощью аргумента reason, а аргумент `strict`  заставляет тест упасть, если ошибка не произошла сама.
Аргумент `raises` заставляет тест отработать только в том случае, если в тесте есть какой-то конкретный тип ошибки;

```python
@pytest.mark.xfail()
@pytest.mark.xfail(reason="", strict=True, raises="AssertionError")
```
```python
@pytest.mark.xfail()

@pytest.mark.xfail(reason="просто потому что")
def test_fail():
    user1 = random.randint(0, 100)
    user2 = random.randint(0, 100)

    assert user1 <= 100
    assert user2 <= 100
    try:
        assert user1 == user2
    except AssertionError:
        pytest.xfail("TASK-1234")
```  

Если тест прошел успешно(исправили к примеру баг), то он будет отмечен как `XPASS`, если тест упал, 
то он будет отмечен как `XFAIL`.
Если на тест навешена марка `xfail`, и он будет запущен, но он не проверит ошибки синтаксиса внутри теста. 
То есть, если внутри теста есть ошибки, то они не будут показаны. 
Чтобы подобного избежать, можно не использовать марку `xfail`, а использовать `try` и `except`:

```python
def test_fail():
    user1 = random.randint(0, 100)
    user2 = random.randint(0, 100)

    assert user1 <= 100
    assert user2 <= 100
    try:
        assert user1 == user2
    except AssertionError:
        pytest.xfail("TASK-1234")
```  
И если в тесте есть ошибки синтаксиса, то они будут показаны.  

## usefixtures  
Марка usefixtures позволяет указать, какие фикстуры использовать для теста. С помощью аргумента fixtures указывают, какие фикстуры использовать;  

```python
@pytest.mark.usefixtures("fixture_name")
```  
## Как навесить марку на весь файл с тестами  
Если необходимо навесить марку на весь файл с тестами, то можно использовать следующий код:  
```python
import pytest

pytestmark = pytest.mark.skip(reason="TASK-1234 Тест нестабильный потому что время от времени не хватает таймаута")
```  
## Как запустить тесты несколько раз
Для запуска тестов несколько раз, можно использовать плагин `pytest-repeat`. Для этого нужно установить пакет:
```commandline
pip install pytest-repeat
```

Если необходимо запускать все тесты несколько раз, то можно добавить в файл `pytest.ini` следующие строки:
```ini
[pytest]
addopts = --count=3
```  

Теперь все тесты будут запускаться три раза.

Если необходимо запустить только определенный тест несколько раз, то можно использовать следующую команду:
```commandline
pytest --count=3 test_simple.py
```

Выполнение команды `pytest --count=3 test_simple.py` позволяет запустить тесты определенное количество раз(В данном случае 3 раза).

Свои марки надо регистрировать в файле `pytest.ini`:

```python
[pytest]
markers =
  slow: marks tests as slow(deselect with '-m "not slow"'),
  fast: marks tests as fast

```

Если используется конфигурационный общий файл для Python - `pyproject.toml` :

```python
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
```

Вот так лучше использовать марку xfail - внутри самого теста, на ассерте

```python
def test_something():
    a = 2
    b = 2

    try:
        assert a == b
    except AssertionError:
        pytest.xfail("TASK-1234 Test is xfail because is flaky")

```
## Параметризация  
[Documentation](https://docs.pytest.org/en/7.1.x/how-to/parametrize.html)  
[structure](https://github.com/pytest-dev/pytest/issues/3261#issuecomment-369740536)  
[How-to](https://pytest-xdist.readthedocs.io/en/latest/how-to.html)  
[scope sessions](https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once)  
[Hooks](https://docs.pytest.org/en/7.2.x/reference/reference.html#hooks)  

Можно добавлять свои параметры - тогда тест будет использовать данные из представленных данных.
Если данные трудно читаемые можно использовать аргумент `ids=` который позволяет выводить в более читаемом виде  
```python
@pytest.mark.parametrize("browser, version",
                         [("Chrome", "94-rc1:build124125829"), ("Firefox", 85), ("Safari", 13.2)],
                         ids=["Chrome", "Firefox", "Safari"]
                         )
def test_with_param(browser, version):
    assert browser in ["Chrome", "Firefox", "Safari"]
```
Аргумент `indirect=` позволяет переопределить параметры у фикстуры - в примере фикстуру `browser` мы задали
что будет запускать именно chrome  
```python
@pytest.mark.parametrize("browser", ["Chrome"], indirect=True)
def test_with_indirect_parametrization(browser):
    pass
```

## Параметры параметризации pytest.param  
```python
@pytest.mark.parametrize("browser",
                         [
                             pytest.param("Chrome", id="Chrome"),
                             pytest.param("Firefox", marks=[pytest.mark.slow]),
                             pytest.param("Safari", marks=[pytest.mark.xfail(reason="TASK-123 Safari problem")]),
                         ]
                         )
def test_with_param_marks(browser):
    pass
```  
В данной функции тестирования, мы используем параметризацию с помощью `pytest.param`.
`pytest.param` позволяет добавить маркировку к параметрам.  

## Параметризация фикстур  
```python
@pytest.fixture(params=["Chrome", "Firefox", "Safari"])
def browser(request):
    if request.param == "Chrome":
        return ""
    if request.param == "Firefox":
        return ""
    if request.param == "Safari":
        return ""


def test_with_parametrized_fixture(browser):
    pass
```  
В данном примере, мы параметризуем фикстуру `browser. request.param` - это параметр, который мы передаем в фикстуру. А из фикстуры мы получаем значение, через `request`.  

## Indirect параметризация  
```python
@pytest.fixture(params=["Chrome", "Firefox", "Safari"])
def browser(request):
    if request.param == "Chrome":
        return ""
    if request.param == "Firefox":
        return ""
    if request.param == "Safari":
        return ""


@pytest.mark.parametrize("browser", ["Chrome"], indirect=True) # переопределяем фикстуру, чтобы запускалось только с Chrome
def test_with_indirect_parametrization(browser):
    pass
```
В данном примере, мы используем параметризацию фикстуры с помощью `indirect=True`. Это позволяет передать параметры из фикстуры в тест.

Индиректная параметризация позволяет переопределить фикстуру, чтобы запускалось только с определенным параметром.  

## Присваивание фикстуры в переменную
```python


@pytest.fixture(params=["Chrome", "Firefox", "Safari"])
def browser(request):
    if request.param == "Chrome":
        return ""
    if request.param == "Firefox":
        return ""
    if request.param == "Safari":
        return ""

    
chrome_only = pytest.mark.parametrize("browser", ["Chrome"], indirect=True)


@chrome_only
def test_chrome_extension(browser):
    pass
    
```  

В данном примере, мы присваиваем фикстуру в переменную chrome_only. И используем ее в декораторе `@chrome_only`. 
Это позволяет запускать тесты только с определенными параметрами и использовать более красивые и читабельные декораторы.



## __repr__ в параметризации  

```python
@dataclass
class User:
    id: int
    name: str
    age: int
    description: str

    def __repr__(self):
        return f"{self.name} ({self.id})"


user1 = User(id=1, name="Mario", age=32, description="something " * 10)
user2 = User(id=2, name="Wario", age=62, description="else " * 10)


def show_user(user):
    return f"{user.name} ({user.id})"


@pytest.mark.parametrize("user", [user1, user2], ids=show_user)
def test_users(user):
    pass
```
В данном примере, мы используем параметризацию с помощью дата класса `User`. 
Используем функцию `show_user` для отображения имени и id пользователя в названии теста. 
И передаем ее в параметр `ids`. Также метод` __repr__` в датаклассе, позволяет получить строковое представление объекта в виде имени и id. И потом использовать его в ids.  

