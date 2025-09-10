# 🚀 OpenAI API From Scratch with Streamlit
- If you prefer English, please use translation tools like Google Translate to read the English version.

## OpenAI APIを基礎から応用まで体系的に学習するための包括的チュートリアル
##### 主要なOpenAI APIは網羅しています、
- プログラム数（9個）
- サブプログラム数（59個）
## OpenAI API -> Anthropic API のマイグレーション：仕様書
[OpenAPAPI->Anthropic API migration 仕様書]
[Migration](doc/openai_to_anthropic_migration_spec.md)


## 🔗 関連プロジェクト## 🔗 関連プロジェクト
| プロジェクト                                                             | 説明                                         | ステータス |
| ------------------------------------------------------------------------ | -------------------------------------------- | ---------- |
| [openai_api_jp](https://github.com/nakashima2toshio/openai_api_jp)       | OpenAI API完全ガイド（本プロジェクト）       | ✅ 公開中  |
| [anthropic_api_jp](https://github.com/nakashima2toshio/anthropic_api_jp) | Anthropic Claude API活用                     | ✅ 公開中  |
| [openai_rag_jp](https://github.com/nakashima2toshio/openai_rag_jp)       | RAG実装パターン集（cloud版、Local-Qdrant版） | ✅ 公開中  |
| [openai_mcp_jp](https://github.com/nakashima2toshio/openai_mcp_jp)       | MCP(Model Context Protocol)実装              | 🚧 整備中  |
| [openai_django_jp](https://github.com/nakashima2toshio/openai_django_jp) | OpenAI API + Django実装                      | ✅ 公開中  |
| [openai_agent_jp](https://github.com/nakashima2toshio/openai_agent_jp)   | AIエージェント構築                           | 📝 作成中  |

---

## 📚 プロジェクト概要

**OpenAI API JP**は、OpenAI APIの全機能を体系的に学習できるプロジェクトです。基本的なテキスト生成から最新のマルチモーダル処理まで、実践的なデモアプリケーションを通じて段階的に習得できます。

### 🎯 学習目標

- **基礎理解**: OpenAI APIの基本概念とプログラミングパターン
- **実践スキル**: Streamlitを使った対話型アプリケーション開発
- **応用技術**: 構造化出力、関数呼び出し、マルチモーダル処理
- **最新機能**: Chain-of-Thought推論、Realtime API、Vector Store統合

---

## 🏗️ プログラム構成

### 📋 プログラム一覧


| 区分               | プログラム                               | 説明                           |
| ------------------ | ---------------------------------------- | ------------------------------ |
| **OpenAI API**     | `a00_responses_api.py`                   | メイン統合デモ - 全機能を網羅  |
| **OpenAI API**     | `a01_structured_outputs_parse_schema.py` | 構造化出力とスキーマ検証       |
| **OpenAI API**     | `a02_responses_tools_pydantic_parse.py`  | Pydanticベースの関数呼び出し   |
| **OpenAI API**     | `a03_images_and_vision.py`               | 画像生成とビジョンAPI          |
| **OpenAI API**     | `a04_audio_speeches.py`                  | 音声処理（TTS/STT/翻訳）       |
| **OpenAI API**     | `a05_conversation_state.py`              | 会話状態管理                   |
| **OpenAI API**     | `a06_reasoning_chain_of_thought.py`      | Chain-of-Thought推論パターン   |
| **ユーティリティ** | `a10_get_vsid.py`                        | Vector Store ID管理            |
| **ユーティリティ** | `get_cities_list.py`                     | 都市リストデータ処理           |
| **共通モジュール** | `helper_api.py`                          | API操作の中核機能              |
| **共通モジュール** | `helper_st.py`                           | Streamlit UI共通コンポーネント |

---

## 📊 各プログラムの詳細とコード例

### 🎯 a00_responses_api.py - メイン統合デモ

#### サブプログラム（クラス／デモ）一覧


| クラス／関数                | 概要                             |
| --------------------------- | -------------------------------- |
| `BaseDemo`                  | デモ機能の基底クラス（統一化版） |
| `TextResponseDemo`          | 基本テキスト応答                 |
| `MemoryResponseDemo`        | 会話履歴付き応答                 |
| `ImageResponseDemo`         | 画像入力（URL・Base64対応）      |
| `StructuredOutputDemo`      | 構造化出力（create・parse対応）  |
| `WeatherDemo`               | OpenWeatherMap API 連携          |
| `FileSearchVectorStoreDemo` | FileSearch 専用                  |
| `WebSearchToolsDemo`        | WebSearch 専用                   |
| `DemoManager`               | デモ統合管理・実行制御           |

<details>
<summary><b>💻 コード例</b></summary>

#### TextResponseDemo - 基本テキスト応答

```python
messages = get_default_messages()
messages.append(
    EasyInputMessageParam(role="user", content=user_input)
)

# 統一されたAPI呼び出し（temperatureパラメータ対応）
response = self.call_api_unified(messages, temperature=temperature)
　┗ api_params = {
    "input": messages,
    "model": model
    }
    self.client.responses.create(**params)
ResponseProcessorUI.display_response(response)
```

#### MemoryResponseDemo - 会話履歴付き応答

```python
# 1回目: 初回質問
messages = get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=user_input_1))
response_1 = self.call_api_unified(messages, temperature=temperature)

# 2回目以降: 履歴 + 新しい質問
messages.append(EasyInputMessageParam(role="assistant", content=response_1_text))
messages.append(EasyInputMessageParam(role="user", content=user_input_2))
response_2 = self.call_api_unified(messages, temperature=temperature)
```

#### ImageResponseDemo - 画像入力対応

```python
messages = get_default_messages()
messages.append(
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(type="input_text", text=question),
            ResponseInputImageParam(
                type="input_image",
                image_url=image_url,
                detail="auto"
            ),
        ],
    )
)
response = self.call_api_unified(messages, temperature=temperature)
```

#### FileSearchVectorStoreDemo - ファイル検索

```python
# FileSearchツールパラメータの作成
fs_tool = FileSearchToolParam(
    type="file_search",
    vector_store_ids=[vector_store_id],
    max_num_results=max_results
)
messages = get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=query))

response = self.call_api_unified(messages, tools=[fs_tool])
```

</details>

---

### 📝 a01_structured_outputs_parse_schema.py - 構造化出力

#### サブプログラム（クラス／デモ）一覧


| クラス／関数            | 概要                             |
| ----------------------- | -------------------------------- |
| `BaseDemo`              | デモ機能の基底クラス（統一化版） |
| `EventExtractionDemo`   | イベント情報抽出デモ             |
| `MathReasoningDemo`     | 数学的思考ステップデモ           |
| `UIGenerationDemo`      | UI コンポーネント生成デモ        |
| `EntityExtractionDemo`  | エンティティ抽出デモ             |
| `ConditionalSchemaDemo` | 条件分岐スキーマデモ             |
| `ModerationDemo`        | モデレーション＆拒否処理デモ     |
| `DemoManager`           | デモの管理クラス（統一化版）     |

<details>
<summary><b>💻 コード例</b></summary>

#### EventExtractionDemo - イベント情報抽出

```python
# Pydanticモデル定義
class EventInfo(BaseModel):
    name: str = Field(..., description="イベント名")
    date: str = Field(..., description="開催日")
    participants: List[str] = Field(..., description="参加者一覧")

# responses.parse API呼び出し
response = self.call_api_parse(
    input_text=user_text,
    text_format=EventInfo,
    temperature=temperature
)
event_info = response.output_parsed
```

#### MathReasoningDemo - 数学的思考ステップ

```python
# Pydanticモデル定義
class Step(BaseModel):
    explanation: str = Field(..., description="このステップでの説明")
    output: str = Field(..., description="このステップの計算結果")

class MathReasoning(BaseModel):
    steps: List[Step] = Field(..., description="逐次的な解法ステップ")
    final_answer: str = Field(..., description="最終解")

# responses.parse API呼び出し
prompt = f"Solve the equation {expression} step by step..."
response = self.call_api_parse(
    input_text=prompt,
    text_format=MathReasoning,
    temperature=temperature
)
```

</details>

---

### 🛠️ a02_responses_tools_pydantic_parse.py - 関数呼び出し

#### サブプログラム（クラス／デモ）一覧


| クラス／関数                      | 概要                             |
| --------------------------------- | -------------------------------- |
| `BaseDemo`                        | デモ機能の基底クラス             |
| `BasicFunctionCallDemo`           | 基本的な function call のデモ    |
| `MultipleToolsDemo`               | 複数ツール登録・複数関数呼び出し |
| `AdvancedMultipleToolsDemo`       | 高度な複数ツール呼び出し         |
| `NestedStructureDemo`             | 入れ子構造のデモ                 |
| `EnumTypeDemo`                    | Enum 型のデモ                    |
| `NaturalTextStructuredOutputDemo` | 自然文での構造化出力             |
| `SimpleDataExtractionDemo`        | シンプルなデータ抽出             |
| `MultipleEntityExtractionDemo`    | 複数エンティティ抽出             |
| `ComplexQueryDemo`                | 複雑なクエリパターン             |
| `DynamicEnumDemo`                 | 動的な列挙型                     |
| `ChainOfThoughtDemo`              | 思考の連鎖デモ                   |
| `ConversationHistoryDemo`         | 会話履歴デモ                     |
| `DemoManager`                     | デモ管理クラス                   |

<details>
<summary><b>💻 コード例</b></summary>

#### BasicFunctionCallDemo - 基本的な Function Call

```python
class WeatherRequest(BaseModel):
    city: str
    date: str

class NewsRequest(BaseModel):
    topic: str
    date: str

response = self.client.responses.parse(
    model=model,
    input=messages,
    tools=[
        pydantic_function_tool(WeatherRequest),
        pydantic_function_tool(NewsRequest)
    ]
)
```

#### SimpleDataExtractionDemo - シンプルなデータ抽出

```python
class PersonInfo(BaseModel):
    name: str
    age: int

messages = self.get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=user_input))

response = self.client.responses.parse(
    model=model,
    input=messages,
    text_format=PersonInfo
)
```

</details>

---

### 🎨 a03_images_and_vision.py - 画像処理

#### サブプログラム（クラス／デモ）一覧


| クラス／関数            | 概要                         |
| ----------------------- | ---------------------------- |
| `BaseDemo`              | ベースデモクラス（統一化版） |
| `URLImageToTextDemo`    | URL 画像からテキスト生成     |
| `Base64ImageToTextDemo` | Base64 画像からテキスト生成  |
| `PromptToImageDemo`     | プロンプトから画像生成       |
| `DemoManager`           | デモ管理クラス（統一化版）   |

<details>
<summary><b>💻 コード例</b></summary>

#### URLImageToTextDemo - URL画像からテキスト生成

```python
# 画像URLからテキスト生成の実装例
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam, ResponseInputTextParam, ResponseInputImageParam

client = OpenAI()
messages = [
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(type="input_text", text="この画像を日本語で説明してください"),
            ResponseInputImageParam(type="input_image", image_url=image_url, detail="auto")
        ]
    )
]

response = client.responses.create(model=model, input=messages)
```

#### PromptToImageDemo - プロンプトから画像生成

```python
# DALL-E画像生成の実装例
from openai import OpenAI

client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt="美しい日本庭園の風景、桜の花が咲いている、静かな池、石灯籠、写実的なスタイル",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
```

</details>

---

### 🎤 a04_audio_speeches.py - 音声処理

#### サブプログラム（クラス／デモ）一覧


| クラス／関数            | 概要                                   |
| ----------------------- | -------------------------------------- |
| `BaseDemo`              | デモ機能の基底クラス（音声用統一化版） |
| `TextToSpeechDemo`      | Text to Speech API のデモ              |
| `SpeechToTextDemo`      | Speech to Text API のデモ              |
| `SpeechTranslationDemo` | Speech Translation API のデモ          |
| `RealtimeApiDemo`       | Realtime API のデモ                    |
| `ChainedVoiceAgentDemo` | Chained Voice Agent のデモ             |
| `AudioDemoManager`      | 音声デモの管理クラス（統一化版）       |

> 注: a04_audio_speeches.py では `st.expander` 内に `st.code` ブロックが見つかりませんでした。このファイルは音声処理を中心に実装されています。

---

### 💬 a05_conversation_state.py - 会話状態管理

#### サブプログラム（クラス／デモ）一覧


| クラス／関数               | 概要                         |
| -------------------------- | ---------------------------- |
| `BaseDemo`                 | ベースデモクラス（統一化版） |
| `StatefulConversationDemo` | ステートフルな会話継続デモ   |
| `WebSearchParseDemo`       | Web 検索と構造化パース       |
| `FunctionCallingDemo`      | Function Calling デモ        |
| `DemoManager`              | デモ管理クラス（統一化版）   |

<details>
<summary><b>💻 コード例</b></summary>

#### StatefulConversationDemo - ステートフルな会話継続

```python
# ステートフルな会話継続の実装例
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam, ResponseInputTextParam

client = OpenAI()

# 初回質問
initial_response = client.responses.create(
    model=model,
    input=[
        EasyInputMessageParam(
            role="user",
            content=[
                ResponseInputTextParam(
                    type="input_text", 
                    text="OpenAI APIの使い方を教えて"
                )
            ]
        )
    ]
)

# 会話の継続（previous_response_idを使用）
follow_up_response = client.responses.create(
    model=model,
    input="具体的なコード例も教えて",
    previous_response_id=initial_response.id
)
```

#### WebSearchParseDemo - Web検索と構造化パース

```python
# Web検索と構造化パースの実装例
from openai import OpenAI
from openai.types.responses import WebSearchToolParam
from pydantic import BaseModel, Field

client = OpenAI()

# Web検索の実行
tool = {"type": "web_search_preview"}
search_response = client.responses.create(
    model=model,
    input="最新のOpenAI APIの情報は？",
    tools=[tool]
)

# 構造化パースのためのスキーマ定義
class APIInfo(BaseModel):
    title: str = Field(..., description="記事のタイトル")
    url: str = Field(..., description="記事のURL")

# 構造化パース実行
structured_response = client.responses.parse(
    model="gpt-4.1",
    input="上の回答をtitleとurlだけJSON で返して",
    previous_response_id=search_response.id,
    text_format=APIInfo
)
```

</details>

---

### 🧠 a06_reasoning_chain_of_thought.py - 推論パターン

#### サブプログラム（クラス／デモ）一覧


| クラス／関数              | 概要                               |
| ------------------------- | ---------------------------------- |
| `BaseDemo`                | ベースデモクラス（統一化版）       |
| `StepByStepReasoningDemo` | 段階的推論（Step-by-Step）         |
| `HypothesisTestDemo`      | 仮説検証推論                       |
| `TreeOfThoughtDemo`       | 思考の木（Tree of Thought）        |
| `ProsConsDecisionDemo`    | 賛否比較決定（Pros-Cons-Decision） |
| `PlanExecuteReflectDemo`  | 計画→実行→振り返り               |
| `DemoManager`             | デモ管理クラス（統一化版）         |

<details>
<summary><b>💻 コード例</b></summary>

#### StepByStepReasoningDemo - 段階的推論

```python
# Step-by-Step 推論の実装例
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam, ResponseInputTextParam

client = OpenAI()

system_prompt = '''あなたは段階的に問題を解く methodical なチューターです。
質問が与えられたら：
1. 問題を明確で順序立ったステップに分解してください
2. 各ステップに番号を付けてください（Step 1:, Step 2: など）
3. 作業を明確に示してください
4. 最後に "Answer:" に続けて最終的な答えを記載してください
5. 解答の信頼度を0-1で評価してください

推論において正確で論理的にしてください。'''

messages = [
    EasyInputMessageParam(role="system", content=system_prompt),
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(
                type="input_text", 
                text="2X + 1 = 5のとき、Xはいくつ？"
            )
        ]
    )
]

response = client.responses.create(model=model, input=messages)
```

#### TreeOfThoughtDemo - 思考の木

```python
# Tree of Thought 推論の実装例
system_prompt = '''あなたはTree-of-Thoughts探索を実行するAIです。
体系的な分岐推論で問題を解決します。

各問題に対して：
1. 各ステップで複数の候補思考を生成（分岐）
2. 各分岐を0-1のスコアで評価
3. 有望な分岐をさらなる探索のために選択
4. 探索ツリー構造を追跡
5. 解決への最適パスを特定'''

messages = [
    EasyInputMessageParam(role="system", content=system_prompt),
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(
                type="input_text", 
                text="Goal: 4, 9, 10, 13 の数字を使って24を作る（四則演算のみ使用）"
            )
        ]
    )
]

response = client.responses.create(model=model, input=messages)
```

</details>

---

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/nakashima2toshio/openai_api_jp.git
cd openai_api_jp

# Python仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. API キーの設定

```bash
# 環境変数の設定
export OPENAI_API_KEY='sk-proj-your-openai-api-key'

# オプション: 外部API（天気・為替）
export OPENWEATHER_API_KEY='your-key'
export EXCHANGERATE_API_KEY='your-key'
```

### 3. デモアプリの実行

```bash
# メイン統合デモ（推奨）
streamlit run a00_responses_api.py --server.port=8501

# その他のデモ（個別実行）
streamlit run a01_structured_outputs_parse_schema.py --server.port=8502
streamlit run a03_images_and_vision.py --server.port=8503
```

📖 **詳細なセットアップ手順**: [README_setup.md](README_setup.md)

---

## 🎯 学習ロードマップ

### 🌱 **Phase 1: 基礎習得** (1-2週間)

1. **環境構築**: README_setup.mdに従ってセットアップ
2. **基本理解**: a0_simple_api.ipynb でAPI基礎を学習
3. **統合デモ体験**: a00_responses_api.py で全機能を俯瞰

### 🚀 **Phase 2: 機能別習得** (2-3週間)

1. **構造化出力**: a01でスキーマ定義とバリデーション
2. **関数呼び出し**: a02でPydantic統合とツール連携
3. **マルチモーダル**: a03-a04で画像・音声処理

### 🎓 **Phase 3: 実践応用** (3-4週間)

1. **状態管理**: a05で会話コンテキストの永続化
2. **推論パターン**: a06でChain-of-Thought実装
3. **独自実装**: 学んだパターンを組み合わせてオリジナル機能開発

---

## 🔧 開発環境とツール

### 推奨環境

- **OS**: macOS 13+ / Ubuntu 22.04+ / Windows 11 with WSL2
- **Python**: 3.11 以上
- **メモリ**: 16GB以上推奨
- **IDE**: PyCharm Professional / VS Code with Python拡張

### テスト実行

```bash
# 全テスト実行
pytest

# カバレッジ付きテスト
pytest --cov=. --cov-report=html

# 特定マーカーのテスト
pytest -m unit        # 単体テストのみ
pytest -m integration # 統合テストのみ
```

### コード品質管理

```bash
# フォーマット
black *.py

# リント
flake8 *.py --max-line-length=120

# 型チェック
mypy *.py --ignore-missing-imports
```

---

## 📸 スクリーンショット

### メイン統合デモ画面

![a00_responses_api.py](assets/a00_image.png)

### 構造化出力デモ

![a01_structured_outputs](assets/a01_image.png)

### 関数呼び出しデモ

![a02_tools_pydantic](assets/a02_image.png)

### 画像処理デモ

![a03_images_vision](assets/a03_image.png)

### 音声処理デモ

![a04_audio_speeches](assets/a04_image.png)

### 会話状態管理

![a05_conversation_state](assets/a05_image.png)

### 推論パターンデモ

![a06_reasoning](assets/a06_image.png)

## 💼 プロジェクト構造

```
openai_api_jp/
├── 📚 学習用デモアプリケーション
│   ├── a0_simple_api.ipynb             # 入門: Jupyter Notebook
│   ├── a00_responses_api.py            # 統合デモ
│   ├── a01_structured_outputs_parse_schema.py  # 構造化出力
│   ├── a02_responses_tools_pydantic_parse.py   # 関数呼び出し
│   ├── a03_images_and_vision.py        # 画像処理
│   ├── a04_audio_speeches.py           # 音声処理
│   ├── a05_conversation_state.py       # 状態管理
│   └── a06_reasoning_chain_of_thought.py # 推論パターン
│
├── 🔧 ユーティリティ
│   ├── a10_get_vsid.py                 # Vector Store管理
│   ├── get_cities_list.py              # データ処理
│   ├── helper_api.py                   # API共通機能
│   └── helper_st.py                    # UI共通機能
│
├── 📁 リソース
│   ├── config.yml                      # 設定ファイル
│   ├── requirements.txt                # 依存関係
│   ├── pytest.ini                      # テスト設定
│   ├── data/                           # サンプルデータ
│   ├── images/                         # サンプル画像
│   ├── assets/                         # スクリーンショット
│   └── doc/                            # ドキュメント
│
└── 📖 ドキュメント
    ├── README.md                        # 本ドキュメント
    ├── README_setup.md                  # セットアップ詳細
    └── CLAUDE.md                        # Claude Code用設定
```

---

## 🌟 主な特徴

### ✅ 包括的なAPI網羅

- **テキスト生成**: GPT-4o, GPT-5, o1/o3推論モデル
- **構造化出力**: JSONスキーマ, Pydantic統合
- **マルチモーダル**: 画像生成(DALL-E), 画像解析(Vision), 音声(Whisper/TTS)
- **高度な機能**: Vector Store, Web検索, Realtime API

### ✅ 実践的な学習設計

- **段階的学習**: 基礎から応用まで体系的カリキュラム
- **実行可能なデモ**: すべてのコードが即座に実行可能
- **詳細なコメント**: 日本語による丁寧な解説
- **エラーハンドリング**: 本番環境を想定した堅牢な実装

### ✅ 開発者フレンドリー

- **モジュール設計**: 再利用可能なコンポーネント
- **型安全**: Pydanticによる型検証
- **テスト**: pytest完備
- **UI/UX**: Streamlitによる直感的インターフェース

---

## 📞 サポート・貢献

### 🐛 問題報告

[GitHub Issues](https://github.com/nakashima2toshio/openai_api_jp/issues)

### 🤝 コントリビューション

プルリクエスト歓迎！[Contributing Guide](CONTRIBUTING.md)を参照

### 📧 連絡先

- GitHub: [@nakashima2toshio](https://github.com/nakashima2toshio)
- Email: プロフィールを参照

---

## 📄 ライセンス

MIT License - 詳細は[LICENSE](LICENSE)ファイルを参照

---

<div align="center">

**🎯 OpenAI APIマスターへの道を、今すぐ始めよう！**

⭐ このプロジェクトが役立ったら、スターをお願いします！

</div>
