# Makefile for OpenAI API JP Project Testing

.PHONY: test test-cov test-unit test-integration test-a00 test-a00-all test-a00-all-html clean help

help:  ## ヘルプを表示
	@echo "使用可能なコマンド:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test:  ## すべてのテストを実行
	pytest tests/ -v

test-cov:  ## カバレージ付きでテストを実行しHTMLレポートを生成
	pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "カバレージレポート: htmlcov/index.html"

test-unit:  ## 単体テストのみ実行
	pytest tests/unit/ -v

test-integration:  ## 統合テストのみ実行
	pytest tests/integration/ -v

test-a00:  ## a00_responses_api.pyのテストのみ実行
	pytest tests/unit/test_a00_responses_api.py -v --cov=a00_responses_api --cov-report=term-missing

test-a00-html:  ## a00_responses_api.pyのカバレージHTMLレポートを生成
	pytest tests/unit/test_a00_responses_api.py --cov=a00_responses_api --cov-report=html --cov-report=term
	@echo "カバレージレポート: htmlcov/index.html"
	@echo "ブラウザで開く: open htmlcov/index.html"

test-quick:  ## 失敗したテストのみ再実行（高速）
	pytest --lf -v

test-parallel:  ## テストを並列実行（要: pytest-xdist）
	pytest -n auto tests/

clean:  ## テスト関連のキャッシュをクリーンアップ
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

coverage-report:  ## カバレージレポートをブラウザで開く
	@if [ -f htmlcov/index.html ]; then \
		open htmlcov/index.html; \
	else \
		echo "レポートが見つかりません。先に 'make test-cov' を実行してください。"; \
	fi

install-test-deps:  ## テスト用の追加依存パッケージをインストール
	pip install pytest-xdist pytest-sugar pytest-randomly pytest-benchmark

# デフォルトターゲット
all: test-cov

# 追加: a00 の両テスト（通常版 + fixed版）をまとめて実行するターゲット
test-a00-all:  ## a00 の両テストを実行（fixed含む）
	pytest tests/unit/test_a00_responses_api.py tests/unit/test_a00_responses_api_fixed.py -v

test-a00-all-html:  ## a00 の両テストをHTMLカバレッジ付きで実行
	pytest tests/unit/test_a00_responses_api.py tests/unit/test_a00_responses_api_fixed.py --cov=a00_responses_api --cov-report=html --cov-report=term
	@echo "カバレッジレポート: htmlcov/index.html"
