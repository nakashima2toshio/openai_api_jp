# リポジトリガイドライン

## プロジェクト構成
- デモはリポジトリ直下: `a00_responses_api.py`（メイン）、`a01`〜`a06` 各機能デモ。共通: `a10_get_vsid.py`, `helper_api.py`, `helper_st.py`。
- リソース: `assets/`（スクショ）、`images/`（画像）、`data/`（サンプル）、`doc/`（文書）、`config.yml`（設定）。
- テスト: `tests/`（pytest、マーカーは `pytest.ini` を参照）。必要なら作成してください。

## ビルド・テスト・開発コマンド
- 環境構築: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- デモ起動（Streamlit）: `streamlit run a00_responses_api.py` （必要に応じて `--server.port=8501`）。他のデモも同様に起動可能。
- 品質チェック: `black *.py`、`flake8 *.py --max-line-length=120`、`mypy *.py --ignore-missing-imports`
- テスト: `pytest`、`pytest --cov=. --cov-report=html`、`pytest -m unit|integration|ui|functional|performance|slow|api`

## コーディング規約・命名
- Python 3.11+、4スペースインデント、目安120桁。型ヒントを推奨、Pydanticモデルを活用。
- 命名: ファイル/関数/変数は `snake_case`、クラスは `CamelCase`、定数は `UPPER_SNAKE_CASE`。デモは `aNN_description.py` パターンを踏襲。
- インポート時の副作用は避け、実行コードは `if __name__ == "__main__":` の下に配置。

## テスト方針
- フレームワーク: pytest。`tests/test_*.py`、クラス `Test*`、関数 `test_*`。
- `pytest.ini` のマーカー（例: `@pytest.mark.unit`, `@pytest.mark.integration`）を使用。
- ユニットテストは外部APIを直接呼ばない。I/Oは `responses`/`requests-mock` でモックし、`data/` のサンプルを利用。
- 実APIを叩く検証は `integration`（必要なら `slow` 併用）として任意実行に。

## コミット・プルリク
- コミットは命令形・現在形（例: "Add vision demo"）。小さく意味単位で分割し、意図が分かる説明を付与。
- PR には目的/背景/変更点、関連 Issue、影響範囲、UI変更のスクショやログを記載。
- 事前条件: テスト/リント/型チェックが通過し、影響するドキュメント（`README.md`/`doc/`）を更新。

## セキュリティと設定
- 秘密情報は環境変数で管理: `OPENAI_API_KEY`（必須）、任意で `OPENWEATHER_API_KEY`, `EXCHANGERATE_API_KEY`。`.env` を使う場合もコミット禁止。
- 資格情報・大容量バイナリ・生成物はコミットしない。設定は基本 `config.yml` に置き、環境変数で上書き可能に。

## エージェント向け注意
- 公開デモのエントリ（`a00`〜`a06`）の命名は維持。変更時は `README.md` の起動例も更新。
- `helper_api.py`/`helper_st.py` を変更した場合は、全デモの起動確認とインポート整合を徹底。
