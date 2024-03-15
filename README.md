## Pytest, параметры  
### Содержание лекции:  
1.  Аргументы запуска. Собираем фикстуры, марки и другую полезную информацию для отладки
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

Марка `skip` позволяет пропустить тест и не выполнять его содержимое. С помощью аргумента reason следует указывать причину пропуска;  
```python
@pytest.mark.skip()
@pytest.mark.skip(reason="Этот тест еще не завершен")
```

Марка `xfail` позволяет указать, что тест заведомо может не работать. При этом тест запустится. Причину также указывают с помощью аргумента reason, а аргумент `strict`  заставляет тест упасть, если ошибка не произошла сама. Аргумент `raises` заставляет тест отработать только в том случае, если в тесте есть какой-то конкретный тип ошибки;  
```python
@pytest.mark.xfail()
@pytest.mark.xfail(reason="", strict=True, raises="AssertionError")
```
