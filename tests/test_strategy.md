# テスト戦略とカバレージ向上ガイド

## 現在のカバレージ状況
- a00_responses_api.py: 16% (1165文中977文が未カバー)

## カバレージ向上のための段階的アプローチ

### 第1段階: 基盤テスト (目標: 30%)
1. **設定・初期化のテスト**
   - setup_page_config() ✅ 完了
   - setup_common_ui() 
   - BaseDemo.__init__()

2. **基本的なデモクラスのテスト**
   - TextResponseDemo.run()
   - MemoryResponseDemo.run()

### 第2段階: 中核機能テスト (目標: 60%)
1. **API呼び出しのテスト**
   - OpenAI API呼び出しのモック
   - レスポンス処理のテスト

2. **エラーハンドリング**
   - API エラー
   - ネットワークエラー
   - 入力検証エラー

### 第3段階: 包括的テスト (目標: 80%)
1. **統合テスト**
   - エンドツーエンドのフロー
   - 複数のデモクラス間の連携

2. **エッジケースのテスト**
   - 空入力
   - 大量データ
   - 同時実行

## テスト作成の優先順位

### 高優先度（すぐに作成すべき）
```python
# 1. デモクラスの初期化を修正
def test_demo_initialization():
    demo = TextResponseDemo("Test Demo")  # demo_name引数を追加
    assert demo.name == "Test Demo"

# 2. API呼び出しのモック
@patch('openai.OpenAI')
def test_api_call(mock_openai):
    # APIレスポンスのモック
    pass

# 3. エラーハンドリング
def test_error_handling():
    # 各種エラーケースのテスト
    pass
```

### 中優先度
- 構造化出力のテスト
- ツール呼び出しのテスト
- 画像処理のテスト

### 低優先度
- UI表示のテスト（Streamlit部分）
- ログ出力のテスト

## カバレージレポートの活用

### HTMLレポートの見方
1. `htmlcov/index.html`を開く
2. 赤い行: テストされていない
3. 黄色い行: 部分的にテストされている
4. 緑の行: 完全にテストされている

### 重要なメトリクス
- **Line Coverage**: 実行された行の割合
- **Branch Coverage**: 条件分岐のカバー率
- **Function Coverage**: テストされた関数の割合

## CI/CDでの活用

### GitHub Actionsの例
```yaml
name: Test Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest-cov
    - name: Run tests with coverage
      run: |
        pytest --cov=. --cov-report=xml --cov-report=term
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## テスト実行のショートカット

### Makefile の作成
```makefile
test:
	pytest tests/

test-cov:
	pytest --cov=. --cov-report=html --cov-report=term

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-watch:
	pytest-watch tests/

clean:
	rm -rf htmlcov/ .coverage .pytest_cache/
```

## トラブルシューティング

### よくある問題と解決策

1. **ImportError**
   - PYTHONPATHの設定を確認
   - conftest.pyでパスを追加

2. **Streamlit関連のエラー**
   - モックを適切に設定
   - @patch デコレータの順序に注意

3. **カバレージが上がらない**
   - exclude_lines設定を確認
   - デコレータやメタクラスの扱い

## 次のステップ

1. ✅ テスト環境のセットアップ完了
2. ⏳ デモクラスの初期化引数を修正
3. ⏳ 基本的なテストケースの追加
4. ⏳ カバレージ30%達成
5. ⏳ CI/CDパイプラインの設定