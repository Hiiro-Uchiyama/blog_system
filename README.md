## blog system

基本的なブログサイトを構築するためのプロジェクトです。

## コードの実行方法

`cd blog`でblogのディレクトリに移動し、`python manage.py runserver`を入力することでサーバーを立ち上げ、実行することが可能です。

## 詳細設定

```
pip install -r requirements.txt
createdb 〇〇
python manage.py makemigrations
python manage.py manage.py
```

上記はPostgresSQLのデータベースを作成し、ミグレーションを行うまでの流れです。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB名',
        'USER': 'PCのユーザー名',
        'PASSWORD': 'PCのパスワード',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
`settings.py`にある上記のコードに任意の変更を加えてください。

## 問題点

- タグ検索
- 検索機能
- 上位表示アルゴリズム

## 要件定義

- ブログサイトの基本的な機能の実装する

## 外部設計

- templatesとstaticに配置した静的ファイルを使用

## 内部設計

- PostgresSQLを採用
- django-summernoteを使用する
- ユーザーの作成は行わない
- templatesとstaticに表示画面のhtmlファイルやcssファイルを配置する
- detailにはSEO対策を行う

## 活用

- 個人ブログとしての活用
  - SEO対策の学習
  - Google Adsense

## 公式サイト

[公式サイト](https://landlim.com/ja/)

## 開発

> GithubのソースやWebサイトの情報を頼りに開発を行っています