from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# from sqlalchemy.orm import scoped_session, sessionmaker

# Engine の作成
Engine = create_engine(
    "sqlite:///migrations/db.sqlite",
    encoding="utf-8",
    echo=True
)

# セッションの作成
Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=True,
        bind=Engine))

Base = declarative_base()
# 予めテーブル定義の継承元クラスにqueryプロパティを仕込んでおく
Base.query = Session.query_property()
