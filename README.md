### 本概要署m、OpenAI API サンプルプログラム一覧

### 概要

- OpenAI APIの学習用サンプルプログラム集の機能一覧です。
- 各プログラムは異なるAPIの側面と機能を実際に体験できるよう設計されており、
- 基本的な使用法から高度な応用まで段階的に学習できます。
- （注）バージョンにより、右ペインの説明は拡充、整理されています。

#### 環境のセットアップ

[環境セットアップ](https://./README_setup.md)  <-- こちらを参照のこと

#### ドキュメント、設計書：

[ドキュメント] ./doc/ 以下のディレクトリ、プログラムと同名のファイル.md
-----------------------------------------------------------------------
## OpenAI APIの使い方： JupyterでAPIの基本を試そう
- a0_simple_api.ipynb

### **OpenAI Responses API Integrated Demo**


| Proguram Name                          | Overview                                                 |
| -------------------------------------- | -------------------------------------------------------- |
| a00_responses_api.py                   | Main integrated demo showcasing all OpenAI features      |
| a01_structured_outputs_parse_schema.py | Structured outputs with schema validation                |
| a02_responses_tools_pydantic_parse.py  | Pydantic-based parsing and function calling              |
| a03_images_and_vision.py               | Image generation and vision API demonstrations           |
| a04_audio_speeches.py                  | Text-to-speech, transcription, and realtime audio        |
| a05_conversation_state.py              | Conversation state management using previous_response_id |
| a06_reasoning_chain_of_thought.py      | Chain-of-thought reasoning patterns                      |

**主要API**: `responses.create`, Vector Stores API, OpenWeatherMap API, Web Search Tool, Computer Use Tool


| プログラム名                           | 概要                                               |
| -------------------------------------- | -------------------------------------------------- |
| a00_responses_api.py                   | OpenAI APIの全機能を統合的に紹介するメインデモ     |
| a01_structured_outputs_parse_schema.py | スキーマ検証を用いた構造化出力                     |
| a02_responses_tools_pydantic_parse.py  | Pydanticベースの解析と関数呼び出し                 |
| a03_images_and_vision.py               | 画像生成とビジョンAPIのデモンストレーション        |
| a04_audio_speeches.py                  | テキスト読み上げ、文字起こし、リアルタイム音声処理 |
| a05_conversation_state.py              | previous_response_idを使用した会話状態管理         |
| a06_reasoning_chain_of_thought.py      | Chain-of-thought 推論パターン                      |

---

## a00_responses_api.py


| プログラム名         | クラス・関数名            | 処理概要                         |
| -------------------- | ------------------------- | -------------------------------- |
| a00_responses_api.py | BaseDemo                  | デモ機能の基底クラス（統一化版） |
|                      | TextResponseDemo          | 基本テキスト応答                 |
|                      | MemoryResponseDemo        | 会話履歴付き応答                 |
|                      | ImageResponseDemo         | 画像入力（URL・Base64対応）      |
|                      | StructuredOutputDemo      | 構造化出力（create・parse対応）  |
|                      | WeatherDemo               | OpenWeatherMap API連携           |
|                      | FileSearchVectorStoreDemo | FileSearch専用                   |
|                      | WebSearchToolsDemo        | WebSearch専用                    |
|                      | DemoManager               | デモ統合管理・実行制御           |

## a01_structured_outputs_parse_schema.py

**Structured Outputs 6パターン**


| プログラム名                              | クラス・関数名        | 処理概要                         |
| ----------------------------------------- | --------------------- | -------------------------------- |
| a10_01_structured_outputs_parse_schema.py | BaseDemo              | デモ機能の基底クラス（統一化版） |
|                                           | EventExtractionDemo   | イベント情報抽出デモ             |
|                                           | MathReasoningDemo     | 数学的思考ステップデモ           |
|                                           | UIGenerationDemo      | UIコンポーネント生成デモ         |
|                                           | EntityExtractionDemo  | エンティティ抽出デモ             |
|                                           | ConditionalSchemaDemo | 条件分岐スキーマデモ             |
|                                           | ModerationDemo        | モデレーション＆拒否処理デモ     |
|                                           | DemoManager           | デモの管理クラス（統一化版）     |

**主要API**: `responses.parse`, Pydantic モデル

---

## a02_responses_tools_pydantic_parse.py

**Pydantic Parse 高度デモ**


| プログラム名                             | クラス・関数名                  | 処理概要                               |
| ---------------------------------------- | ------------------------------- | -------------------------------------- |
| a10_02_responses_tools_pydantic_parse.py | BaseDemo                        | デモ機能の基底クラス                   |
|                                          | BasicFunctionCallDemo           | 基本的なfunction callのデモ            |
|                                          | MultipleToolsDemo               | 複数ツールの登録・複数関数呼び出しデモ |
|                                          | AdvancedMultipleToolsDemo       | 高度な複数ツール呼び出しデモ           |
|                                          | NestedStructureDemo             | 入れ子構造のデモ                       |
|                                          | EnumTypeDemo                    | Enum型のデモ                           |
|                                          | NaturalTextStructuredOutputDemo | 自然文での構造化出力デモ               |
|                                          | SimpleDataExtractionDemo        | シンプルなデータ抽出デモ               |
|                                          | MultipleEntityExtractionDemo    | 複数エンティティ抽出デモ               |
|                                          | ComplexQueryDemo                | 複雑なクエリパターンデモ               |
|                                          | DynamicEnumDemo                 | 動的な列挙型デモ                       |
|                                          | ChainOfThoughtDemo              | 思考の連鎖デモ                         |
|                                          | ConversationHistoryDemo         | 会話履歴デモ                           |
|                                          | DemoManager                     | デモの管理クラス                       |

**主要API**: `responses.parse`, `pydantic_function_tool`, OpenWeatherMap API

---

## a03_images_and_vision.py

**画像＆ビジョンAPI**


| プログラム名                | クラス・関数名        | 処理概要                       |
| --------------------------- | --------------------- | ------------------------------ |
| a10_03_images_and_vision.py | BaseDemo              | ベースデモクラス（統一化版）   |
|                             | URLImageToTextDemo    | URL画像からテキスト生成デモ    |
|                             | Base64ImageToTextDemo | Base64画像からテキスト生成デモ |
|                             | PromptToImageDemo     | プロンプトから画像生成デモ     |
|                             | DemoManager           | デモ管理クラス（統一化版）     |

**主要API**: `responses.create`, `images.generate`, DALL-E 3/2

---

## a04_audio_speeches.py

**音声処理API統合**


| プログラム名             | クラス・関数名        | 処理概要                               |
| ------------------------ | --------------------- | -------------------------------------- |
| a10_04_audio_speeches.py | BaseDemo              | デモ機能の基底クラス（音声用統一化版） |
|                          | TextToSpeechDemo      | Text to Speech API のデモ              |
|                          | SpeechToTextDemo      | Speech to Text API のデモ              |
|                          | SpeechTranslationDemo | Speech Translation API のデモ          |
|                          | RealtimeApiDemo       | Realtime API のデモ                    |
|                          | ChainedVoiceAgentDemo | Chained Voice Agent のデモ             |
|                          | AudioDemoManager      | 音声デモの管理クラス（統一化版）       |

**主要API**: `audio.speech.create`, `audio.transcriptions.create`, `audio.translations.create`, Realtime API

---

## a05_conversation_state.py

**会話状態管理**


| プログラム名                 | クラス・関数名           | 処理概要                     |
| ---------------------------- | ------------------------ | ---------------------------- |
| a10_05_conversation_state.py | BaseDemo                 | ベースデモクラス（統一化版） |
|                              | StatefulConversationDemo | ステートフルな会話継続デモ   |
|                              | WebSearchParseDemo       | Web検索と構造化パースデモ    |
|                              | FunctionCallingDemo      | Function Callingデモ         |
|                              | DemoManager              | デモ管理クラス（統一化版）   |

**主要API**: `responses.create`, `responses.parse`, Web Search Tool, Open-Meteo API

---

## a06_reasoning_chain_of_thought.py

**Chain of Thought 5パターン**


| プログラム名                         | クラス・関数名          | 処理概要                                     |
| ------------------------------------ | ----------------------- | -------------------------------------------- |
| a10_06_reasoning_chain_of_thought.py | BaseDemo                | ベースデモクラス（統一化版）                 |
|                                      | StepByStepReasoningDemo | 段階的推論（Step-by-Step）デモ               |
|                                      | HypothesisTestDemo      | 仮説検証推論デモ                             |
|                                      | TreeOfThoughtDemo       | 思考の木（Tree of Thought）デモ              |
|                                      | ProsConsDecisionDemo    | 賛否比較決定（Pros-Cons-Decision）デモ       |
|                                      | PlanExecuteReflectDemo  | 計画実行振り返り（Plan-Execute-Reflect）デモ |
|                                      | DemoManager             | デモ管理クラス（統一化版）                   |

**主要API**: `responses.create`, 推論系モデル対応

---

### ヘルパー関数


| ファイル名    | 概要                                                                                         | 利用API / 機能        |
| ------------- | -------------------------------------------------------------------------------------------- | --------------------- |
| helper_api.py | OpenAI Python SDK 呼び出しや共通ユーティリティの集約（クライアント初期化・共通呼び出し等）。 | **OpenAI Python SDK** |
| helper_st.py  | Streamlit UI 用の共通部品（レイアウト/入力/表示まわりのヘルパー）。                          | **Streamlit**         |

## a00_responses_api.py 画面

![image.png](assets/a00_image.png?t=1756205198890)

### a01_structured_outputs_parse_schema.py　画面

![a01_image.png](assets/a01_image.png)

### a02_responses_tools_pydantic_parse.py　画面

![a02_image.png](assets/a02_image.png)

### a03_images_and_vision.py　画面

![a03_image.png](assets/a03_image.png)

### a04_audio_speeches.py　画面

![a04_image.png](assets/a04_image.png)

### a05_conversation_state.py　画面

![a05_image.png](assets/a05_image.png)

### a06_reasoning_chain_of_thought.py　画面

![a06_image.png](assets/a06_image.png)

---

## 学習の進め方

### 📚 初心者向け

- **a00_responses_api.py** - 全機能を一通り体験
- **a01_structured_outputs_parse_schema.py** - 構造化出力の基本

### 🔧 中級者向け

- **a02_responses_tools_pydantic_parse.py** - Pydantic活用
- **a03_images_and_vision.py** - マルチモーダル処理

### 🚀 上級者向け

- **a04_audio_speeches.py** - 音声処理
- **a05_conversation_state.py** - 状態管理
- **a06_reasoning_chain_of_thought.py** - 推論パターン

---

## 実行方法　 : （注）ポート番号は適切に調整してください。

```bash
# メイン統合デモ
streamlit run a00_responses_api.py --server.port=8501

# 構造化出力デモ
streamlit run a01_structured_outputs_parse_schema.py --server.port=8501

# Tools・Pydantic Parse デモ
streamlit run a02_responses_tools_pydantic_parse.py --server.port=8502

# 画像・ビジョンデモ
streamlit run a03_images_and_vision.py --server.port=8503

# 音声処理デモ
streamlit run a04_audio_speeches.py --server.port=8504

# 会話状態管理デモ
streamlit run a05_conversation_state.py --server.port=8505

# Chain of Thought デモ
streamlit run a06_reasoning_chain_of_thought.py --server.port=8506
```

## 必要な環境変数

```bash
# 必須
export OPENAI_API_KEY='your-openai-api-key'

# オプション（一部機能で使用）
export OPENWEATHER_API_KEY='your-openweather-api-key'
export EXCHANGERATE_API_KEY='your-exchangerate-api-key'
```

---

### その他のリポジトリ一覧：

・内容　　　　　　　　　　　　　　「リポジトリーURL」

- OpenAI API - 基本・応用：　URL:[openai_api_jp](https://github.com/nakashima2toshio/openai_api_jp)　このプロジェクトサンプル：6本、API-41パターン
- RAGの作成と検索：          URL:[openai_rag_jp](https://github.com/nakashima2toshio/openai_rag_jp)　  別リポジトリ（整備中）
- MCPの作成と利用例:         URL:[openai_mcp_jp](https://github.com/nakashima2toshio/openai_mcp_jp)　　別リポジトリ（整備中）
- Agentの作成と利用例:       URL:[openai_agent_jp](https://github.com/nakashima2toshio/openai_agent_jp)　別リポジトリ（作成中）

### 画面構成

![image.png](assets/a00_image.png)

### OpenAI API：利用例

#### 左ペイン

![l_image.png](assets/l_painimage.png)

### セットアップ

```bash
# 1. リポジトリクローン
git clone https://github.com/nakashima2toshio/openai_api_app.git
cd openai_api_app

# 2. 依存関係インストール
pip install -r requirements.txt

# 3. 環境変数設定
export OPENAI_API_KEY='your-api-key'

# 4. 実行
streamlit run a10_00_responses_api.py
```
