from dataclasses import dataclass

import pytest


@pytest.mark.parametrize("browser, version",
                         [("Chrome", "94-rc1:build124125829"), ("Firefox", 85), ("Safari", 13.2)],
                         ids=["Chrome", "Firefox", "Safari"]
                         )
def test_with_param(browser, version):
    assert browser in ["Chrome", "Firefox", "Safari"]


@pytest.mark.parametrize("browser", ["Chrome", "Firefox", "Safari"])
@pytest.mark.parametrize("test_role", ["manager", "guest", "admin"])
def test_with_matrix_param(browser, test_role):
    pass


'''
Пример работы с параметром - когда нам надо среди параметров запускать тест с конкретным одним и например ждем что он может упасть
Тогда мы добавляем доп марку - pytest.param() в которой можем прописать xfail
'''

@pytest.mark.parametrize("browser",
                         [
                             pytest.param("Chrome", id="Chrome"),
                             pytest.param("Firefox", marks=[pytest.mark.slow]),
                             pytest.param("Safari", marks=[pytest.mark.xfail(reason="TASK-123 Safari problem")]),
                         ]
                         )
def test_with_param_marks(browser):
    pass

# ---------------------------------------------


@pytest.fixture()
def chrome():
    pass


@pytest.fixture()
def firefox():
    pass


@pytest.fixture()
def safari():
    pass


@pytest.fixture(params=["Chrome", "Firefox", "Safari"])
def browser(request):
    if request.param == "Chrome":
        return request.getfixturevalue("chrome")
    if request.param == "Firefox":
        return request.getfixturevalue("firefox")
    if request.param == "Safari":
        return request.getfixturevalue("safari")


def test_with_parametrized_fixture(browser):
    pass


@pytest.mark.parametrize("browser", ["Chrome"], indirect=True)
def test_with_indirect_parametrization(browser):
    pass

'''
Такая конструкция позволяет упростить наименование параметризации - вначале в файле задаем переменную crome_only 
которой и  присвоим уже наш ожидаемый параметр а далее на сам тест навесим именно эту переменную'''

chrome_only = pytest.mark.parametrize("browser", ["Chrome"], indirect=True)


@chrome_only
def test_chrome_extension(browser):
    pass



'''
Функции для отображения пользователей. Чтобы получить данные польтзователя, мы сделали доп функцию, прописали там как должна выводиться инфа о
пользователе и далее эту передаем в параметризацию
аргумент ids=repr - тк Юзер у нас  - dataclass - для егопоказа есть эта функция - те не надо будет передавать нашу созданную функцию
 для этого мы в dataclass создадим нашу функцию которая будет определять какие данные пользователя выводить - 
 __repr__() '''

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


@pytest.mark.parametrize("user", [user1, user2], ids=repr)
def test_users(user):
    pass


''' как вариант можем напрямую передавать нашу созданную функцию'''

@pytest.mark.parametrize("user", [user1, user2], ids=show_user)
def test_users(user):
    pass