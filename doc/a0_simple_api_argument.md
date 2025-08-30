# OpenAI API 引数クラス構造ガイド
## 🎯 特に重要なクラス
- EasyInputMessageParam - すべてのメッセージの基本形
- ResponseInputTextParam/ImageParam - マルチモーダル入力の核
- FileSearchToolParam - Vector Store検索機能
- ResponseFormatTextJSONSchemaConfigParam - 構造化出力制御

## 📋 クラス分類と関係図

```
OpenAI Responses API
├── メッセージ系クラス
│   ├── EasyInputMessageParam (基本メッセージ)
│   ├── ResponseInputTextParam (テキスト入力)
│   └── ResponseInputImageParam (画像入力)
├── ツール系クラス
│   ├── FileSearchToolParam (ファイル検索)
│   ├── WebSearchToolParam (Web検索)
│   └── ComputerToolParam (Computer Use)
├── フォーマット系クラス
│   ├── ResponseTextConfigParam (テキスト設定)
│   └── ResponseFormatTextJSONSchemaConfigParam (JSON Schema)
├── 補助クラス
│   └── UserLocation (位置情報)
└── レスポンス系クラス
    └── Response (APIレスポンス)
```

## 🔧 メッセージ系クラス

### 1. EasyInputMessageParam
**用途**: 基本的なメッセージパラメータ（旧Chat Completionsと互換）

```python
# テキストのみ
EasyInputMessageParam(role="user", content="質問内容")

# マルチモーダル（テキスト + 画像）
EasyInputMessageParam(
    role="user",
    content=[
        ResponseInputTextParam(type="input_text", text="画像について説明して"),
        ResponseInputImageParam(
            type="input_image",
            image_url="https://example.com/image.jpg",
            detail="auto"
        )
    ]
)

# システムメッセージ
EasyInputMessageParam(role="developer", content="システム指示")
```

**属性**:
- `role`: `"user"` | `"assistant"` | `"system"` | `"developer"`
- `content`: `str` または `List[ResponseInput*Param]`

### 2. ResponseInputTextParam
**用途**: テキスト入力の指定

```python
ResponseInputTextParam(
    type="input_text",
    text="解析したいテキスト内容"
)
```

**属性**:
- `type`: 固定値 `"input_text"`
- `text`: 入力テキスト内容

### 3. ResponseInputImageParam
**用途**: 画像入力の指定

```python
# URL指定
ResponseInputImageParam(
    type="input_image",
    image_url="https://example.com/image.jpg",
    detail="auto"  # "low" | "high" | "auto"
)

# Base64指定
ResponseInputImageParam(
    type="input_image",
    image_url="data:image/jpeg;base64,/9j/4AAQ...",
    detail="high"
)
```

**属性**:
- `type`: 固定値 `"input_image"`
- `image_url`: 画像URL または Data URI
- `detail`: 解析精度 (`"low"`, `"high"`, `"auto"`)

## 🛠️ ツール系クラス

### 4. FileSearchToolParam
**用途**: Vector Storeを使ったファイル検索

```python
FileSearchToolParam(
    type="file_search",
    vector_store_ids=["vs_abc123", "vs_def456"],
    max_num_results=5
)
```

**属性**:
- `type`: 固定値 `"file_search"`
- `vector_store_ids`: Vector Store IDのリスト
- `max_num_results`: 最大検索結果数 (1-50)

### 5. WebSearchToolParam
**用途**: Web検索機能

```python
WebSearchToolParam(
    type="web_search_preview",
    user_location=UserLocation(
        type="approximate",
        country="JP",
        city="Tokyo",
        region="Tokyo"
    ),
    search_context_size="medium"  # "low" | "medium" | "high"
)
```

**属性**:
- `type`: 固定値 `"web_search_preview"`
- `user_location`: `UserLocation`オブジェクト
- `search_context_size`: コンテキストサイズ

