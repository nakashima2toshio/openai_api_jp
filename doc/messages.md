# OpenAI API Messages関連クラスの構成と使い方

## 概要

このドキュメントでは、OpenAI APIで使用されるメッセージ関連のクラスとその構造、使用方法について解説します。特に`call_api_unified`メソッドで利用される主要なクラスと関数について詳述します。

## 1. 主要なメッセージ型

### 1.1 EasyInputMessageParam

OpenAI Responses APIで使用される基本的なメッセージパラメータです。

```python
from openai.types.responses import EasyInputMessageParam

# 基本的な使用例
message = EasyInputMessageParam(
    role="user",  # "user", "assistant", "system", "developer"のいずれか
    content="こんにちは、今日の天気を教えてください。"
)
```

**主要な特徴:**
- `role`: メッセージの送信者を示す（user/assistant/system/developer）
- `content`: メッセージの内容（テキストまたはマルチモーダルコンテンツ）
- Responses API（`responses.create()`, `responses.parse()`）で使用

### 1.2 ResponseInputTextParam

テキスト入力を表すパラメータです。マルチモーダル入力時に使用されます。

```python
from openai.types.responses import ResponseInputTextParam

text_param = ResponseInputTextParam(
    type="input_text",
    text="この画像について説明してください。"
)
```

### 1.3 ResponseInputImageParam

画像入力を表すパラメータです。

```python
from openai.types.responses import ResponseInputImageParam

# URL形式の画像
image_param = ResponseInputImageParam(
    type="input_image",
    source={"type": "url", "data": image_url}
)

# Base64形式の画像
image_param = ResponseInputImageParam(
    type="input_image",
    source={"type": "base64", "data": base64_string}
)
```

### 1.4 Chat Completion用メッセージ型

Chat Completions APIでは異なるメッセージ型を使用します：

```python
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam
)
```

## 2. メッセージ管理クラス

### 2.1 MessageManager (helper_api.py)

メッセージ履歴を管理するクラスです。

```python
from helper_api import MessageManager

# インスタンス化
manager = MessageManager()

# メッセージの追加
manager.add_message("user", "質問内容")
manager.add_message("assistant", "回答内容")

# メッセージ履歴の取得
messages = manager.get_messages()

# メッセージのクリア
manager.clear_messages()

# エクスポート/インポート
exported_data = manager.export_messages()
manager.import_messages(exported_data)
```

**主な機能:**
- メッセージ履歴の自動管理
- メッセージ数の制限（config.ymlの`api.message_limit`で設定）
- developerメッセージの保持
- エクスポート/インポート機能

### 2.2 MessageManagerUI (helper_st.py)

Streamlit用のメッセージ管理UIクラスです。

```python
from helper_st import MessageManagerUI

# デモごとにユニークなキーで初期化
message_manager = MessageManagerUI(f"messages_{demo_key}")

# メッセージの追加と表示
message_manager.add_message("user", user_input)
message_manager.add_message("assistant", response_text)

# 会話履歴の表示
message_manager.display_messages()
```

## 3. デフォルトメッセージ関数

### 3.1 get_default_messages()

config.ymlから設定されたデフォルトメッセージを取得します。

```python
from helper_api import get_default_messages

messages = get_default_messages()
# 返り値:
# [
#     EasyInputMessageParam(role="developer", content="You are a helpful assistant..."),
#     EasyInputMessageParam(role="user", content="Please help me..."),
#     EasyInputMessageParam(role="assistant", content="I'll help you...")
# ]
```

### 3.2 append_user_message()

デフォルトメッセージにユーザーメッセージを追加します。

```python
from helper_api import append_user_message

messages = append_user_message("新しい質問内容")
```

### 3.3 append_developer_message() / append_assistant_message()

同様に、developer/assistantメッセージを追加します。

```python
from helper_api import append_developer_message, append_assistant_message

messages = append_developer_message("開発者向け指示")
messages = append_assistant_message("アシスタントの応答")
```

## 4. call_api_unified メソッドの実装パターン

### 4.1 基本的な実装 (a00_responses_api.py)

```python
def call_api_unified(self, messages: List[EasyInputMessageParam], 
                    temperature: Optional[float] = None, **kwargs):
    """統一されたAPI呼び出し"""
    model = self.get_model()
    
    # API呼び出しパラメータの構築
    api_params = {
        "model": model,
        "input": messages,  # Responses APIでは "input" を使用
    }
    
    # temperatureが指定されている場合は追加
    if temperature is not None:
        api_params["temperature"] = temperature
    
    # その他のパラメータを追加
    api_params.update(kwargs)
    
    # OpenAI APIを呼び出し
    response = self.client.responses.create(**api_params)
    
    return response
```

### 4.2 構造化出力での使用 (a01_structured_outputs_parse_schema.py)

```python
# JSON Schema形式での構造化出力
messages = get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=user_input))

response = client.responses.create(
    model=model,
    input=messages,
    text=ResponseTextConfigParam(
        type="json_schema",
        json_schema=ResponseFormatTextJSONSchemaConfigParam(
            name="response_name",
            schema=json_schema,
            strict=True
        )
    )
)
```

