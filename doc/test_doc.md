# テスト実行ガイド - a00_responses_api.py

## 📊 現在のテスト状況
- **カバレージ**: 20.86% (1165文中922文が未カバー)
- **テスト結果**: 3件成功、10件失敗、1件警告
- **最終更新**: 2025-09-10

## ✅ 保存されるファイル

### 1. カバレージデータ
```bash
.coverage              # SQLiteデータベース形式のカバレージ情報
coverage.xml           # XML形式のレポート（CI/CD用）※make test-covで生成
```

### 2. HTMLレポート
```bash
htmlcov/
├── index.html         # メインページ
├── a00_responses_api_py.html  # 詳細カバレージ
├── class_index.html   # クラス別インデックス
└── function_index.html # 関数別インデックス
```

## 🚀 実践的な使い方

### 開発フロー

1. make test-a00           # テスト実行
2. make test-a00-html      # カバレージ確認
3. make coverage-report    # ブラウザで詳細確認
4. コード修正
5. make test-quick         # 失敗したテストのみ再実行
6. make clean              # キャッシュクリア（必要時）


