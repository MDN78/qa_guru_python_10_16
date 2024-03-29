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
pytest --co # позволяет вывести все доступные тесты в директории
pytest -k "вхождение строки любого теста" # запуск конкретного теста
pytest --markers # вывод всех доступных марок в проекте
pytest --fixtures # выводит список всех доступных фикстур
pytest -durations=x # вывод x самых долгих тестов
pytest -l # выводит значения переменных в момент ошибки
pytest --setup-plan # тесты не запускает, но выводит план запуска тестов
```

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