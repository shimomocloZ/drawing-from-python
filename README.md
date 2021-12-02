# 商品購入抽選ロジック
## 仕様
- 購入できる商品が10個、購入対象者が5名存在する。
- 購入者は第1〜第10まで購入希望を出せる。
- 購入者一人あたりの商品購入の上限は2つまでとする。
- 購入者ごとの購入希望が重複する場合、購入数が少ない方を優先する。
- 購入数も同じ場合は、ランダムに決定する。
- 購入者が確定している商品は、次回以降の抽選時は抽選対象外となる。
- 抽選結果は`data`フォルダにJSON形式で出力される
## 環境準備

### 依存関係
- python 3.9

### 環境構築
1. pipenvをインストール
    ```bash
    pip install pipenv
    ```
1. 仮想環境を作成する
    ```bash
    pipenv install --python 3.9
    ```
1. 依存モジュールをインストールする
    ```bash
    pipenv install
    ```
1. DBをセットアップする
   ```bash
   pipenv run db:migrate
   ```
   1. DBをリセットする場合は書きを実行する
        ```bash
        pipenv run db:migrate:reset
        ```
1. データを投入する
   ```bash
   pipenv run db:seed
   ```

### 実行
1. 下記コマンドを実行する
    ```bash
    pipenv run start
    ```
