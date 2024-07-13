# praktika2024garpix

## Выполнила Горохова Полина Алексеевна 
## БПМ-22-1

### Индивудиальное задание 
 Дан json-файл, содержащий описание набора уникальных сущностей. Каждая сущность представлена набором признаков. Необходимо составить алгоритм, который за наименьшее число шагов (с наименьшей вычислительной сложностью) сможет определить минимальный по составу набор признаков, значения которых однозначно идентифицируют сущность в данном наборе (т.е. конкатенация значений этих признаков для каждой сущности может служить ее идентификатором).

- Язык разработки Python. 
- Функция для запуска кода имеет имя main и размещена в файле app.py, который размещен в корневой папке репозитория. Функция main принимает один аргумент типа “строка”, содержащий json-строку с исходными данными, и возвращает таблицу с одной колонкой, значения которой содержат искомый набор имен признаков. Возвращаемая таблица сериализована в виде csv-строки (UTF-8).   
- Программный код снабжен комментариями и сопровожден unit-тестами для проверки основных функций.

Главная функция с функцией запуска находится в файле app.py. 
- Чтобы запустить проверку качества кода, достаточно запустить app.py без аргументов:
```python app.py```
- Чтобы запустить с входными данными (json-строкой), нужно запустить файл app.py той же строкой, но с аргументами, например:

```python app.py
{
    "фамилия": "Смирнов",
    "имя": "Евгений",
    "отчество": "Александрович",
    "класс": "6",
    "подгруппа": "1",
    "предмет": "История",
    "видДеятельности": "Учебная",
    "количествоЧасовВнеделю": "2"
}

