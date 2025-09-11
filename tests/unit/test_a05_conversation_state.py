"""
a05_conversation_state.py の単体テスト
Conversation State Management デモのテスト
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
import streamlit as st
from pathlib import Path
import sys
import json
from typing import Dict, Any, List
import time
from pydantic import BaseModel, Field

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPageConfig:
    """ページ設定のテスト"""
    
    @patch('streamlit.set_page_config')
    @patch('a05_conversation_state.config')
    def test_setup_page_config_success(self, mock_config, mock_set_page_config):
        """ページ設定が正常に実行される"""
        from a05_conversation_state import setup_page_config
        
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Conversation Title",
            "ui.page_icon": "🔄",
            "ui.layout": "wide"
        }.get(key, default)
        
        setup_page_config()
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Conversation Title",
            page_icon="🔄",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config_already_set(self, mock_set_page_config):
        """既に設定済みの場合はエラーを無視"""
        from a05_conversation_state import setup_page_config
        
        mock_set_page_config.side_effect = st.errors.StreamlitAPIException("Already set")
        
        # エラーが発生してもクラッシュしない
        setup_page_config()


class TestCommonUI:
    """共通UI関数のテスト"""
    
    @patch('streamlit.write')
    def test_setup_common_ui(self, mock_write):
        """共通UI設定が正しく動作する"""
        from a05_conversation_state import setup_common_ui
        
        setup_common_ui("Test Demo", "gpt-4o-mini")
        
        # ヘッダーとモデル表示が呼ばれたことを確認
        assert mock_write.call_count >= 2
    
    @patch('a05_conversation_state.InfoPanelManager')
    @patch('streamlit.sidebar.write')
    def test_setup_sidebar_panels(self, mock_write, mock_info_panel):
        """サイドバーパネル設定のテスト"""
        from a05_conversation_state import setup_sidebar_panels
        
        setup_sidebar_panels("gpt-4o-mini")
        
        # 各情報パネルが呼ばれたことを確認
        mock_info_panel.show_model_info.assert_called_once_with("gpt-4o-mini")
        mock_info_panel.show_session_info.assert_called_once()
        mock_info_panel.show_cost_info.assert_called_once_with("gpt-4o-mini")
        mock_info_panel.show_performance_info.assert_called_once()


class TestBaseDemo:
    """BaseDemoクラスのテスト"""
    
    @patch('a05_conversation_state.sanitize_key')
    def test_base_demo_initialization(self, mock_sanitize):
        """BaseDemoクラスの初期化テスト"""
        from a05_conversation_state import BaseDemo
        
        mock_sanitize.return_value = "test_demo"
        
        # 具象クラスを作成してテスト
        class ConcreteDemo(BaseDemo):
            def run_demo(self):
                pass
        
        demo = ConcreteDemo("Test Demo")
        
        assert demo.demo_name == "Test Demo"
        assert demo.safe_key == "test_demo"
        assert demo.model is None
        assert demo.client is None
    
    @patch('a05_conversation_state.OpenAI')
    @patch('a05_conversation_state.setup_common_ui')
    def test_execute_method(self, mock_setup_ui, mock_openai):
        """executeメソッドのテスト"""
        from a05_conversation_state import BaseDemo
        
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        class TestDemo(BaseDemo):
            def run_demo(self):
                self.demo_executed = True
        
        demo = TestDemo("Test")
        
        # デコレータをバイパスして実行
        demo.execute.__wrapped__.__wrapped__(demo, "gpt-4o-mini")
        
        assert demo.model == "gpt-4o-mini"
        assert demo.demo_executed == True
        mock_setup_ui.assert_called_once_with("Test", "gpt-4o-mini")


class TestStatefulConversationDemo:
    """StatefulConversationDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """StatefulConversationDemoのインスタンスを作成"""
        from a05_conversation_state import StatefulConversationDemo
        
        demo = StatefulConversationDemo("ステートフルな会話継続")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo_initial(self, mock_subheader, mock_code, mock_expander, 
                             mock_write, mock_text_area, mock_button, demo_instance):
        """run_demoメソッドの初回実行テスト"""
        
        mock_text_area.return_value = "Test initial question"
        mock_button.side_effect = [False, False]  # 初回と追加の両方False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called()
            assert mock_button.call_count == 1  # 初回質問ボタンのみ
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    @patch('a05_conversation_state.get_default_messages')
    def test_process_initial_question(self, mock_get_messages, mock_rerun, 
                                     mock_success, mock_spinner, demo_instance):
        """_process_initial_questionメソッドのテスト"""
        
        mock_get_messages.return_value = []
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "test_response_id_123"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_initial_question("Test question")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"initial_response_{demo_instance.safe_key}"] == mock_response
            assert st.session_state[f"initial_query_{demo_instance.safe_key}"] == "Test question"
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_follow_up_question(self, mock_rerun, mock_success, 
                                       mock_spinner, demo_instance):
        """_process_follow_up_questionメソッドのテスト"""
        
        # 初回レスポンスのモック
        mock_initial_response = MagicMock()
        mock_initial_response.id = "initial_response_id"
        
        # 追加質問レスポンスのモック
        mock_follow_up_response = MagicMock()
        mock_follow_up_response.id = "follow_up_response_id"
        demo_instance.client.responses.create.return_value = mock_follow_up_response
        
        with patch('streamlit.session_state', {
            f"initial_response_{demo_instance.safe_key}": mock_initial_response
        }):
            demo_instance._process_follow_up_question("Follow up question")
            
            # previous_response_idが使用されていることを確認
            demo_instance.client.responses.create.assert_called_once_with(
                model="gpt-4o-mini",
                input="Follow up question",
                previous_response_id="initial_response_id"
            )
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
    
    @patch('streamlit.columns')
    @patch('streamlit.subheader')
    @patch('streamlit.write')
    @patch('streamlit.metric')
    @patch('streamlit.code')
    @patch('a05_conversation_state.ResponseProcessorUI')
    def test_display_conversation_results(self, mock_response_ui, mock_code, mock_metric,
                                         mock_write, mock_subheader, mock_columns, demo_instance):
        """_display_conversation_resultsメソッドのテスト"""
        
        # レスポンスのモック
        mock_initial_response = MagicMock()
        mock_initial_response.id = "response_id_123456789"
        mock_initial_response.usage.total_tokens = 500
        
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        with patch('streamlit.session_state', {
            f"initial_response_{demo_instance.safe_key}": mock_initial_response,
            f"initial_query_{demo_instance.safe_key}": "Test query"
        }):
            demo_instance._display_conversation_results()
            
            mock_response_ui.display_response.assert_called_once_with(mock_initial_response)
            mock_subheader.assert_called()
            assert mock_metric.call_count >= 3  # モデル、ステップ、トークン数など


