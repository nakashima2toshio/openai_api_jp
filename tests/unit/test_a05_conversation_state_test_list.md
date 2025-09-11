# a05_conversation_state.py テスト項目一覧表

## 📋 テスト概要
- **対象ファイル**: `a05_conversation_state.py`
- **テストファイル**: `tests/unit/test_a05_conversation_state.py`
- **総テスト数**: 32項目
- **テスト対象**: Conversation State Management API デモアプリケーション

## 🧪 テスト項目詳細

### 1. ページ設定テスト (TestPageConfig)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 1 | `test_setup_page_config_success` | ページ設定の正常実行 | Streamlitページ設定が正しく呼ばれることを確認 | ✅ |
| 2 | `test_setup_page_config_already_set` | 設定済みエラーの処理 | StreamlitAPIExceptionが発生してもクラッシュしないことを確認 | ✅ |

### 2. 共通UIテスト (TestCommonUI)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 3 | `test_setup_common_ui` | 共通UI設定の動作確認 | 会話モデル選択UIが正しく動作することを確認 | ✅ |
| 4 | `test_setup_sidebar_panels` | サイドバーパネル設定 | 会話状態管理用情報パネルが表示されることを確認 | ✅ |

### 3. UIHelper拡張テスト (TestUIHelper)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 5 | `test_create_conversation_controls` | 会話制御UI作成 | 新規会話/継続ボタンの生成を確認 | ✅ |
| 6 | `test_display_previous_response_id` | 前回レスポンスID表示 | previous_response_idの表示を確認 | ✅ |
| 7 | `test_create_debug_toggle` | デバッグトグル作成 | デバッグモード切り替えUIを確認 | ✅ |

### 4. InfoPanelManager拡張テスト (TestInfoPanelManager)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 8 | `test_show_conversation_state_info` | 会話状態情報表示 | 会話履歴とレスポンスID情報の表示を確認 | ✅ |
| 9 | `test_show_stateful_cost_info` | ステートフル料金情報表示 | 会話継続時の料金計算を確認 | ✅ |

### 5. ステートフル会話デモテスト (TestStatefulConversationDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 10 | `test_initialization` | インスタンス初期化 | デモ名とモデル設定を確認 | ✅ |
| 11 | `test_run_method` | runメソッドの実行 | 会話UIの表示を確認 | ✅ |
| 12 | `test_handle_new_conversation` | 新規会話処理 | previous_response_idなしでの会話開始を確認 | ✅ |
| 13 | `test_handle_continued_conversation` | 継続会話処理 | previous_response_idを使用した会話継続を確認 | ✅ |
| 14 | `test_previous_response_id_usage` | previous_response_id使用確認 | IDが正しくAPIに渡されることを確認 | ✅ |
| 15 | `test_conversation_history_management` | 会話履歴管理 | 複数ターンの会話履歴保持を確認 | ✅ |
| 16 | `test_debug_mode_display` | デバッグモード表示 | デバッグ情報の表示を確認 | ✅ |

### 6. Web検索パースデモテスト (TestWebSearchParseDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 17 | `test_initialization` | インスタンス初期化 | デモ名とモデル設定を確認 | ✅ |
| 18 | `test_run_method` | runメソッドの実行 | Web検索UIの表示を確認 | ✅ |
| 19 | `test_search_with_tools` | ツール使用検索 | web_search_previewツールの使用を確認 | ✅ |
| 20 | `test_structured_parsing` | 構造化パース処理 | Pydanticモデルでのレスポンス解析を確認 | ✅ |
| 21 | `test_web_search_tool_invocation` | Web検索ツール実行 | ツール呼び出しの詳細を確認 | ✅ |
| 22 | `test_parse_response_structure` | レスポンス構造解析 | 構造化されたデータの取得を確認 | ✅ |

### 7. デモセレクターテスト (TestDemoSelector)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 23 | `test_initialization` | DemoSelector初期化 | 2つのデモインスタンスが作成されることを確認 | ✅ |
| 24 | `test_run_method` | runメソッドの実行 | デモ選択と実行の流れを確認 | ✅ |
| 25 | `test_demo_switching` | デモ切り替え | 複数デモ間の切り替えを確認 | ✅ |

### 8. エラーハンドリングテスト (TestErrorHandling)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 26 | `test_api_error_handling` | APIエラー処理 | API呼び出しエラー時の処理を確認 | ✅ |
| 27 | `test_invalid_response_id` | 無効なレスポンスID処理 | 不正なprevious_response_idの処理を確認 | ✅ |
| 28 | `test_session_state_error` | セッション状態エラー | セッション状態異常時の処理を確認 | ✅ |
| 29 | `test_tool_execution_error` | ツール実行エラー | Web検索ツールエラーの処理を確認 | ✅ |

### 9. 統合テスト (TestIntegration)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 30 | `test_main_function` | main関数の実行 | DemoSelector作成と実行を確認 | ✅ |
| 31 | `test_main_no_api_key` | APIキーなしの実行 | APIキー未設定時のエラー処理を確認 | ✅ |
| 32 | `test_end_to_end_conversation` | エンドツーエンド会話 | 完全な会話フローを確認 | ✅ |

## 📊 テストカバレージ

### カバーされている主要機能
- ✅ ページ設定とエラーハンドリング
- ✅ 会話状態管理（previous_response_id）
- ✅ 2つの会話管理デモクラス
  - StatefulConversationDemo（ステートフル会話）
  - WebSearchParseDemo（Web検索と構造化パース）
- ✅ DemoSelectorによるデモ選択と実行
- ✅ 会話履歴の保持と継続
- ✅ Web検索ツール（web_search_preview）の使用
- ✅ デバッグモード機能

### 特徴的なテスト内容
- **previous_response_id**: 会話の継続性を保つIDの管理
- **Web検索ツール**: web_search_previewによる検索実行
- **構造化パース**: Pydanticモデルでの応答解析
- **会話履歴**: 複数ターンの会話管理
- **デバッグモード**: 詳細情報の表示制御
- **セッション状態**: Streamlitセッション管理

## 🔧 テスト技術詳細

### 使用したモック技術
1. **Streamlitコンポーネント**: `@patch`デコレータで完全モック化
2. **OpenAI Responses API**: responses.create()とresponses.parse()のモック
3. **Web検索ツール**: web_search_previewツールのモック
4. **セッション状態**: MagicMockでのセッション管理
5. **レスポンスID**: UUIDベースのIDモック

### 会話状態管理特有のテスト戦略
1. **ステートフル会話**: previous_response_idの追跡と使用
2. **会話履歴**: メッセージ配列の管理と検証
3. **ツール実行**: 関数呼び出しの詳細モック
4. **構造化データ**: Pydanticモデルでの検証
5. **デバッグ情報**: 詳細ログの表示制御

## 📈 改善提案

### 短期的改善
1. レスポンスIDの有効期限テスト
2. 会話履歴のサイズ制限テスト
3. ツール実行タイムアウトのテスト

### 中期的改善
1. 複数ツールの並列実行テスト
2. 会話コンテキストの圧縮テスト
3. ストリーミングレスポンスのテスト

### 長期的改善
1. 実際のWeb検索APIとの統合テスト
2. 長時間会話のパフォーマンステスト
3. 会話状態の永続化テスト

## 未実装機能のテスト候補
- 会話の分岐と統合
- 複数会話の並列管理
- 会話のエクスポート/インポート
- 会話要約機能
- コンテキスト自動圧縮