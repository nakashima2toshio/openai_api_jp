# OpenAI APIデモ 個別モジュールテストガイド

## 📚 目次
1. [a00_responses_api.py テストガイド](#a00_responses_apipy-テストガイド)
2. [a01_structured_outputs_parse_schema.py テストガイド](#a01_structured_outputs_parse_schemapy-テストガイド)
3. [a02_responses_tools_pydantic_parse.py テストガイド](#a02_responses_tools_pydantic_parsepy-テストガイド)
4. [a03_images_and_vision.py テストガイド](#a03_images_and_visionpy-テストガイド)
5. [a04_audio_speeches.py テストガイド](#a04_audio_speechespy-テストガイド)
6. [a05_conversation_state.py テストガイド](#a05_conversation_statepy-テストガイド)
7. [a06_reasoning_chain_of_thought.py テストガイド](#a06_reasoning_chain_of_thoughtpy-テストガイド)

---

## a00_responses_api.py テストガイド

### モジュール概要
基本的なOpenAI Responses APIの使用例を実装したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a00_responses_api.py`
- **テスト数**: 33
- **カバレージ**: 34%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 |
|---------|-----------|---------|
| TestPageConfig | ページ設定のテスト | 2 |
| TestCommonUI | 共通UI関数のテスト | 1 |
| TestBaseDemoClass | 基底クラスのテスト | 3 |
| TestTextResponseDemo | テキスト応答デモのテスト | 2 |
| TestStructuredOutputDemo | 構造化出力デモのテスト | 2 |
| TestWeatherDemo | 天気APIデモのテスト | 3 |
| TestImageResponseDemo | 画像応答デモのテスト | 2 |
| TestMemoryResponseDemo | メモリ応答デモのテスト | 2 |
| TestMainApp | メインアプリのテスト | 1 |
| TestErrorHandling | エラーハンドリングのテスト | 1 |
| TestIntegration | 統合テスト | 1 |

### 実行コマンド

```bash
# 基本実行
python -m pytest tests/unit/test_a00_responses_api.py -v

# カバレージ付き
python -m pytest tests/unit/test_a00_responses_api.py \
  --cov=a00_responses_api \
  --cov-report=term-missing

# 特定のクラスのみ
python -m pytest tests/unit/test_a00_responses_api.py::TestTextResponseDemo -v

# 特定のテストのみ
python -m pytest tests/unit/test_a00_responses_api.py::TestTextResponseDemo::test_process_query -v
```

### 主要なモック対象
- Streamlitコンポーネント（st.button, st.text_area, st.write等）
- OpenAI APIクライアント（responses.create）
- 外部API（OpenWeatherMap, ExchangeRate）

### テストのポイント
1. **API呼び出しの検証**: responses.createが正しいパラメータで呼ばれているか
2. **UI表示の検証**: Streamlitコンポーネントが適切に呼ばれているか
3. **エラーハンドリング**: API例外時の処理が適切か

---

## a01_structured_outputs_parse_schema.py テストガイド

### モジュール概要
構造化出力とPydanticスキーマ検証を使用したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a01_structured_outputs_parse_schema.py`
- **テスト数**: 27
- **カバレージ**: 56%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 |
|---------|-----------|---------|
| TestPageConfig | ページ設定のテスト | 2 |
| TestCommonUI | 共通UI関数のテスト | 1 |
| TestBaseDemoClass | 基底クラスのテスト | 3 |
| TestEventExtractionDemo | イベント抽出デモのテスト | 2 |
| TestMathReasoningDemo | 数学推論デモのテスト | 2 |
| TestUIGenerationDemo | UI生成デモのテスト | 2 |
| TestEntityExtractionDemo | エンティティ抽出デモのテスト | 2 |
| TestConditionalSchemaDemo | 条件スキーマデモのテスト | 2 |
| TestModerationDemo | モデレーションデモのテスト | 2 |
| TestMainApp | メインアプリのテスト | 3 |
| TestErrorHandling | エラーハンドリングのテスト | 2 |
| TestIntegration | 統合テスト | 1 |

### 実行コマンド

```bash
# 基本実行
python -m pytest tests/unit/test_a01_structured_outputs_parse_schema.py -v

# カバレージ付き
python -m pytest tests/unit/test_a01_structured_outputs_parse_schema.py \
  --cov=a01_structured_outputs_parse_schema \
  --cov-report=term-missing

# Pydanticモデル関連のテストのみ
python -m pytest tests/unit/test_a01_structured_outputs_parse_schema.py -k "pydantic" -v

# スキーマ検証テストのみ
python -m pytest tests/unit/test_a01_structured_outputs_parse_schema.py -k "schema" -v
```

### Pydanticモデル一覧
- EventInfo（イベント情報）
- MathReasoning（数学的推論）
- DynamicUI（動的UI定義）
- EntityInfo（エンティティ情報）
- ConditionalOutput（条件付き出力）
- ModerationResult（モデレーション結果）

### テストのポイント
1. **Pydanticモデルの検証**: スキーマに従った構造化データの生成
2. **responses.parse()の使用**: 構造化レスポンスの解析
3. **推論モデルの判定**: is_reasoning_model()の動作確認

---

## a02_responses_tools_pydantic_parse.py テストガイド

### モジュール概要
Pydanticツールと関数呼び出し（Function Calling）を使用したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a02_responses_tools_pydantic_parse.py`
- **テスト数**: 23
- **カバレージ**: 45%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 |
|---------|-----------|---------|
| TestPageConfig | ページ設定のテスト | 2 |
| TestCommonUI | 共通UI関数のテスト | 2 |
| TestBaseDemo | 基底クラスのテスト | 2 |
| TestBasicFunctionCallDemo | 基本関数呼び出しデモのテスト | 3 |
| TestNestedStructureDemo | ネスト構造デモのテスト | 2 |
| TestEnumTypeDemo | 列挙型デモのテスト | 2 |
| TestNaturalTextStructuredDemo | 自然言語構造化デモのテスト | 2 |
| TestConversationHistoryDemo | 会話履歴デモのテスト | 2 |
| TestDemoManager | デモマネージャーのテスト | 3 |
| TestErrorHandling | エラーハンドリングのテスト | 2 |
| TestIntegration | 統合テスト | 1 |

### 実行コマンド

```bash
# 基本実行
python -m pytest tests/unit/test_a02_responses_tools_pydantic_parse.py -v

# カバレージ付き
python -m pytest tests/unit/test_a02_responses_tools_pydantic_parse.py \
  --cov=a02_responses_tools_pydantic_parse \
  --cov-report=term-missing

# Function Callingテストのみ
python -m pytest tests/unit/test_a02_responses_tools_pydantic_parse.py::TestBasicFunctionCallDemo -v

# ツール関連のテストのみ
python -m pytest tests/unit/test_a02_responses_tools_pydantic_parse.py -k "tool" -v
```

### Pydanticツール一覧
- GetStockPrice（株価取得）
- GetWeather（天気情報取得）
- ResearchPaper（研究論文構造）
- TaskPriority（タスク優先度）
- NaturalQuery（自然言語クエリ）
- ConversationTurn（会話ターン）

### テストのポイント
1. **pydantic_function_toolの使用**: Pydanticモデルからツール定義生成
2. **関数呼び出しの検証**: ツール実行とレスポンス処理
3. **ネスト構造の処理**: 複雑なデータ構造の検証

---

## a03_images_and_vision.py テストガイド

### モジュール概要
画像生成（DALL-E）とVision APIを使用したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a03_images_and_vision.py`
- **テスト数**: 19（一部未実装によるエラーあり）
- **カバレージ**: 60%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 | 状態 |
|---------|-----------|---------|------|
| TestPageConfig | ページ設定のテスト | 2 | ✅ |
| TestCommonUI | 共通UI関数のテスト | 2 | ✅ |
| TestBaseDemo | 基底クラスのテスト | 2 | ✅ |
| TestURLImageToTextDemo | URL画像からテキスト生成のテスト | 2 | ⚠️ |
| TestBase64ImageToTextDemo | Base64画像からテキスト生成のテスト | 2 | ⚠️ |
| TestPromptToImageDemo | プロンプトから画像生成のテスト | 2 | ✅ |
| TestImageEditDemo | 画像編集デモのテスト | 1 | ❌ |
| TestImageVariationDemo | 画像バリエーションデモのテスト | 1 | ❌ |
| TestDemoManager | デモマネージャーのテスト | 2 | ⚠️ |
| TestErrorHandling | エラーハンドリングのテスト | 2 | ⚠️ |
| TestIntegration | 統合テスト | 1 | ⚠️ |

### 実行コマンド

```bash
# 基本実行（エラーをスキップ）
python -m pytest tests/unit/test_a03_images_and_vision.py -v -k "not (Edit or Variation)"

# カバレージ付き
python -m pytest tests/unit/test_a03_images_and_vision.py \
  --cov=a03_images_and_vision \
  --cov-report=term-missing

# Vision APIテストのみ
python -m pytest tests/unit/test_a03_images_and_vision.py -k "vision or Vision" -v

# DALL-Eテストのみ
python -m pytest tests/unit/test_a03_images_and_vision.py::TestPromptToImageDemo -v
```

### API使用一覧
- **Vision API**: 画像からテキスト生成（responses.create）
- **DALL-E API**: テキストから画像生成（images.generate）
- **画像編集API**: 画像の編集（images.edit）※未実装
- **画像バリエーションAPI**: 画像のバリエーション生成（images.create_variation）※未実装

### テストのポイント
1. **Base64エンコード**: 画像ファイルのBase64変換処理
2. **画像URL処理**: URL画像の取得と処理
3. **DALL-E生成**: プロンプトからの画像生成

---

## a04_audio_speeches.py テストガイド

### モジュール概要
音声合成（TTS）と音声認識（STT）を使用したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a04_audio_speeches.py`
- **テスト数**: 24（一部未実装によるエラーあり）
- **カバレージ**: 41%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 | 状態 |
|---------|-----------|---------|------|
| TestPageConfig | ページ設定のテスト | 2 | ✅ |
| TestCommonUI | 共通UI関数のテスト | 2 | ✅ |
| TestUIHelper | UIヘルパー拡張のテスト | 3 | ✅ |
| TestInfoPanelManager | 情報パネル管理のテスト | 2 | ✅ |
| TestTextToSpeechDemo | テキスト読み上げデモのテスト | 2 | ❌ |
| TestSpeechToTextDemo | 音声文字起こしデモのテスト | 2 | ❌ |
| TestRealtimeVoiceDemo | リアルタイム音声デモのテスト | 1 | ❌ |
| TestAudioComparisonDemo | 音声比較デモのテスト | 2 | ❌ |
| TestDemoSelector | デモセレクターのテスト | 2 | ⚠️ |
| TestErrorHandling | エラーハンドリングのテスト | 2 | ⚠️ |
| TestIntegration | 統合テスト | 2 | ⚠️ |

### 実行コマンド

```bash
# 基本実行（エラーをスキップ）
python -m pytest tests/unit/test_a04_audio_speeches.py -v -k "not (TTS or STT or Realtime or Comparison)"

# カバレージ付き
python -m pytest tests/unit/test_a04_audio_speeches.py \
  --cov=a04_audio_speeches \
  --cov-report=term-missing

# UIテストのみ
python -m pytest tests/unit/test_a04_audio_speeches.py -k "UI" -v

# 音声モデル関連のテストのみ
python -m pytest tests/unit/test_a04_audio_speeches.py -k "audio or Audio" -v
```

### API使用一覧
- **TTS API**: テキストから音声生成（audio.speech.create）
- **STT API**: 音声からテキスト生成（audio.transcriptions.create）
- **Whisper API**: 音声認識（audio.transcriptions.create）
- **リアルタイムAPI**: WebSocket接続での音声処理

### テストのポイント
1. **音声ファイル処理**: BytesIOでの音声データモック
2. **音声モデル選択**: TTS/STTモデルの選択UI
3. **料金計算**: 文字数/時間に基づく料金計算

---

## a05_conversation_state.py テストガイド

### モジュール概要
会話状態管理とprevious_response_idを使用した継続的な会話を実装したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a05_conversation_state.py`
- **テスト数**: 21
- **カバレージ**: 51%

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 |
|---------|-----------|---------|
| TestPageConfig | ページ設定のテスト | 2 |
| TestCommonUI | 共通UI関数のテスト | 2 |
| TestBaseDemo | 基底クラスのテスト | 2 |
| TestStatefulConversationDemo | ステートフル会話デモのテスト | 4 |
| TestWebSearchParseDemo | Web検索パースデモのテスト | 3 |
| TestMultiStepWorkflowDemo | マルチステップワークフローのテスト | 1 |
| TestDemoManager | デモマネージャーのテスト | 2 |
| TestErrorHandling | エラーハンドリングのテスト | 2 |
| TestConversationStateFeatures | 会話状態機能のテスト | 2 |
| TestIntegration | 統合テスト | 1 |

### 実行コマンド

```bash
# 基本実行
python -m pytest tests/unit/test_a05_conversation_state.py -v

# カバレージ付き
python -m pytest tests/unit/test_a05_conversation_state.py \
  --cov=a05_conversation_state \
  --cov-report=term-missing

# ステートフル会話テストのみ
python -m pytest tests/unit/test_a05_conversation_state.py::TestStatefulConversationDemo -v

# previous_response_id関連のテスト
python -m pytest tests/unit/test_a05_conversation_state.py -k "previous_response_id" -v
```

### 主要機能
- **previous_response_id**: 会話の継続性を保つID管理
- **Web検索ツール**: web_search_previewツールの使用
- **構造化パース**: Pydanticモデルでの応答解析
- **会話履歴管理**: 複数ターンの会話保持

### テストのポイント
1. **会話継続性**: previous_response_idが正しく渡されているか
2. **Web検索ツール**: ツール定義と実行の検証
3. **セッション状態**: Streamlitセッション管理の確認

---

## a06_reasoning_chain_of_thought.py テストガイド

### モジュール概要
Chain of Thought（CoT）推論パターンを実装したデモモジュール

### テスト構成
- **テストファイル**: `tests/unit/test_a06_reasoning_chain_of_thought.py`
- **テスト数**: 28
- **カバレージ**: 87%（最高カバレージ）

### テストクラス一覧

| クラス名 | テスト内容 | テスト数 |
|---------|-----------|---------|
| TestPageConfig | ページ設定のテスト | 2 |
| TestCommonUI | 共通UI関数のテスト | 2 |
| TestBaseDemo | 基底クラスのテスト | 2 |
| TestStepByStepReasoningDemo | 段階的推論デモのテスト | 3 |
| TestHypothesisTestDemo | 仮説検証デモのテスト | 2 |
| TestTreeOfThoughtDemo | 思考の木デモのテスト | 3 |
| TestProsConsDecisionDemo | 賛否比較決定デモのテスト | 2 |
| TestPlanExecuteReflectDemo | 計画実行振り返りデモのテスト | 2 |
| TestDemoManager | デモマネージャーのテスト | 3 |
| TestReasoningPatterns | 推論パターンのテスト | 3 |
| TestErrorHandling | エラーハンドリングのテスト | 2 |
| TestIntegration | 統合テスト | 2 |

### 実行コマンド

```bash
# 基本実行
python -m pytest tests/unit/test_a06_reasoning_chain_of_thought.py -v

# カバレージ付き
python -m pytest tests/unit/test_a06_reasoning_chain_of_thought.py \
  --cov=a06_reasoning_chain_of_thought \
  --cov-report=term-missing

# 推論パターンテストのみ
python -m pytest tests/unit/test_a06_reasoning_chain_of_thought.py::TestReasoningPatterns -v

# Tree of Thoughtテストのみ
python -m pytest tests/unit/test_a06_reasoning_chain_of_thought.py::TestTreeOfThoughtDemo -v
```

### 推論パターン一覧
1. **Step-by-Step Reasoning**: 段階的推論
2. **Hypothesis-Test**: 仮説検証推論
3. **Tree of Thought**: 思考の木（分岐探索）
4. **Pros-Cons-Decision**: 賛否比較決定
5. **Plan-Execute-Reflect**: 計画実行振り返り

### テストのポイント
1. **システムプロンプト検証**: 各推論パターンの指示内容確認
2. **構造化出力**: セクション分けされた出力形式
3. **信頼度スコア**: 0-1での推論結果評価
4. **右ペイン情報**: Tree of Thoughtでの探索情報表示

---

## 共通テストパターン

### Streamlitコンポーネントのモック
```python
@patch('streamlit.button')
@patch('streamlit.text_area')
def test_ui_components(mock_text_area, mock_button):
    mock_text_area.return_value = "Test input"
    mock_button.return_value = True
    # テスト実行
```

### OpenAI APIのモック
```python
def test_api_call(demo_instance):
    mock_response = MagicMock()
    mock_response.id = "test_id"
    demo_instance.client.responses.create.return_value = mock_response
    # テスト実行
```

### エラーハンドリングのテスト
```python
@patch('streamlit.error')
def test_error_handling(mock_error):
    demo.client.responses.create.side_effect = Exception("API Error")
    # エラー処理のテスト
    mock_error.assert_called()
```

## トラブルシューティング

### よくある問題

1. **ImportError**: 
   - 解決: `export PYTHONPATH=$PYTHONPATH:$(pwd)`

2. **未実装クラスのエラー**:
   - 解決: テストで`pytest.skip()`を使用

3. **モックの不具合**:
   - 解決: `@patch`の順序を確認（下から上へ適用）

4. **カバレージが低い**:
   - 解決: `--cov-report=term-missing`で未カバー行を確認

## まとめ

各モジュールは独自の特徴とテスト要件を持っています：

- **a00**: 基本的なAPI使用（最も基礎的）
- **a01**: Pydanticスキーマ検証（構造化重視）
- **a02**: Function Calling（ツール使用）
- **a03**: 画像処理（マルチモーダル）
- **a04**: 音声処理（音声I/O）
- **a05**: 会話管理（ステート管理）
- **a06**: 推論パターン（最高カバレージ）

各モジュールのテストは独立して実行可能で、特定の機能に焦点を当てたテストが可能です。

---

最終更新: 2025年9月11日