### 6. ComputerToolParam
**用途**: Computer Use機能（画面操作）

```python
ComputerToolParam(type="computer")
```

**属性**:
- `type`: 固定値 `"computer"`

## 📐 フォーマット系クラス

### 7. ResponseTextConfigParam
**用途**: レスポンス形式の設定

```python
ResponseTextConfigParam(
    format=ResponseFormatTextJSONSchemaConfigParam(
        name="data_extraction",
        type="json_schema",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "date": {"type": "string"}
            },
            "required": ["name", "date"]
        },
        strict=True
    )
)
```

### 8. ResponseFormatTextJSONSchemaConfigParam
**用途**: JSON Schema形式の指定

```python
ResponseFormatTextJSONSchemaConfigParam(
    name="schema_name",
    type="json_schema",
    schema={...},  # JSON Schema仕様
    strict=True    # 厳密モード
)
```

## 🌍 補助クラス

### 9. UserLocation
**用途**: Web検索での位置情報指定

```python
UserLocation(
    type="approximate",  # "exact" | "approximate"
    country="JP",
    city="Tokyo",
    region="Tokyo"
)
```

## 📤 レスポンス系クラス

### 10. Response
**用途**: API呼び出しの結果

```python
# APIレスポンスの主要属性
response.id            # レスポンスID
response.model         # 使用モデル
response.created_at    # 作成日時
response.output        # 出力内容
response.usage         # トークン使用量
response.output_text   # テキスト出力（簡易アクセス）
```

## 💡 実際の使用例

### シンプルなテキスト質問
```python
messages = [
    EasyInputMessageParam(role="user", content="Pythonについて教えて")
]

response = client.responses.create(
    model="gpt-4o",
    input=messages
)
```

### 画像解析
```python
messages = [
    EasyInputMessageParam(
        role="user",
        content=[
            ResponseInputTextParam(type="input_text", text="この画像を説明して"),
            ResponseInputImageParam(
                type="input_image",
                image_url="https://example.com/image.jpg",
                detail="high"
            )
        ]
    )
]
```

### 構造化出力
```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "date": {"type": "string"}
    },
    "required": ["name", "date"]
}

text_config = ResponseTextConfigParam(
    format=ResponseFormatTextJSONSchemaConfigParam(
        name="event_extraction",
        type="json_schema",
        schema=schema,
        strict=True
    )
)

response = client.responses.create(
    model="gpt-4o",
    input=messages,
    text=text_config
)
```

### ツール使用（ファイル検索）
```python
search_tool = FileSearchToolParam(
    type="file_search",
    vector_store_ids=["vs_abc123"],
    max_num_results=5
)

response = client.responses.create(
    model="gpt-4o",
    input=messages,
    tools=[search_tool],
    include=["file_search_call.results"]
)
```

### Web検索
```python
location = UserLocation(
    type="approximate",
    country="JP",
    city="Tokyo",
    region="Tokyo"
)

web_tool = WebSearchToolParam(
    type="web_search_preview",
    user_location=location,
    search_context_size="medium"
)

response = client.responses.create(
    model="gpt-4o",
    input=messages,
    tools=[web_tool]
)
```

## 🔄 クラス間の関係性

1. **EasyInputMessageParam** は他のInputParamクラスを`content`として含むことができる
2. **ツール系クラス**は`tools`パラメータに配列で指定
3. **フォーマット系クラス**は`text`パラメータで出力形式を制御
4. **UserLocation**は**WebSearchToolParam**の必須属性
5. **Response**はすべてのAPIコールの戻り値

## ⚠️ 重要なポイント

- **role**は従来の`"system"`に加えて`"developer"`が利用可能
- **画像入力**はURL形式とBase64形式の両方対応
- **Vector Store**は事前作成が必要
- **JSON Schema**の`strict=True`で厳密な型チェック
- **Web検索**は位置情報が検索結果に影響
- **Temperature**は推論系モデル（o1, o3, o4系）では無効