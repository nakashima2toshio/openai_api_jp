#!/bin/bash

# 一括テストとカバレージ測定スクリプト
# 6つのOpenAI APIデモモジュールのテストを実行

echo "=========================================="
echo "OpenAI APIデモ 一括テスト実行"
echo "=========================================="

# テスト対象モジュール
MODULES=(
    "a00_responses_api"
    "a01_structured_outputs_parse_schema"
    "a02_responses_tools_pydantic_parse"
    "a03_images_and_vision"
    "a04_audio_speeches"
    "a05_conversation_state"
    "a06_reasoning_chain_of_thought"
)

# 1. 個別テスト実行（詳細確認用）
echo ""
echo "1. 個別モジュールテスト実行"
echo "------------------------------------------"
for module in "${MODULES[@]}"; do
    echo "Testing $module..."
    python -m pytest tests/unit/test_${module}.py -q
    if [ $? -eq 0 ]; then
        echo "✅ $module: PASSED"
    else
        echo "❌ $module: FAILED"
    fi
done

# 2. 一括テスト実行（サマリー）
echo ""
echo "2. 一括テスト実行（サマリー）"
echo "------------------------------------------"
python -m pytest tests/unit/test_a0*.py --tb=short

# 3. カバレージ測定
echo ""
echo "3. カバレージ測定"
echo "------------------------------------------"
python -m pytest tests/unit/test_a0[0-6]*.py \
    --cov=a00_responses_api \
    --cov=a01_structured_outputs_parse_schema \
    --cov=a02_responses_tools_pydantic_parse \
    --cov=a03_images_and_vision \
    --cov=a04_audio_speeches \
    --cov=a05_conversation_state \
    --cov=a06_reasoning_chain_of_thought \
    --cov-report=term-missing \
    --cov-report=html

# 4. HTMLカバレージレポート生成
echo ""
echo "4. HTMLカバレージレポート"
echo "------------------------------------------"
echo "HTMLレポートが生成されました: htmlcov/index.html"
echo "ブラウザで開く: open htmlcov/index.html"

# 5. テスト統計
echo ""
echo "5. テスト統計"
echo "------------------------------------------"
TOTAL_TESTS=$(python -m pytest tests/unit/test_a0*.py --co -q | wc -l)
echo "総テスト数: $TOTAL_TESTS"

# 6. 各モジュールのテスト数
echo ""
echo "6. モジュール別テスト数"
echo "------------------------------------------"
for module in "${MODULES[@]}"; do
    count=$(python -m pytest tests/unit/test_${module}.py --co -q 2>/dev/null | wc -l)
    echo "$module: $count tests"
done

echo ""
echo "=========================================="
echo "テスト実行完了"
echo "=========================================="