# -*- coding: utf-8 -*-
import csv


def read_csv(file_path: str):
    with open(file_path, 'r', encoding='utf8', newline='') as f:
        reader = csv.DictReader(f)
        result = [row for row in reader]

    return result
