# 🔧 OpenAI API JP 開発環境セットアップガイド

## 📋 目次

1. [💻 システム要件](#💻-システム要件)
2. [🛠️ 開発環境構成](#🛠️-開発環境構成)
3. [⚙️ セットアップ手順](#⚙️-セットアップ手順)
4. [🔑 API キー設定](#🔑-api-キー設定)
5. [📦 依存関係インストール](#📦-依存関係インストール)
6. [🧪 動作確認](#🧪-動作確認)
7. [🚀 アプリケーション実行](#🚀-アプリケーション実行)
8. [🐛 トラブルシューティング](#🐛-トラブルシューティング)
9. [📚 開発ツール設定](#📚-開発ツール設定)

---

## 💻 システム要件

### 🔧 ハードウェア要件


| 項目           | 推奨スペック           | 最小要件            |
| -------------- | ---------------------- | ------------------- |
| **CPU**        | Apple Silicon M1 以上 |                     |
| **メモリ**     | 24GB+                  | 16GB                |
| **ストレージ** | SSD 100GB 以上         | SSD 50GB 以上       |
| **OS**         | macOS Ventura 13.0+    | macOS Big Sur 11.0+ |

### 🖥️ 確認済み環境

- **MacBook Air M2 24GBメモリ** ✅
- **macOS 14.6 (Sonoma)** ✅
- **Python 3.11+** ✅

---

## 🛠️ 開発環境構成

### 📋 基本構成


| 項目                     | ツール・サービス     | バージョン | 用途                  |
| ------------------------ | -------------------- | ---------- | --------------------- |
| **IDE**                  | PyCharm Professional | 最新版     | 統合開発環境          |
| **言語**                 | Python               | 3.11+      | メイン開発言語        |
| **AI API**               | OpenAI API           | API v1     | AIモデル呼び出し      |
| **AI API**               | Anthropic Claude API | API v1     | Claude Code統合       |
| **パッケージ管理**       | pip                  | 最新版     | Python パッケージ管理 |
| **テストフレームワーク** | pytest               | 最新版     | テスト実行            |
| **Webフレームワーク**    | Streamlit            | 1.44.0+    | デモアプリUI          |

### 🔗 API サービス構成


| サービス      | 契約レベル | API Tier | 主な用途                    |
| ------------- | ---------- | -------- | --------------------------- |
| **OpenAI**    | Pro契約    | Tier 3   | GPT-4o, o1, DALL-E, TTS/STT |
| **Anthropic** | Pro契約    | Tier 2   | Claude 3.5, Claude Code     |

---

## ⚙️ セットアップ手順

### 1️⃣ **プロジェクトクローン・移動**

```bash
# GitHubからプロジェクトをクローン
git clone https://github.com/nakashima2toshio/openai_api_jp.git

# プロジェクトディレクトリに移動
cd openai_api_jp

# プロジェクト構造確認
ls -la

# リモートリポジトリ確認
git remote -v
```

#### 📋 **プロジェクト概要**
- **プロジェクト名**: OpenAI API - 基本・応用
- **GitHubリポジトリ**: [openai_api_jp](https://github.com/nakashima2toshio/openai_api_jp)
- **目的**: OpenAI APIの包括的な学習・デモアプリケーション
- **言語**: Python (Streamlit)

### 2️⃣ **Python仮想環境作成（推奨）**

```bash
# Python仮想環境作成
python3 -m venv venv

# 仮想環境アクティベート (macOS/Linux)
source venv/bin/activate

# 仮想環境確認
which python
python --version
```

### 3️⃣ **システム依存関係（macOS特有）**

```bash
# Homebrew インストール（未インストールの場合）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 音声処理用ライブラリ（PyAudio用）
brew install portaudio

# その他システムライブラリ
brew install ffmpeg  # 音声フォーマット変換用
brew install git     # バージョン管理
```

---

## 🔑 API キー設定

### 📝 環境変数設定

```bash
# ~/.zshrc または ~/.bash_profile に追加
export OPENAI_API_KEY='sk-proj-your-openai-api-key-here'
export ANTHROPIC_API_KEY='sk-ant-your-anthropic-api-key-here'

# オプション: 外部API（天気予報等）
export OPENWEATHER_API_KEY='your-openweather-api-key'
export EXCHANGERATE_API_KEY='your-exchangerate-api-key'

# 環境変数読み込み
source ~/.zshrc
```

### 🔐 環境変数確認

```bash
# API キー設定確認（セキュリティのため一部マスク表示）
echo $OPENAI_API_KEY | sed 's/\(sk-proj-....\).*/\1***/'
echo $ANTHROPIC_API_KEY | sed 's/\(sk-ant-....\).*/\1***/'
```

### 📄 .env ファイル（代替方法）

```bash
# プロジェクトルートに .env ファイル作成
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
OPENWEATHER_API_KEY=your-openweather-api-key
EXCHANGERATE_API_KEY=your-exchangerate-api-key
EOF

# セキュリティのため .env をgitignore追加
echo ".env" >> .gitignore
```

---

## 📦 依存関係インストール

### 🚀 基本インストール

```bash
# Python依存関係インストール
pip install --upgrade pip
pip install -r requirements.txt
```

### 🎤 音声処理依存関係（重要）

```bash
# PyAudio インストール（音声処理に必須）
pip install PyAudio

# 音声処理確認
python -c "import pyaudio; print('PyAudio OK')"
python -c "import simpleaudio; print('SimpleAudio OK')"
```

### ⚡ 高速化オプション（M2 Mac用）

```bash
# Apple Silicon最適化版TensorFlow/PyTorch
pip install --upgrade tensorflow-macos tensorflow-metal
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 🧪 開発用追加ツール

```bash
# 開発・テスト用ツール
pip install pytest pytest-cov pytest-mock
pip install black flake8 mypy  # コード品質
pip install jupyter notebook   # データ分析用
```

---

## 🧪 動作確認

### 1️⃣ **基本設定テスト**

```bash
# Python動作確認
python -c "
import sys
print(f'Python: {sys.version}')
import openai
print(f'OpenAI SDK: {openai.__version__}')
import streamlit as st
print(f'Streamlit: {st.__version__}')
"
```

### 2️⃣ **API接続テスト**

```bash
# OpenAI API接続テスト
python -c "
import openai
import os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    response = client.models.list()
    print('✅ OpenAI API接続成功')
    print(f'利用可能モデル数: {len(response.data)}')
except Exception as e:
    print(f'❌ OpenAI API接続失敗: {e}')
"
```

### 3️⃣ **設定ファイル確認**

```bash
# config.yml 読み込みテスト
python -c "
import yaml
with open('config.yml') as f:
    config = yaml.safe_load(f)
    print('✅ config.yml読み込み成功')
    print(f'デフォルトモデル: {config[\"models\"][\"default\"]}')
    print(f'利用可能モデル数: {len(config[\"models\"][\"available\"])}')
"
```

### 4️⃣ **音声処理テスト**

```bash
# 音声ライブラリテスト
python -c "
try:
    import pyaudio
    print('✅ PyAudio OK')
except ImportError:
    print('❌ PyAudio インストール必要')

try:
    import simpleaudio
    print('✅ SimpleAudio OK') 
except ImportError:
    print('❌ SimpleAudio インストール必要')
"
```

---

## 🚀 アプリケーション実行

### 🎯 個別デモアプリ実行

```bash
# メイン統合デモ（推奨起動）
streamlit run a00_responses_api.py --server.port=8501

# 構造化出力デモ
streamlit run a01_structured_outputs_parse_schema.py --server.port=8501

# ツール・Pydantic連携デモ
streamlit run a02_responses_tools_pydantic_parse.py --server.port=8502

# 画像・ビジョンデモ
streamlit run a03_images_and_vision.py --server.port=8503

# 音声処理デモ
streamlit run a04_audio_speeches.py --server.port=8504

# 会話状態管理デモ
streamlit run a05_conversation_state.py --server.port=8505

# 推論・思考の連鎖デモ
streamlit run a06_reasoning_chain_of_thought.py --server.port=8506
```

### 🌐 アクセスURL

アプリケーション起動後、ブラウザで以下URLにアクセス：

- **統合デモ**: http://localhost:8501
- **構造化出力**: http://localhost:8501
- **ツール連携**: http://localhost:8502
- **画像・ビジョン**: http://localhost:8503
- **音声処理**: http://localhost:8504
- **会話状態管理**: http://localhost:8505
- **推論・CoT**: http://localhost:8506

### 📱 複数デモ同時実行

```bash
# ターミナル分割で複数デモ同時起動
# Terminal 1
streamlit run a00_responses_api.py --server.port=8501

# Terminal 2  
streamlit run a04_audio_speeches.py --server.port=8504

# Terminal 3
streamlit run a03_images_and_vision.py --server.port=8503
```

---

## 🐛 トラブルシューティング

### ❌ よくあるエラーと対処法

#### 🔑 **API認証エラー**

```bash
# エラー例: "Incorrect API key provided"
❌ Error: Incorrect API key provided

# 対処法:
✅ API キー再確認
echo $OPENAI_API_KEY
✅ 環境変数再読み込み
source ~/.zshrc
✅ APIキー権限確認（OpenAI Dashboard）
```

#### 🎤 **音声処理エラー**

```bash
# エラー例: "No module named 'pyaudio'"
❌ ModuleNotFoundError: No module named 'pyaudio'

# 対処法:
✅ システムライブラリ確認
brew install portaudio
✅ PyAudio再インストール  
pip uninstall PyAudio
pip install PyAudio
```

#### 💾 **メモリエラー（大量データ処理時）**

```bash
# エラー例: "RuntimeError: resource exhausted"
❌ RuntimeError: resource exhausted (memory)

# 対処法:
✅ バッチサイズ削減
✅ 不要プロセス停止
✅ Streamlitアプリ再起動
```

#### 🌐 **ネットワーク・プロキシエラー**

```bash
# エラー例: "Connection timeout"
❌ requests.exceptions.ConnectTimeout

# 対処法:
✅ ネットワーク接続確認
ping api.openai.com
✅ プロキシ設定確認
env | grep -i proxy
✅ ファイアウォール設定確認
```

### 🔧 **環境リセット**

```bash
# 完全リセット手順
# 1. 仮想環境削除・再作成
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate

# 2. 依存関係再インストール
pip install --upgrade pip
pip install -r requirements.txt

# 3. 設定確認
python -c "import openai; print('OK')"
```

---

## 📚 開発ツール設定

### 🔬 **PyCharm Professional設定**

#### 🛠️ プロジェクト設定

```
File → Settings (⌘,) で以下を設定:

📁 Project Structure:
  - Source Folders: プロジェクトルート
  - Excluded Folders: venv/, __pycache__/, .pytest_cache/

🐍 Python Interpreter:
  - 仮想環境のPython選択: venv/bin/python

🧪 Test Runner:
  - Default test runner: pytest
  - Working directory: プロジェクトルート

🎨 Code Style:
  - Python: PEP 8準拠
  - Line length: 120
  - Auto-format: Black使用
```

#### 🚀 Run Configuration設定

```
Streamlitアプリ用Run Configuration作成:

Name: Streamlit Main Demo
Script path: a00_responses_api.py  
Module: streamlit
Parameters: run $FilePath$ --server.port=8501
Working directory: プロジェクトルート
Environment variables: OPENAI_API_KEY=xxx
```

### 🧪 **pytest設定**

```bash
# テスト実行（全テスト）
pytest

# 詳細出力
pytest -v

# カバレッジ付き実行
pytest --cov=. --cov-report=html

# マーカー別実行
pytest -m unit        # 単体テストのみ
pytest -m integration # 統合テストのみ
pytest -m slow        # 重いテストのみ
```

### 📊 **コード品質ツール**

```bash
# Black（自動フォーマット）
black *.py helper_*.py

# Flake8（コード品質チェック）
flake8 *.py --max-line-length=120

# mypy（型チェック）
mypy *.py --ignore-missing-imports

# すべて一括実行
black *.py && flake8 *.py --max-line-length=120 && mypy *.py --ignore-missing-imports
```

### 📈 **パフォーマンス監視**

```bash
# メモリ使用量監視
pip install memory-profiler
@profile デコレータでプロファイリング

# Streamlit開発サーバー監視
streamlit run app.py --server.runOnSave=true
```

---

## 📋 セットアップチェックリスト

### ✅ **必須セットアップ項目**

- [ ]  **Python 3.11+** インストール確認
- [ ]  **仮想環境** 作成・アクティベート
- [ ]  **requirements.txt** 依存関係インストール
- [ ]  **OpenAI API Key** 環境変数設定
- [ ]  **Anthropic API Key** 環境変数設定
- [ ]  **PyAudio** 音声ライブラリインストール
- [ ]  **config.yml** 設定ファイル確認
- [ ]  **API接続テスト** 成功確認
- [ ]  **デモアプリ** 最低1つ起動確認

### 🔧 **推奨セットアップ項目**

- [ ]  **PyCharm Professional** プロジェクト設定
- [ ]  **pytest** テスト環境構築
- [ ]  **Black/Flake8** コード品質ツール設定
- [ ]  **外部API Key**（天気・為替等）設定
- [ ]  **Jupyter Notebook** データ分析環境
- [ ]  **Git設定** バージョン管理
- [ ]  **プロキシ・ファイアウォール** ネットワーク設定確認

### 🚀 **最終動作確認**

- [ ]  **統合デモ** (a00_responses_api.py) 起動・操作確認
- [ ]  **音声デモ** (a04_audio_speeches.py) TTS/STT動作確認
- [ ]  **画像デモ** (a03_images_and_vision.py) 画像処理確認
- [ ]  **API使用量** OpenAI/Anthropic Dashboard確認
- [ ]  **エラーログ** 正常動作確認

---

## 🎉 セットアップ完了

すべての項目が完了したら、OpenAI APIのデモアプリケーション開発環境が整いました！

### 🚀 次のステップ

1. **[統合デモアプリ実行](http://localhost:8501)** - まずはメインデモで全機能体験
2. **[設計書確認](/doc/)** - 各機能の詳細仕様理解
3. **[コード解析](a00_responses_api.py)** - 実装パターン学習
4. **[独自機能開発](#)** - オリジナル機能追加

### 📞 サポート

セットアップで問題が発生した場合：

1. **[トラブルシューティング](#🐛-トラブルシューティング)** を確認
2. **エラーメッセージをコピー** してデバッグ情報収集
3. **環境情報を整理**（OS、Python、依存関係バージョン）
4. **GitHubイシュー作成** または **開発者に相談**

---

**🎯 Happy Coding with OpenAI APIs! 🚀**
