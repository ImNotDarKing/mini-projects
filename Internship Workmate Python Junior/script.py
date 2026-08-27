import argparse
import csv
from tabulate import tabulate

AGGREGATIONS = {
    "min": lambda nums: min(nums),
    "max": lambda nums: max(nums),
    "avg": lambda nums: sum(nums) / len(nums),
}

def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Инструмент для обработки данных"
    )

    parser.add_argument("source_file", help="Путь к файлу")

    parser.add_argument("--where", help="Фильтрация вида 'column=value' или 'column>value'")

    parser.add_argument("--aggregate",  help="Агрегация вида 'column=operation' где operation: min, max, avg")

    return parser.parse_args()


def parse_filter_condition(condition_str: str) -> tuple[str, str, str]:

    if "=" in condition_str:
        parts = condition_str.split("=")
        column = parts[0]
        value = parts[1]
        operation = "eq"
        return column, operation, value

    if ">" in condition_str:
        parts = condition_str.split(">")
        column = parts[0]
        value = parts[1]
        operation = "gt"
        return column, operation, value

    if "<" in condition_str:
        parts = condition_str.split("<")
        column = parts[0]
        value = parts[1]
        operation = "lt"
        return column, operation, value


def parse_aggregate_condition(condition_str: str) -> tuple[str, str]:

    column, operation = condition_str.split("=")

    return column, operation


def load_csv_data(filepath: str) -> tuple[list[str], list[dict]]:
    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        headers = reader.fieldnames

        rows = list(reader)

    return headers, rows


def filter_records(data_list: list[dict], column: str, operation: str, target_value: str) -> list[dict]:
    result = []

    for row in data_list:
        current_value = row[column]

        try:
            val_to_compare = float(current_value)
            search_value = float(target_value)
        except:
            val_to_compare = current_value
            search_value = target_value

        if operation == "eq" and val_to_compare == search_value:
            result.append(row)
        elif operation == "gt" and val_to_compare > search_value:
            result.append(row)
        elif operation == "lt" and val_to_compare < search_value:
            result.append(row)
            
    return result


def main() -> None:
    args = parse_arguments()

    headers, rows = load_csv_data(args.source_file)

    if args.where:
        column, operation, value = parse_filter_condition(args.where)

        if column not in headers:
            print(f"Ошибка: колонка '{column}' отсутсвует в таблице")
            return

        rows = filter_records(rows, column, operation, value)

    if args.aggregate:
        column, operation = parse_aggregate_condition(args.aggregate)

        if column not in headers:
            print(f"Ошибка: колонка '{column}' отсутсвует в таблице")
            return

        try: 
            # Замена спискового включения:
            # numbers = []
            # for row in rows:
                # value = float(row[column])
                # numbers.append(value)
            numbers = [float(row[column]) for row in rows]
        except ValueError:
            print(f"Ошибка: колонка '{column}' содержит не числовые значения")
            return

        # if operation == "min":
        #     result = min(numbers)
        # elif operation == "max":
        #     result = max(numbers)
        # elif operation == "avg":
        #     result = sum(numbers) / len(numbers)
            
        result = AGGREGATIONS[operation](numbers)

        print(f"Результат вычисления ({operation}) по колонке '{column}': {result}")
        return

    clean_table = [[row[h] for h in headers] for row in rows]
    print(tabulate(clean_table, headers=headers, tablefmt="grid"))

    return

if __name__ == "__main__":
    main()