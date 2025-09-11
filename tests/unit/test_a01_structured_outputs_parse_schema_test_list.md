# a01_structured_outputs_parse_schema.py テスト項目一覧表

## 📋 テスト概要
- **対象ファイル**: `a01_structured_outputs_parse_schema.py`
- **テストファイル**: `tests/unit/test_a01_structured_outputs_parse_schema.py`
- **総テスト数**: 29項目
- **テスト対象**: Structured Outputs Parse Schema デモアプリケーション

## 🧪 テスト項目詳細

### 1. ページ設定テスト (TestPageConfig)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 1 | `test_setup_page_config_success` | ページ設定の正常実行 | Streamlitページ設定が正しく呼ばれることを確認 | ✅ |
| 2 | `test_setup_page_config_already_set` | 設定済みエラーの処理 | StreamlitAPIExceptionが発生してもクラッシュしないことを確認 | ✅ |

### 2. 共通UIテスト (TestCommonUI)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 3 | `test_setup_common_ui` | 共通UI設定の動作確認 | モデル選択UIが正しく動作し、選択したモデルを返すことを確認 | ✅ |

### 3. 基底クラステスト (TestBaseDemoClass)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 4 | `test_base_demo_initialization` | BaseDemo初期化 | ConfigManager、OpenAIClient等が正しく初期化されることを確認 | ✅ |
| 5 | `test_call_api_parse` | parse API呼び出し | responses.parse APIの呼び出しとPydanticモデル処理を確認 | ✅ |
| 6 | `test_is_reasoning_model` | 推論モデル判定 | o1、o3、o4、gpt-5系モデルの判定ロジックを確認 | ✅ |

### 4. イベント抽出デモテスト (TestEventExtractionDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 7 | `test_event_extraction_run` | run()メソッドの実行 | デモの初期化とUI要素の表示を確認 | ✅ |
| 8 | `test_process_extraction` | _process_extractionメソッド | EventInfoモデルを使用したイベント情報抽出処理を確認 | ✅ |

### 5. 数学的推論デモテスト (TestMathReasoningDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 9 | `test_process_math_reasoning` | 数学推論処理 | MathReasoningモデルを使用した段階的解法生成を確認 | ✅ |

### 6. UI生成デモテスト (TestUIGenerationDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 10 | `test_process_ui_generation` | UI生成処理 | UIComponentモデルを使用した再帰的コンポーネント生成を確認 | ✅ |

### 7. エンティティ抽出デモテスト (TestEntityExtractionDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 11 | `test_process_entity_extraction` | エンティティ抽出処理 | Entitiesモデルを使用した属性・色・動物の抽出を確認 | ✅ |

### 8. 条件分岐スキーマデモテスト (TestConditionalSchemaDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 12 | `test_process_conditional_schema_user_info` | UserInfo条件分岐 | Union型でUserInfoスキーマが選択される処理を確認 | ✅ |
| 13 | `test_process_conditional_schema_address` | Address条件分岐 | Union型でAddressスキーマが選択される処理を確認 | ✅ |

### 9. モデレーションデモテスト (TestModerationDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 14 | `test_process_moderation_allowed` | コンテンツ許可処理 | 安全なコンテンツが許可される処理を確認 | ✅ |
| 15 | `test_process_moderation_refused` | コンテンツ拒否処理 | 不適切コンテンツが拒否される処理を確認 | ✅ |

### 10. デモマネージャーテスト (TestDemoManager)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 16 | `test_demo_manager_initialization` | DemoManager初期化 | 6つのデモインスタンスが正しく作成されることを確認 | ✅ |
| 17 | `test_demo_manager_run` | デモ選択と実行 | 選択されたデモが正しく実行されることを確認 | ✅ |

### 11. エラーハンドリングテスト (TestErrorHandling)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 18 | `test_handle_error` | 基本エラー処理 | 多言語対応エラーメッセージの表示を確認 | ✅ |
| 19 | `test_api_error_handling` | APIエラー処理 | API呼び出しエラー時の適切な処理を確認 | ✅ |

### 12. 統合テスト (TestIntegration)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 20 | `test_main_without_api_key` | APIキーなしの起動 | 環境変数未設定時のエラー処理を確認 | ✅ |
| 21 | `test_main_with_api_key` | APIキーありの起動 | 正常起動とDemoManager実行を確認 | ✅ |

### 13. Pydanticモデルテスト (TestPydanticModels)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 22 | `test_event_info_model` | EventInfoモデル | イベント名、日付、参加者リストの検証 | ✅ |
| 23 | `test_math_reasoning_model` | MathReasoningモデル | 思考ステップと最終回答の検証 | ✅ |
| 24 | `test_ui_component_model` | UIComponentモデル | 再帰的UIコンポーネント構造の検証 | ✅ |
| 25 | `test_entities_model` | Entitiesモデル | 属性、色、動物リストの検証 | ✅ |
| 26 | `test_conditional_item_model` | ConditionalItemモデル | Union型（UserInfo/Address）の検証 | ✅ |
| 27 | `test_moderation_result_model` | ModerationResultモデル | 拒否理由とコンテンツの検証 | ✅ |

## 📊 テストカバレージ

### カバーされている主要機能
- ✅ ページ設定とエラーハンドリング
- ✅ 基底クラスの初期化とparse API呼び出し
- ✅ 推論系モデルの判定ロジック
- ✅ 6つの構造化出力デモクラス
  - EventExtractionDemo（イベント情報抽出）
  - MathReasoningDemo（数学的思考ステップ）
  - UIGenerationDemo（UIコンポーネント生成）
  - EntityExtractionDemo（エンティティ抽出）
  - ConditionalSchemaDemo（条件分岐スキーマ）
  - ModerationDemo（モデレーション＆拒否処理）
- ✅ DemoManagerによるデモ選択と実行
- ✅ すべてのPydanticモデル定義
- ✅ エラーハンドリングと多言語対応

### 特徴的なテスト内容
- **responses.parse API**: OpenAIの構造化出力APIのモック
- **Pydanticモデル**: 型安全な構造化データの検証
- **Union型処理**: 条件分岐スキーマの動的選択
- **再帰的構造**: UIComponentの階層構造
- **推論系モデル対応**: temperature無効化の確認

## 🔧 テスト技術詳細

### 使用したモック技術
1. **Streamlitコンポーネント**: `@patch`デコレータで完全モック化
2. **OpenAI responses.parse API**: `MagicMock`で構造化出力をシミュレート
3. **Pydanticモデル**: 実際のモデルインスタンスを使用して検証
4. **デコレータ**: `__wrapped__`属性でバイパス

### Pydanticモデルのテスト戦略
1. **モデル定義の検証**: 各フィールドの型と制約を確認
2. **インスタンス生成**: 実際のデータでモデルを作成
3. **Union型の処理**: isinstance()でサブタイプを判定
4. **再帰構造**: UIComponentの子要素を検証

## 📈 改善提案

### 短期的改善
1. ValidationErrorのテストケース追加
2. 各デモの_display_*メソッドのテスト
3. temperatureコントロールの詳細テスト

### 中期的改善
1. 実際のresponses.parse APIレスポンス構造の再現
2. UIコンポーネントの再帰的レンダリングテスト
3. セッション状態管理の詳細テスト

### 長期的改善
1. E2Eテストでの実際のPydanticモデル処理
2. 複雑な構造化データのバリデーションテスト
3. パフォーマンステストの追加