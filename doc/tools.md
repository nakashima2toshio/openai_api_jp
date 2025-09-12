# OpenAI API Tools関連の構成と使い方

## 概要

OpenAI APIのTools機能は、AIモデルに外部ツールや関数を呼び出す能力を与える仕組みです。このドキュメントでは、プロジェクトで使用されているTools関連のクラス、パラメータ、実装パターンについて解説します。

## 1. 主要なツールパラメータ型

### 1.1 FileSearchToolParam

ベクターストア内のドキュメントを検索するためのツールパラメータです。

```python
from openai.types.responses import FileSearchToolParam

# FileSearchツールの設定
fs_tool = FileSearchToolParam(
    type="file_search",
    vector_store_ids=["vs_abc123"],  # ベクターストアID
    max_num_results=5  # 最大検索結果数
)
```

**主要なパラメータ:**
- `type`: "file_search"（固定値）
- `vector_store_ids`: 検索対象のベクターストアIDリスト
- `max_num_results`: 返される最大結果数

### 1.2 WebSearchToolParam

Web検索を実行するためのツールパラメータです。

```python
from openai.types.responses import WebSearchToolParam

# WebSearchツールの設定
ws_tool = WebSearchToolParam(
    type="web_search_preview",
    user_location={
        "type": "approximate",
        "country": "JP",
        "city": "Tokyo",
        "region": "Tokyo"
    },
    search_context_size="medium"  # "low", "medium", "high"
)
```

**主要なパラメータ:**
- `type`: "web_search_preview"（固定値）
- `user_location`: ユーザーの地域情報
- `search_context_size`: 検索コンテキストのサイズ

### 1.3 FunctionToolParam

カスタム関数を定義して呼び出すためのツールパラメータです。

```python
from openai.types.responses import FunctionToolParam

# Function Callingツールの設定
weather_tool: FunctionToolParam = {
    "type": "function",
    "name": "get_weather",
    "description": "指定された場所の天気情報を取得",
    "parameters": {
        "type": "object",
        "properties": {
            "latitude": {"type": "number", "description": "緯度"},
            "longitude": {"type": "number", "description": "経度"}
        },
        "required": ["latitude", "longitude"],
        "additionalProperties": False
    },
    "strict": True  # スキーマの厳密な検証
}
```

### 1.4 ComputerToolParam

コンピュータ操作（スクリーンショット、クリック等）のためのツールパラメータです。

```python
from openai.types.responses import ComputerToolParam

computer_tool = ComputerToolParam(
    type="computer"
    # その他のパラメータは用途に応じて設定
)
```

## 2. Pydantic Function Tool

Pydanticモデルを使用した関数定義の簡潔な方法です。

### 2.1 基本的な使用方法

```python
from pydantic import BaseModel
from openai import pydantic_function_tool

# Pydanticモデルの定義
class WeatherRequest(BaseModel):
    city: str
    date: str

# ツールとして使用
response = client.responses.parse(
    model="gpt-4o",
    input=messages,
    tools=[pydantic_function_tool(WeatherRequest)]
)
```

### 2.2 複数ツールの組み合わせ

```python
class NewsRequest(BaseModel):
    topic: str
    date: str

class CalculatorRequest(BaseModel):
    exp: str  # 計算式

# 複数のツールを同時に使用
response = client.responses.parse(
    model="gpt-4o",
    input=messages,
    tools=[
        pydantic_function_tool(WeatherRequest),
        pydantic_function_tool(NewsRequest),
        pydantic_function_tool(CalculatorRequest, name="calculator")
    ]
)
```

### 2.3 ネストされた構造

```python
class Task(BaseModel):
    name: str
    deadline: str

class ProjectRequest(BaseModel):
    project_name: str
    tasks: List[Task]

# ネストされた構造を持つツール
response = client.responses.parse(
    model="gpt-4o",
    input=messages,
    tools=[pydantic_function_tool(ProjectRequest)]
)
```

## 3. 実装パターン

### 3.1 FileSearch実装例 (a00_responses_api.py)

