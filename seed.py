# -*- coding: utf-8 -*-
import os

from sqlalchemy_seed import (create_table, drop_table,  # noqa E401
                             load_fixture_files, load_fixtures)

from migrations.setting import Session


def main():
    path = os.path.join('migrations', 'seeds', 'fixtures')
    fixtures = load_fixture_files(
        path, ['products.yaml', 'wishlists.yaml', 'buyers.yaml'])
    load_fixtures(Session, fixtures)


if __name__ == '__main__':
    main()