class TestWebSearchParseDemo:
    """WebSearchParseDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """WebSearchParseDemoのインスタンスを作成"""
        from a05_conversation_state import WebSearchParseDemo
        
        demo = WebSearchParseDemo("Web検索と構造化パース")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_input')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander,
                     mock_write, mock_text_input, mock_button, demo_instance):
        """run_demoメソッドの基本的な実行テスト"""
        
        mock_text_input.return_value = "Test search query"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_input.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_execute_web_search(self, mock_rerun, mock_success, mock_spinner, demo_instance):
        """_execute_web_searchメソッドのテスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "search_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._execute_web_search("Test search query")
            
            # Web検索ツールが使用されていることを確認
            call_args = demo_instance.client.responses.create.call_args
            assert call_args[1]['tools'][0]['type'] == 'web_search_preview'
            
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"search_response_{demo_instance.safe_key}"] == mock_response
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_execute_structured_parse(self, mock_rerun, mock_success, 
                                     mock_spinner, demo_instance):
        """_execute_structured_parseメソッドのテスト"""
        
        # 検索レスポンスのモック
        mock_search_response = MagicMock()
        mock_search_response.id = "search_response_id"
        
        # 構造化レスポンスのモック
        mock_structured_response = MagicMock()
        demo_instance.client.responses.parse.return_value = mock_structured_response
        
        with patch('streamlit.session_state', {
            f"search_response_{demo_instance.safe_key}": mock_search_response
        }):
            demo_instance._execute_structured_parse()
            
            # previous_response_idが使用されていることを確認
            demo_instance.client.responses.parse.assert_called_once()
            call_args = demo_instance.client.responses.parse.call_args
            assert call_args[1]['previous_response_id'] == "search_response_id"
            
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()


class TestMultiStepWorkflowDemo:
    """MultiStepWorkflowDemoクラスのテスト（存在する場合）"""
    
    @pytest.fixture
    def demo_instance(self):
        """MultiStepWorkflowDemoのインスタンスを作成"""
        try:
            from a05_conversation_state import MultiStepWorkflowDemo
            demo = MultiStepWorkflowDemo("マルチステップワークフロー")
            demo.model = "gpt-4o-mini"
            demo.client = MagicMock()
            return demo
        except ImportError:
            pytest.skip("MultiStepWorkflowDemo not implemented")
    
    def test_demo_exists(self, demo_instance):
        """デモクラスが存在することを確認"""
        assert demo_instance is not None
        assert hasattr(demo_instance, 'run_demo')