```python
def _execute_ai_search(self, vector_store_id: str, query: str, max_results: int = 5):
    """FileSearchを使用したAI検索"""
    # FileSearchツールパラメータの作成
    fs_tool = FileSearchToolParam(
        type="file_search",
        vector_store_ids=[vector_store_id],
        max_num_results=max_results
    )
    
    # API呼び出し
    response = self.call_api_unified(
        messages=[EasyInputMessageParam(role="user", content=query)],
        tools=[fs_tool],
        include=["file_search_call.results"]  # 詳細結果を含める
    )
    
    # 結果の処理
    if hasattr(response, "file_search_call") and response.file_search_call:
        if hasattr(response.file_search_call, "results"):
            # 検索結果の表示処理
            self._display_ai_search_results(response.file_search_call.results)
```

### 3.2 WebSearch実装例 (a00_responses_api.py)

```python
def _execute_web_search(self, query: str, context_size: Literal["low", "medium", "high"]):
    """WebSearchツールの実行"""
    # 地域情報の設定
    user_location = dict(
        type="approximate",
        country="JP",
        city="Tokyo",
        region="Tokyo"
    )
    
    # WebSearchツールの設定
    ws_tool = WebSearchToolParam(
        type="web_search_preview",
        user_location=user_location,
        search_context_size=context_size
    )
    
    # API呼び出し
    response = self.call_api_unified(
        messages=[EasyInputMessageParam(role="user", content=query)],
        tools=[ws_tool]
    )
    
    # 結果表示
    ResponseProcessorUI.display_response(response)
```

### 3.3 Function Calling実装例 (a05_conversation_state.py)

```python
def _execute_function_calling(self, query: str, selected_city: str, cities: dict):
    """Function Callingの実行"""
    # Pydanticモデルでパラメータ定義
    class WeatherParams(BaseModel):
        latitude: float = Field(..., description="緯度（10進）")
        longitude: float = Field(..., description="経度（10進）")
    
    # 実際の関数
    def get_weather(latitude: float, longitude: float) -> dict:
        """Open-Meteo APIで天気情報を取得"""
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        response = requests.get(url)
        return response.json()
    
    # JSON Schema生成
    schema = WeatherParams.model_json_schema()
    schema["additionalProperties"] = False
    
    # FunctionToolParam構築
    weather_tool: FunctionToolParam = {
        "type": "function",
        "name": "get_weather",
        "description": get_weather.__doc__,
        "parameters": schema,
        "strict": True,
    }
    
    # API呼び出し
    response = self.client.responses.create(
        model="gpt-4.1",
        input=query,
        tools=[weather_tool]
    )
    
    # 実際のデータ取得と結果表示
    coords = cities[selected_city]
    weather_data = get_weather(coords["lat"], coords["lon"])
```

### 3.4 Pydantic Parse実装例 (a02_responses_tools_pydantic_parse.py)

```python
# Enumを使った制約付きモデル
class Unit(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"

class WeatherRequestWithUnit(BaseModel):
    city: str
    date: str
    unit: Unit  # Enum制約

# 使用例
messages = self.get_default_messages()
messages.append(EasyInputMessageParam(role="user", content=user_input))

response = self.client.responses.parse(
    model=model,
    input=messages,
    tools=[pydantic_function_tool(WeatherRequestWithUnit)]
)

# レスポンスからツール呼び出し結果を取得
if hasattr(response, 'output'):
    for item in response.output:
        if hasattr(item, 'type') and item.type == "tool_call":
            # ツール呼び出しの結果処理
            result = item.parsed_arguments
```

## 4. APIレスポンスの処理

### 4.1 ツール呼び出し結果の取得

```python
# レスポンスからツール呼び出し結果を抽出
def extract_tool_calls(response: Response) -> List[Dict]:
    tool_calls = []
    
    if hasattr(response, 'output'):
        for item in response.output:
            if hasattr(item, 'type') and item.type == "tool_call":
                tool_call = {
                    'name': item.name,
                    'arguments': item.parsed_arguments
                }
                tool_calls.append(tool_call)
    
    return tool_calls
```

### 4.2 FileSearch結果の処理

```python
# FileSearch結果の詳細表示
def display_file_search_results(results):
    for idx, result in enumerate(results, 1):
        st.write(f"**結果 {idx}**")
        
        if hasattr(result, 'score'):
            st.write(f"関連度スコア: {result.score:.4f}")
        
        if hasattr(result, 'content'):
            # コンテンツの表示
            for content_item in result.content:
                if hasattr(content_item, 'text'):
                    st.markdown(content_item.text)
        
        if hasattr(result, 'file'):
            st.write(f"ファイル: {result.file.name}")
```

## 5. エラーハンドリング

### 5.1 ツール実行エラーの処理

