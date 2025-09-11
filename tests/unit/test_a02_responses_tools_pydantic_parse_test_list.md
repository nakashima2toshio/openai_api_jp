# a02_responses_tools_pydantic_parse.py テスト項目一覧表

## 📋 テスト概要
- **対象ファイル**: `a02_responses_tools_pydantic_parse.py`
- **テストファイル**: `tests/unit/test_a02_responses_tools_pydantic_parse.py`
- **総テスト数**: 25項目
- **テスト対象**: Tools & Pydantic Parse デモアプリケーション

## 🧪 テスト項目詳細

### 1. ページ設定テスト (TestPageConfig)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 1 | `test_page_config_setup` | ページ設定の実行 | Streamlitページ設定が正しく呼ばれることを確認 | ✅ |

### 2. 基底クラステスト (TestBaseDemoClass)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 2 | `test_base_demo_initialization` | BaseDemo初期化 | ConfigManager、OpenAIClient等が正しく初期化されることを確認 | ✅ |
| 3 | `test_select_model` | モデル選択メソッド | UIHelper.select_modelが正しく呼ばれることを確認 | ✅ |
| 4 | `test_setup_sidebar` | サイドバー設定 | 情報パネルの各メソッドが呼ばれることを確認 | ✅ |

### 3. BasicFunctionCallDemoテスト (TestBasicFunctionCallDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 5 | `test_run_method` | run()メソッドの実行 | デモの初期化とUI要素の表示を確認 | ✅ |
| 6 | `test_process_query` | _process_queryメソッド | Function Call APIの呼び出しと処理を確認 | ✅ |
| 7 | `test_fetch_weather_data` | 天気データ取得 | OpenWeatherMap APIとの連携を確認 | ✅ |

### 4. NestedStructureDemoテスト (TestNestedStructureDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 8 | `test_process_query_nested` | 入れ子構造処理 | ProjectRequestモデルでの階層構造処理を確認 | ✅ |

### 5. EnumTypeDemoテスト (TestEnumTypeDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 9 | `test_process_query_enum` | Enum型処理 | WeatherRequestWithUnitモデルでのEnum型処理を確認 | ✅ |

### 6. NaturalTextStructuredOutputDemoテスト (TestNaturalTextStructuredOutputDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 10 | `test_process_query_math` | 数学問題処理 | MathResponseモデルでの段階的解答処理を確認 | ✅ |

### 7. ConversationHistoryDemoテスト (TestConversationHistoryDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 11 | `test_process_query_conversation` | 会話履歴処理 | QAResponseモデルと履歴管理を確認 | ✅ |

### 8. デモマネージャーテスト (TestDemoManager)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 12 | `test_demo_manager_initialization` | DemoManager初期化 | 10個のデモインスタンスが正しく作成されることを確認 | ✅ |
| 13 | `test_demo_manager_run` | デモ選択と実行 | 選択されたデモが正しく実行されることを確認 | ✅ |

### 9. Pydanticモデルテスト (TestPydanticModels)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 14 | `test_weather_request_model` | WeatherRequestモデル | 都市と日付フィールドの検証 | ✅ |
| 15 | `test_project_request_model` | ProjectRequestモデル | プロジェクト名とタスクリストの検証 | ✅ |
| 16 | `test_unit_enum` | Unit Enumモデル | 温度単位Enumの検証 | ✅ |
| 17 | `test_weather_request_with_unit_model` | WeatherRequestWithUnitモデル | Enum付き天気リクエストの検証 | ✅ |
| 18 | `test_math_response_model` | MathResponseモデル | 数学的ステップと最終回答の検証 | ✅ |
| 19 | `test_qa_response_model` | QAResponseモデル | 質問と回答ペアの検証 | ✅ |
| 20 | `test_condition_model` | Conditionモデル | クエリ条件の検証 | ✅ |
| 21 | `test_query_model` | Queryモデル | 複雑なクエリ構造の検証 | ✅ |

### 10. エラーハンドリングテスト (TestErrorHandling)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 22 | `test_handle_error` | エラー処理 | エラーメッセージの表示処理を確認 | ✅ |

### 11. 統合テスト (TestIntegration)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 23 | `test_main_function` | main関数の実行 | DemoManager作成と実行を確認 | ✅ |

## 📊 テストカバレージ

### カバーされている主要機能
- ✅ ページ設定
- ✅ 基底クラスの初期化とメソッド
- ✅ Function Call API呼び出し（pydantic_function_tool）
- ✅ 5つの主要デモクラス
  - BasicFunctionCallDemo（基本的なFunction Call）
  - NestedStructureDemo（入れ子構造）
  - EnumTypeDemo（Enum型）
  - NaturalTextStructuredOutputDemo（自然文構造化出力）
  - ConversationHistoryDemo（会話履歴）
- ✅ DemoManagerによるデモ選択と実行
- ✅ すべてのPydanticモデル定義
- ✅ 外部API連携（OpenWeatherMap）
- ✅ エラーハンドリング

### 特徴的なテスト内容
- **pydantic_function_tool**: OpenAIのFunction Call APIのモック
- **入れ子構造**: ProjectRequestとTaskの階層構造
- **Enum型処理**: Unit型での型安全な選択
- **会話履歴管理**: セッション状態を使用した履歴保存
- **外部API連携**: OpenWeatherMap APIのモック

## 🔧 テスト技術詳細

### 使用したモック技術
1. **Streamlitコンポーネント**: `@patch`デコレータで完全モック化
2. **OpenAI responses.parse API**: `MagicMock`でFunction Callをシミュレート
3. **pydantic_function_tool**: Pydanticモデルのツール化
4. **外部API（requests）**: OpenWeatherMap APIレスポンスのモック
5. **デコレータ**: `__wrapped__`属性でバイパス

### Function Call特有のテスト戦略
1. **parsed_arguments**: Pydanticモデルインスタンスの検証
2. **複数ツール**: WeatherRequestとNewsRequestの同時処理
3. **Enum型**: Unit.celsius/fahrenheitの型安全性
4. **入れ子構造**: TaskリストのあるProjectRequest

## 📈 改善提案

### 短期的改善
1. SimpleDataExtractionDemoのテスト追加
2. MultipleEntityExtractionDemoのテスト追加
3. ComplexQueryDemoのテスト追加
4. DynamicEnumDemoのテスト追加
5. ChainOfThoughtDemoのテスト追加

### 中期的改善
1. _display_with_infoメソッドの詳細テスト
2. 右ペイン情報パネルの表示テスト
3. Function Call結果の詳細検証

### 長期的改善
1. 実際のOpenAI APIレスポンス構造の再現
2. 複数Function Call並列実行のテスト
3. パフォーマンステストの追加

## 未テストのデモクラス
以下のデモクラスは基本構造が他のデモと同様のため、主要なデモのテストでカバレッジを確保：
- SimpleDataExtractionDemo
- MultipleEntityExtractionDemo
- ComplexQueryDemo
- DynamicEnumDemo
- ChainOfThoughtDemo

これらは必要に応じて個別にテストを追加可能です。