class TestDemoManager:
    """DemoManagerクラスのテスト"""
    
    @patch('a05_conversation_state.StatefulConversationDemo')
    @patch('a05_conversation_state.WebSearchParseDemo')
    def test_demo_manager_initialization(self, mock_web_search, mock_stateful):
        """DemoManagerの初期化テスト"""
        try:
            from a05_conversation_state import DemoManager
        except ImportError:
            pytest.skip("DemoManager not implemented")
        
        manager = DemoManager()
        
        assert hasattr(manager, 'demos')
        assert len(manager.demos) >= 2
        assert any("ステートフル" in key or "Stateful" in key for key in manager.demos.keys())
    
    @patch('streamlit.sidebar.radio')
    @patch('a05_conversation_state.UIHelper')
    @patch('a05_conversation_state.setup_sidebar_panels')
    def test_run_method(self, mock_sidebar_panels, mock_ui_helper, mock_radio):
        """runメソッドのテスト"""
        try:
            from a05_conversation_state import DemoManager
        except ImportError:
            pytest.skip("DemoManager not implemented")
        
        mock_radio.return_value = "ステートフルな会話継続"
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        # モックデモ
        mock_demo = MagicMock()
        
        with patch('a05_conversation_state.StatefulConversationDemo', return_value=mock_demo), \
             patch('a05_conversation_state.WebSearchParseDemo'):
            
            manager = DemoManager()
            # DemoManagerはrunメソッドを持たない、run_demoメソッドを使用
            manager.run_demo("ステートフルな会話継続", "gpt-4o-mini")
            
            # デモが実行されることを確認
            mock_demo.execute.assert_called_once_with("gpt-4o-mini")


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    @patch('a05_conversation_state.config')
    def test_api_error_handling(self, mock_config, mock_error):
        """APIエラーハンドリングのテスト"""
        from a05_conversation_state import StatefulConversationDemo
        
        mock_config.get.return_value = False
        
        demo = StatefulConversationDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        demo.client.responses.create.side_effect = Exception("API Error")
        
        with patch('a05_conversation_state.get_default_messages', return_value=[]), \
             patch('streamlit.spinner'):
            
            demo._process_initial_question("Test question")
            
            mock_error.assert_called()
            assert "API Error" in mock_error.call_args[0][0]
    
    @patch('streamlit.error')
    @patch('streamlit.exception')
    @patch('a05_conversation_state.config')
    def test_debug_mode_exception(self, mock_config, mock_exception, mock_error):
        """デバッグモードでの例外表示テスト"""
        from a05_conversation_state import WebSearchParseDemo
        
        mock_config.get.return_value = True  # debug_mode = True
        
        demo = WebSearchParseDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        demo.client.responses.create.side_effect = Exception("Test Error")
        
        with patch('streamlit.spinner'):
            demo._execute_web_search("Test query")
            
            mock_error.assert_called()
            mock_exception.assert_called()  # デバッグモードで例外詳細が表示される


class TestConversationStateFeatures:
    """会話状態管理機能のテスト"""
    
    def test_previous_response_id_usage(self):
        """previous_response_idの使用確認"""
        from a05_conversation_state import StatefulConversationDemo
        
        demo = StatefulConversationDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        
        # 初回レスポンス
        initial_response = MagicMock()
        initial_response.id = "initial_id_123"
        
        with patch('streamlit.session_state', {
            f"initial_response_{demo.safe_key}": initial_response
        }), \
        patch('streamlit.spinner'), \
        patch('streamlit.success'), \
        patch('streamlit.rerun'):
            
            demo._process_follow_up_question("Follow up")
            
            # previous_response_idが正しく使用されているか確認
            call_args = demo.client.responses.create.call_args
            assert call_args[1]['previous_response_id'] == "initial_id_123"
    
    def test_web_search_tool_usage(self):
        """Web検索ツールの使用確認"""
        from a05_conversation_state import WebSearchParseDemo
        
        demo = WebSearchParseDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        
        with patch('streamlit.session_state', {}), \
             patch('streamlit.spinner'), \
             patch('streamlit.success'), \
             patch('streamlit.rerun'):
            
            demo._execute_web_search("Test search")
            
            # Web検索ツールが使用されているか確認
            call_args = demo.client.responses.create.call_args
            tools = call_args[1]['tools']
            assert len(tools) == 1
            assert tools[0]['type'] == 'web_search_preview'


class TestIntegration:
    """統合テスト"""
    
    @patch('streamlit.error')
    @patch('streamlit.sidebar.radio')
    @patch('a05_conversation_state.UIHelper')
    @patch('a05_conversation_state.setup_sidebar_panels')
    @patch('a05_conversation_state.SessionStateManager')
    @patch('a05_conversation_state.DemoManager')
    def test_main_function(self, mock_demo_manager, mock_session_state, mock_sidebar_panels,
                          mock_ui_helper, mock_radio, mock_error):
        """main関数のテスト"""
        try:
            from a05_conversation_state import main
        except ImportError:
            # main関数が定義されていない場合はスキップ
            pytest.skip("main function not defined")
        
        # モックの設定
        mock_manager_instance = MagicMock()
        mock_demo_manager.return_value = mock_manager_instance
        mock_manager_instance.get_demo_list.return_value = ["ステートフルな会話継続"]
        mock_radio.return_value = "ステートフルな会話継続"
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        # main関数の実行
        main()
        
        # 各コンポーネントが呼ばれたことを確認
        mock_session_state.init_session_state.assert_called_once()
        mock_demo_manager.assert_called_once()
        mock_manager_instance.get_demo_list.assert_called_once()
        mock_manager_instance.run_demo.assert_called_once_with("ステートフルな会話継続", "gpt-4o-mini")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])