```python
try:
    response = self.client.responses.create(
        model=model,
        input=messages,
        tools=[tool_param]
    )
except Exception as e:
    logger.error(f"ツール実行エラー: {e}")
    st.error(f"ツールの実行に失敗しました: {str(e)}")
    
    if config.get("experimental.debug_mode", False):
        st.exception(e)
```

### 5.2 パラメータ検証

```python
# Pydanticモデルでの自動検証
class ValidatedRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    
    @validator('date')
    def validate_date(cls, v):
        # カスタム検証ロジック
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('日付形式が正しくありません')
        return v
```

## 6. 設定とカスタマイズ

### 6.1 config.ymlでの設定

```yaml
tools:
  file_search:
    default_max_results: 5
    enable_detailed_results: true
  
  web_search:
    default_location:
      country: "JP"
      city: "Tokyo"
    default_context_size: "medium"
  
  function_calling:
    strict_mode: true
    timeout: 30
```

### 6.2 動的なツール選択

```python
def get_tools_for_query(query: str) -> List:
    """クエリに応じて適切なツールを選択"""
    tools = []
    
    if "検索" in query or "探す" in query:
        tools.append(FileSearchToolParam(
            type="file_search",
            vector_store_ids=get_vector_store_ids()
        ))
    
    if "天気" in query or "weather" in query.lower():
        tools.append(pydantic_function_tool(WeatherRequest))
    
    if "計算" in query:
        tools.append(pydantic_function_tool(CalculatorRequest))
    
    return tools
```

## 7. ベストプラクティス

### 7.1 ツール設計の原則

1. **単一責任**: 各ツールは1つの明確な目的を持つ
2. **明確な命名**: ツール名と関数名は機能を明確に表す
3. **詳細な説明**: descriptionフィールドで用途を明確に記述
4. **パラメータ検証**: Pydanticやスキーマで入力を厳密に検証

### 7.2 パフォーマンス最適化

```python
# ツール呼び出しのキャッシング
@cache_result(ttl=3600)
def cached_tool_call(tool_params, query):
    response = client.responses.create(
        model="gpt-4o",
        input=query,
        tools=[tool_params]
    )
    return response

# バッチ処理
def batch_tool_calls(queries: List[str], tools: List):
    """複数のクエリを効率的に処理"""
    results = []
    for query in queries:
        # 並列処理やバッチ最適化を実装
        result = process_with_tools(query, tools)
        results.append(result)
    return results
```

### 7.3 セキュリティ考慮事項

```python
# APIキーの安全な管理
def get_secure_api_key(service: str) -> str:
    """環境変数から安全にAPIキーを取得"""
    key = os.getenv(f"{service.upper()}_API_KEY")
    if not key:
        raise ValueError(f"{service}のAPIキーが設定されていません")
    return key

# 入力のサニタイゼーション
def sanitize_tool_input(input_data: Dict) -> Dict:
    """ツール入力のサニタイゼーション"""
    # SQLインジェクション対策
    # XSS対策
    # その他のセキュリティ処理
    return sanitized_data
```

## 8. トラブルシューティング

### 8.1 一般的な問題と解決策

| 問題 | 原因 | 解決策 |
|------|------|--------|
| ツールが呼び出されない | スキーマの不一致 | Pydanticモデルのスキーマを確認 |
| FileSearch結果が空 | ベクターストアIDの誤り | vector_store_idsを確認 |
| Function Callingエラー | パラメータ型の不一致 | JSON Schemaの型定義を確認 |
| WebSearch結果が少ない | context_sizeが小さい | "high"に設定してみる |

### 8.2 デバッグ方法

```python
# デバッグモードの有効化
if config.get("experimental.debug_mode", False):
    # 詳細なログ出力
    logger.debug(f"Tool parameters: {tool_params}")
    logger.debug(f"API response: {response}")
    
    # レスポンスの完全な構造を表示
    st.json(response.model_dump())
```

## まとめ

OpenAI APIのTools機能は、以下の要素で構成されています：

1. **ツールパラメータ型**: FileSearch、WebSearch、Function、Computer
2. **Pydantic統合**: モデルベースの型安全な関数定義
3. **API呼び出し**: responses.create()やresponses.parse()での利用
4. **結果処理**: ツール呼び出し結果の抽出と表示

これらを組み合わせることで、AIモデルに外部ツールや関数を効果的に利用させることができ、より高度で実用的なアプリケーションを構築できます。