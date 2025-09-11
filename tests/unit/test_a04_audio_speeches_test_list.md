# a04_audio_speeches.py テスト項目一覧表

## 📋 テスト概要
- **対象ファイル**: `a04_audio_speeches.py`
- **テストファイル**: `tests/unit/test_a04_audio_speeches.py`
- **総テスト数**: 24項目
- **テスト対象**: Audio & Speech API デモアプリケーション

## 🧪 テスト項目詳細

### 1. ページ設定テスト (TestPageConfig)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 1 | `test_setup_page_config_success` | ページ設定の正常実行 | Streamlitページ設定が正しく呼ばれることを確認 | ✅ |
| 2 | `test_setup_page_config_already_set` | 設定済みエラーの処理 | StreamlitAPIExceptionが発生してもクラッシュしないことを確認 | ✅ |

### 2. 共通UIテスト (TestCommonUI)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 3 | `test_setup_common_ui` | 共通UI設定の動作確認 | 音声モデル選択UIが正しく動作することを確認 | ✅ |
| 4 | `test_setup_sidebar_panels` | サイドバーパネル設定 | 音声API用情報パネルが表示されることを確認 | ✅ |

### 3. UIHelper拡張テスト (TestUIHelper)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 5 | `test_select_audio_model` | 音声モデル選択 | TTS/STTモデルの選択UIを確認 | ✅ |
| 6 | `test_select_voice` | 音声種類選択 | 5種類の音声（alloy、nova等）選択を確認 | ✅ |
| 7 | `test_create_audio_download_button` | ダウンロードボタン作成 | MP3ダウンロードボタンの生成を確認 | ✅ |

### 4. InfoPanelManager拡張テスト (TestInfoPanelManager)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 8 | `test_show_audio_model_info_tts` | TTSモデル情報表示 | Text-to-Speechモデル情報の表示を確認 | ✅ |
| 9 | `test_show_audio_cost_info_tts` | TTS料金情報表示 | 文字数に基づく料金計算を確認 | ✅ |

### 5. Text-to-Speechデモテスト (TestTextToSpeechDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 10 | `test_run_method` | runメソッドの実行 | TTSデモUIの表示を確認 | ✅ |
| 11 | `test_generate_speech` | 音声生成処理 | OpenAI TTS APIの呼び出しと音声再生を確認 | ✅ |

### 6. Speech-to-Textデモテスト (TestSpeechToTextDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 12 | `test_run_no_file` | ファイル未アップロード時 | ファイルアップローダーの動作確認 | ✅ |
| 13 | `test_transcribe_audio` | 音声文字起こし処理 | Whisper APIの呼び出しとテキスト表示を確認 | ✅ |

### 7. リアルタイム音声デモテスト (TestRealtimeVoiceDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 14 | `test_run_method` | runメソッドの実行 | リアルタイムAPIのUI表示を確認 | ✅ |

### 8. 音声比較デモテスト (TestAudioComparisonDemo)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 15 | `test_run_method` | runメソッドの実行 | 音声比較UIの表示を確認 | ✅ |
| 16 | `test_compare_voices` | 音声比較処理 | 5種類の音声生成と表示を確認 | ✅ |

### 9. デモセレクターテスト (TestDemoSelector)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 17 | `test_initialization` | DemoSelector初期化 | 4つのデモインスタンスが作成されることを確認 | ✅ |
| 18 | `test_run_method` | runメソッドの実行 | デモ選択と実行の流れを確認 | ✅ |

### 10. エラーハンドリングテスト (TestErrorHandling)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 19 | `test_audio_download_button_error` | ダウンロードエラー処理 | ダウンロードボタンのエラー処理を確認 | ✅ |
| 20 | `test_transcription_error` | 文字起こしエラー処理 | Whisper APIエラー時の処理を確認 | ✅ |

### 11. 統合テスト (TestIntegration)
| No | テスト名 | 説明 | テスト内容 | 状態 |
|----|----------|------|------------|------|
| 21 | `test_main_function` | main関数の実行 | DemoSelector作成と実行を確認 | ✅ |
| 22 | `test_main_no_api_key` | APIキーなしの実行 | APIキー未設定時のエラー処理を確認 | ✅ |

## 📊 テストカバレージ

### カバーされている主要機能
- ✅ ページ設定とエラーハンドリング
- ✅ 音声モデル選択UI（TTS/STT）
- ✅ 4つの音声処理デモクラス
  - TextToSpeechDemo（テキスト読み上げ）
  - SpeechToTextDemo（音声文字起こし）
  - RealtimeVoiceDemo（リアルタイム音声）
  - AudioComparisonDemo（音声比較）
- ✅ DemoSelectorによるデモ選択と実行
- ✅ 音声ファイルのダウンロード機能
- ✅ 料金計算機能

### 特徴的なテスト内容
- **TTS API**: audio.speech.create()での音声生成
- **STT API**: audio.transcriptions.create()での文字起こし
- **音声比較**: 5種類の音声（alloy、nova、echo、onyx、shimmer）生成
- **リアルタイムAPI**: WebSocket接続のモック
- **料金計算**: 文字数/時間に基づく料金計算

## 🔧 テスト技術詳細

### 使用したモック技術
1. **Streamlitコンポーネント**: `@patch`デコレータで完全モック化
2. **OpenAI Audio API**: TTS/STTのレスポンスをモック
3. **音声ファイル**: BytesIOでの音声データモック
4. **ファイルアップロード**: MagicMockでファイルオブジェクトを模擬
5. **非同期処理**: AsyncMockでリアルタイム処理をモック

### 音声処理特有のテスト戦略
1. **音声生成**: バイナリデータの返却をモック
2. **音声再生**: st.audioコンポーネントのモック
3. **文字起こし**: テキスト結果の返却をモック
4. **実行時間計測**: 音声生成/処理時間の測定

## 📈 改善提案

### 短期的改善
1. 音声ファイル形式（MP3、WAV、M4A）のテスト
2. ファイルサイズ制限（25MB）のテスト
3. 文字数制限（4,096文字）のテスト

### 中期的改善
1. ストリーミング音声処理のテスト
2. 複数言語での文字起こしテスト
3. 音声品質（standard/HD）の比較テスト

### 長期的改善
1. 実際の音声ファイルを使用した統合テスト
2. WebSocket接続の詳細テスト（リアルタイムAPI）
3. パフォーマンステストの追加

## 未実装機能のテスト候補
- 音声翻訳機能（audio.translations）
- タイムスタンプ付き文字起こし
- 音声フォーマット変換
- バッチ音声処理