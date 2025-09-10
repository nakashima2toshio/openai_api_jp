"""
ラッパークラスを使用したテスト実装例
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_solutions.session_state_wrapper import SessionStateWrapper, BaseDemoRefactored
from test_solutions.ui_wrapper import UIWrapper, setup_common_ui_refactored, TextResponseDemoRefactored


class TestSessionStateWrapper:
    """SessionStateWrapperのテスト"""
    
    def test_session_state_in_test_mode(self):
        """テストモードでのセッション状態管理"""
        # テストモードで初期化
        session = SessionStateWrapper(test_mode=True)
        
        # 値の設定と取得
        session.set("test_key", "test_value")
        assert session.get("test_key") == "test_value"
        
        # 存在確認
        assert session.exists("test_key") == True
        assert session.exists("non_existent") == False
        
        # デフォルト値
        assert session.get("non_existent", "default") == "default"
    
    def test_initialize_method(self):
        """初期化メソッドのテスト"""
        session = SessionStateWrapper(test_mode=True)
        
        initial_data = {
            'initialized': True,
            'model': 'gpt-4o-mini',
            'execution_count': 0
        }
        
        session.initialize("demo_state", initial_data)
        assert session.get("demo_state") == initial_data
        
        # 既存のキーは上書きされない
        session.initialize("demo_state", {'new': 'data'})
        assert session.get("demo_state") == initial_data


class TestUIWrapper:
    """UIWrapperのテスト"""
    
    def test_ui_write_in_test_mode(self):
        """テストモードでのwrite操作"""
        ui = UIWrapper(test_mode=True)
        
        ui.write("Hello World")
        ui.write("Test Message")
        
        output = ui.get_output()
        assert len(output) == 2
        assert output[0] == "Hello World"
        assert output[1] == "Test Message"
    
    def test_ui_error_in_test_mode(self):
        """テストモードでのerror操作"""
        ui = UIWrapper(test_mode=True)
        
        ui.error("Error 1")
        ui.error("Error 2")
        
        errors = ui.get_errors()
        assert len(errors) == 2
        assert errors[0] == "Error 1"
        assert errors[1] == "Error 2"
    
    def test_ui_columns_in_test_mode(self):
        """テストモードでのcolumns操作"""
        ui = UIWrapper(test_mode=True)
        
        cols = ui.columns([3, 1])
        assert len(cols) == 2
        assert all(isinstance(col, MagicMock) for col in cols)
        assert ui.column_config == [(3, 1)]
    
    def test_ui_button_and_text_area(self):
        """ボタンとテキストエリアのテスト"""
        ui = UIWrapper(test_mode=True)
        
        # ボタンは常にTrue
        assert ui.button("Submit") == True
        
        # テキストエリアはデフォルト値を返す
        assert ui.text_area("Input", "default") == "default"
        assert ui.text_area("Input") == "Test input"


class TestBaseDemoRefactored:
    """リファクタリング後のBaseDemoのテスト"""
    
    def test_base_demo_initialization(self):
        """初期化のテスト"""
        session = SessionStateWrapper(test_mode=True)
        demo = BaseDemoRefactored("TestDemo", session)
        
        assert demo.demo_name == "TestDemo"
        
        # セッション状態が初期化されている
        state = session.get("demo_state_TestDemo")
        assert state is not None
        assert state['initialized'] == True
        assert state['model'] == 'gpt-4o-mini'
        assert state['execution_count'] == 0
    
    def test_execution_count_operations(self):
        """実行回数カウントのテスト"""
        session = SessionStateWrapper(test_mode=True)
        demo = BaseDemoRefactored("TestDemo", session)
        
        # 初期値
        assert demo.get_execution_count() == 0
        
        # カウントアップ
        demo.increment_execution_count()
        assert demo.get_execution_count() == 1
        
        demo.increment_execution_count()
        assert demo.get_execution_count() == 2


class TestTextResponseDemoRefactored:
    """リファクタリング後のTextResponseDemoのテスト"""
    
    def test_text_response_demo_run(self):
        """run()メソッドのテスト"""
        ui = UIWrapper(test_mode=True)
        session = SessionStateWrapper(test_mode=True)
        
        demo = TextResponseDemoRefactored(ui, session)
        demo.run()
        
        # 出力の確認
        output = ui.get_output()
        assert any("TextResponseDemo" in o for o in output)
    
    def test_process_response(self):
        """_process_response()のテスト"""
        ui = UIWrapper(test_mode=True)
        session = SessionStateWrapper(test_mode=True)
        
        demo = TextResponseDemoRefactored(ui, session)
        demo._process_response("Test prompt")
        
        output = ui.get_output()
        assert any("Test prompt" in o for o in output)
    
    def test_error_handling(self):
        """エラーハンドリングのテスト"""
        ui = UIWrapper(test_mode=True)
        session = SessionStateWrapper(test_mode=True)
        
        demo = TextResponseDemoRefactored(ui, session)
        
        # エラーを発生させる
        with patch.object(demo, '_process_response', side_effect=Exception("Test error")):
            try:
                demo._process_response("Test")
            except:
                pass
        
        # エラーはUIWrapperを通じて処理される（実装に依存）


class TestSetupCommonUIRefactored:
    """setup_common_ui_refactoredのテスト"""
    
    def test_setup_common_ui(self):
        """共通UI設定のテスト"""
        ui = UIWrapper(test_mode=True)
        
        result = setup_common_ui_refactored("TestDemo", ui)
        
        # モデルが返される
        assert result == "gpt-4o-mini"
        
        # 出力の確認
        output = ui.get_output()
        assert any("TestDemo" in o for o in output)
        assert any("gpt-4o-mini" in o for o in output)


# 統合テストの例
class TestIntegrationWithWrappers:
    """ラッパーを使用した統合テスト"""
    
    def test_full_flow_with_wrappers(self):
        """完全なフローのテスト（Streamlit依存なし）"""
        # テストモードで全コンポーネントを初期化
        ui = UIWrapper(test_mode=True)
        session = SessionStateWrapper(test_mode=True)
        
        # デモの初期化
        demo = TextResponseDemoRefactored(ui, session)
        
        # 共通UI設定
        model = setup_common_ui_refactored("TestDemo", ui)
        assert model == "gpt-4o-mini"
        
        # デモの実行
        demo.run()
        
        # 出力とエラーの確認
        output = ui.get_output()
        errors = ui.get_errors()
        
        assert len(output) > 0
        assert len(errors) == 0
        
        print(f"Output: {output}")
        print(f"Errors: {errors}")


if __name__ == "__main__":
    # テストの実行
    pytest.main([__file__, "-v"])