### 4.3 マルチモーダル入力 (a03_images_and_vision.py)

```python
# テキストと画像を組み合わせた入力
messages = get_default_messages()
messages.append(
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(type="input_text", text=question),
            ResponseInputImageParam(
                type="input_image",
                source={"type": "url", "data": image_url}
            )
        ]
    )
)

response = call_api_unified(messages)
```

## 5. 使用パターン別の実装例

### 5.1 単一ターンの会話

```python
# 1回きりの質問応答
messages = get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=user_input))
response = call_api_unified(messages)
```

### 5.2 マルチターンの会話

```python
# 会話履歴を保持
messages = get_default_messages()

# 1回目の会話
messages.append(EasyInputMessageParam(role="user", content=input1))
response1 = call_api_unified(messages)
messages.append(EasyInputMessageParam(role="assistant", content=response1_text))

# 2回目の会話（履歴を含む）
messages.append(EasyInputMessageParam(role="user", content=input2))
response2 = call_api_unified(messages)
```

### 5.3 会話履歴の管理

```python
# MessageManagerを使用した履歴管理
manager = MessageManager()

# 新しいメッセージを追加
manager.add_message("user", user_input)
response = call_api_unified(manager.get_messages())
manager.add_message("assistant", response_text)

# 履歴のエクスポート
conversation_data = manager.export_messages()
```

## 6. クラス間の関係

```
┌─────────────────────────────────────────────────────────┐
│                    OpenAI API Types                      │
├─────────────────────────────────────────────────────────┤
│ ▪ EasyInputMessageParam (基本メッセージ型)               │
│ ▪ ResponseInputTextParam (テキスト入力)                  │
│ ▪ ResponseInputImageParam (画像入力)                     │
│ ▪ ChatCompletionMessageParam (Chat API用)               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                      helper_api.py                       │
├─────────────────────────────────────────────────────────┤
│ ▪ MessageManager (メッセージ履歴管理)                    │
│ ▪ get_default_messages() (デフォルトメッセージ取得)      │
│ ▪ append_*_message() (メッセージ追加関数)               │
│ ▪ OpenAIClient (API クライアント)                        │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                      helper_st.py                        │
├─────────────────────────────────────────────────────────┤
│ ▪ MessageManagerUI (Streamlit用メッセージ管理UI)         │
│ ▪ ResponseProcessorUI (レスポンス表示)                   │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                    Demo Applications                     │
├─────────────────────────────────────────────────────────┤
│ ▪ a00_responses_api.py (基本デモ)                        │
│ ▪ a01_structured_outputs_parse_schema.py (構造化出力)    │
│ ▪ a02_responses_tools_pydantic_parse.py (ツール使用)     │
│ ▪ a03_images_and_vision.py (画像処理)                    │
│ ▪ a04_audio_speeches.py (音声処理)                       │
│ ▪ a05_conversation_state.py (会話状態管理)               │
│ ▪ a06_reasoning_chain_of_thought.py (推論)              │
└─────────────────────────────────────────────────────────┘
```

## 7. 設定とカスタマイズ

### 7.1 config.yml での設定

```yaml
# デフォルトメッセージの設定
default_messages:
  developer: "You are a helpful assistant specialized in software development."
  user: "Please help me with my software development tasks."
  assistant: "I'll help you with your software development needs."

# メッセージ履歴の制限
api:
  message_limit: 50  # 保持する最大メッセージ数
```

### 7.2 エラーハンドリング

```python
from helper_api import error_handler, timer

@error_handler
@timer
def call_api_unified(self, messages, **kwargs):
    try:
        response = self.client.responses.create(
            model=self.model,
            input=messages,
            **kwargs
        )
        return response
    except Exception as e:
        logger.error(f"API呼び出しエラー: {e}")
        raise
```

## 8. ベストプラクティス

1. **メッセージ型の選択**
   - Responses API: `EasyInputMessageParam`を使用
   - Chat Completions API: `ChatCompletionMessageParam`系を使用

2. **履歴管理**
   - 長い会話では`MessageManager`を使用して履歴を管理
   - 必要に応じて履歴をエクスポート/インポート

3. **マルチモーダル入力**
   - テキストと画像を組み合わせる場合は`ResponseInputTextParam`と`ResponseInputImageParam`を使用

4. **エラーハンドリング**
   - `error_handler`デコレータを使用してエラーを適切に処理
   - ログを活用してデバッグ

5. **パフォーマンス**
   - `timer`デコレータで実行時間を計測
   - `TokenManager`でトークン使用量を管理

## まとめ

OpenAI APIのメッセージ関連クラスは、以下の階層構造で組織されています：

1. **OpenAI API型定義**: 基本的なメッセージ型とパラメータ
2. **helper_api.py**: メッセージ管理とAPI呼び出しのロジック
3. **helper_st.py**: Streamlit用のUI関連機能
4. **デモアプリケーション**: 実際の使用例とパターン

この構造により、柔軟で保守性の高いOpenAI APIアプリケーションの開発が可能になります。