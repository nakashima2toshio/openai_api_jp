# CLAUDE_JP.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリのコードを扱う際のガイダンスを日本語で提供します。

## プロジェクト概要

このプロジェクトは、対話的なStreamlitデモを通してOpenAI APIの機能を学習するための教育用Pythonアプリケーションです。テキスト生成、構造化出力、関数呼び出し、画像・ビジョン処理、音声処理、会話管理など、OpenAI APIの包括的な機能を実演します。

## 開発コマンド

### 各デモの実行
```bash
# メイン統合デモ（ポート8501）
streamlit run a00_responses_api.py --server.port=8501

# 構造化出力デモ
streamlit run a01_structured_outputs_parse_schema.py --server.port=8501

# ツール・Pydantic解析（ポート8502）
streamlit run a02_responses_tools_pydantic_parse.py --server.port=8502

# 画像・ビジョン（ポート8503）
streamlit run a03_images_and_vision.py --server.port=8503

# 音声処理（ポート8504）
streamlit run a04_audio_speeches.py --server.port=8504

# 会話状態管理（ポート8505）
streamlit run a05_conversation_state.py --server.port=8505

# 思考連鎖推論（ポート8506）
streamlit run a06_reasoning_chain_of_thought.py --server.port=8506

# Vector Store ID管理ユーティリティ
python a10_get_vsid.py
```

### テスト実行
```bash
# 全テスト実行
pytest

# 詳細出力付き実行
pytest -v

# マーカーを使った特定テスト種別の実行
pytest -m unit        # 単体テストのみ
pytest -m integration # 統合テストのみ
pytest -m api         # APIテストのみ
pytest -m slow        # 長時間実行テストのみ
```

### セットアップ
```bash
# 依存関係インストール
pip install -r requirements.txt

# 必須環境変数
export OPENAI_API_KEY='your-openai-api-key'

# 拡張機能用のオプション APIキー
export OPENWEATHER_API_KEY='your-openweather-api-key'
export EXCHANGERATE_API_KEY='your-exchangerate-api-key'
```

## アーキテクチャ

### 主要エントリーポイント
- **a00_responses_api.py** - 全OpenAI機能を統合したメインデモ
- **a01_structured_outputs_parse_schema.py** - スキーマ検証付き構造化出力
- **a02_responses_tools_pydantic_parse.py** - Pydanticベースの解析と関数呼び出し
- **a03_images_and_vision.py** - 画像生成とビジョンAPIのデモンストレーション
- **a04_audio_speeches.py** - テキスト読み上げ、転写、リアルタイム音声
- **a05_conversation_state.py** - `previous_response_id`を使った会話状態管理
- **a06_reasoning_chain_of_thought.py** - 思考連鎖推論パターン

### ユーティリティスクリプト
- **a10_get_vsid.py** - Vector Store ID管理ユーティリティ
- **get_cities_list.py** - 天気APIのための都市リストデータ処理

### ヘルパーモジュール

**helper_api.py** にはAPI機能の中核が含まれています：
- `ConfigManager` - 設定ファイル処理とモデル管理
- `MessageManager` - メッセージ履歴と会話状態
- `TokenManager` - トークン計算とコスト算出
- `ResponseProcessor` - レスポンス解析とエラー処理
- `OpenAIClient` - 統一OpenAI APIクライアントラッパー

**helper_st.py** はStreamlit UIコンポーネントを提供：
- `UIHelper` - 共通UI要素作成
- `SessionStateManager` - Streamlitセッション状態管理
- `ResponseProcessorUI` - レスポンス表示とフォーマット
- `InfoPanelManager` - 情報パネル作成

### 設定システム
- **config.yml** - モデル定義、価格設定、サンプルデータを含む中央設定ファイル
- 全OpenAIモデルカテゴリに対応：フロンティア（GPT-5）、推論（o3/o4）、標準（GPT-4o）、ビジョン、音声、リアルタイム、画像生成、検索モデル
- APIキーと外部サービス設定用の環境変数サポート

### デモンストレーションする主要機能
- OpenAI APIの包括的カバー（テキスト、構造化出力、関数呼び出し、ビジョン、音声）
- Pydanticモデル検証と解析
- ファイル検索用Vector Store統合
- Web検索ツール統合
- `previous_response_id`による会話状態管理
- リアルタイム音声処理
- マルチモーダル入力処理（テキスト、画像、音声）
- 思考連鎖推論パターン
- 外部API統合（OpenWeatherMap、Exchange Rate API）
- Vector Store管理ユーティリティ

## 開発上の注意事項

- 全ドキュメントとコメントは日本語で記述
- 対話的なWebインターフェース用にStreamlitを使用
- 包括的なエラーハンドリングを含むモジュラー設計
- 詳細なAPI使用例を含む教育重視
- 並行テスト用に各デモが異なるポートで動作
- `/data`と`/images`ディレクトリにサンプルデータファイルを含む
- カスタムマーカーによる複数テストタイプをサポートするテスト設定
- `/utils`ディレクトリに各種ヘルパー機能
- `/doc`ディレクトリに詳細なmarkdownドキュメント
- `/assets`ディレクトリにUIスクリーンショットとサンプル画像

## プロジェクト構造

```
├── a00_responses_api.py           # メイン統合デモ
├── a01-a06_*.py                   # 個別機能デモ
├── a10_get_vsid.py                # Vector Storeユーティリティ
├── helper_api.py                  # 中核API機能
├── helper_st.py                   # Streamlit UIヘルパー
├── config.yml                     # 中央設定ファイル
├── requirements.txt               # Python依存関係
├── pytest.ini                     # テスト設定
├── data/                          # サンプルデータファイル
├── images/                        # サンプル画像
├── assets/                        # UIアセットとスクリーンショット
├── doc/                           # ドキュメント
└── utils/                         # ユーティリティスクリプト
```