"""
a01_structured_outputs_parse_schema.py の単体テスト
responses.parse API を使用した構造化出力デモのテスト
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
import streamlit as st
from pathlib import Path
import sys
import json
from typing import Dict, Any, List, Union
import time
from pydantic import BaseModel, Field, ValidationError

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPageConfig:
    """ページ設定のテスト"""
    
    @patch('streamlit.set_page_config')
    @patch('a01_structured_outputs_parse_schema.config')
    def test_setup_page_config_success(self, mock_config, mock_set_page_config):
        """ページ設定が正常に実行される"""
        from a01_structured_outputs_parse_schema import setup_page_config
        
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Title",
            "ui.page_icon": "🗂️",
            "ui.layout": "wide"
        }.get(key, default)
        
        setup_page_config()
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Title",
            page_icon="🗂️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config_already_set(self, mock_set_page_config):
        """既に設定済みの場合はエラーを無視"""
        from a01_structured_outputs_parse_schema import setup_page_config
        
        mock_set_page_config.side_effect = st.errors.StreamlitAPIException("Already set")
        
        # エラーが発生してもクラッシュしない
        setup_page_config()


class TestCommonUI:
    """共通UI関数のテスト"""
    
    @patch('a01_structured_outputs_parse_schema.UIHelper')
    @patch('a01_structured_outputs_parse_schema.sanitize_key')
    @patch('streamlit.write')
    def test_setup_common_ui(self, mock_write, mock_sanitize_key, mock_ui_helper):
        """共通UI設定が正しく動作する"""
        from a01_structured_outputs_parse_schema import setup_common_ui
        
        mock_sanitize_key.return_value = "test_demo"
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        model = setup_common_ui("Test Demo")
        
        assert model == "gpt-4o-mini"
        mock_sanitize_key.assert_called_once_with("Test Demo")
        mock_ui_helper.select_model.assert_called_once_with("model_test_demo")


class TestBaseDemoClass:
    """BaseDemoクラスのテスト"""
    
    @patch('a01_structured_outputs_parse_schema.ConfigManager')
    @patch('a01_structured_outputs_parse_schema.OpenAIClient')
    @patch('a01_structured_outputs_parse_schema.MessageManagerUI')
    @patch('a01_structured_outputs_parse_schema.SessionStateManager')
    def test_base_demo_initialization(self, mock_session, mock_message_manager,
                                     mock_openai_client, mock_config):
        """BaseDemoクラスの初期化テスト"""
        from a01_structured_outputs_parse_schema import BaseDemo
        
        # ConfigManagerのモック設定
        mock_config_instance = MagicMock()
        mock_config_instance.get.return_value = "test_value"
        mock_config.return_value = mock_config_instance
        
        # 具象クラスを作成してテスト
        class ConcreteDemo(BaseDemo):
            def run(self):
                pass
        
        demo = ConcreteDemo("Test Demo")
        
        assert demo.demo_name == "Test Demo"
        assert hasattr(demo, 'config')
        mock_openai_client.assert_called_once()
        mock_message_manager.assert_called_once()
        mock_session.init_session_state.assert_called_once()
    
    @patch('a01_structured_outputs_parse_schema.OpenAI')
    @patch('os.getenv')
    def test_call_api_parse(self, mock_getenv, mock_openai):
        """call_api_parse メソッドのテスト"""
        from a01_structured_outputs_parse_schema import BaseDemo, EventInfo
        
        # 環境変数のモック
        mock_getenv.return_value = "test_api_key"
        
        # OpenAIクライアントのモック
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.output_parsed = EventInfo(
            name="Test Event",
            date="2025-01-01",
            participants=["Alice", "Bob"]
        )
        mock_client.responses.parse.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # BaseDemoのサブクラス作成
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {}):
            
            demo = TestDemo("Test")
            demo.model = "gpt-4o-mini"
            
            # call_api_parseを直接呼び出し（デコレータなし）
            result = demo.call_api_parse.__wrapped__.__wrapped__(
                demo,
                input_text="Test input",
                text_format=EventInfo,
                temperature=0.5
            )
            
            assert result.output_parsed.name == "Test Event"
            mock_client.responses.parse.assert_called_once()
    
    def test_is_reasoning_model(self):
        """is_reasoning_model メソッドのテスト"""
        from a01_structured_outputs_parse_schema import BaseDemo
        
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {}):
            
            demo = TestDemo("Test")
            
            # 推論系モデルのチェック
            assert demo.is_reasoning_model("o1-preview") == True
            assert demo.is_reasoning_model("o3-mini") == True
            assert demo.is_reasoning_model("gpt-5") == True
            assert demo.is_reasoning_model("gpt-4o-mini") == False
            assert demo.is_reasoning_model("gpt-4-turbo") == False


class TestEventExtractionDemo:
    """EventExtractionDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """EventExtractionDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import EventExtractionDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_event_extraction': 'gpt-4o-mini'}):
            
            demo = EventExtractionDemo("イベント情報抽出")
            return demo
    
    @patch('streamlit.expander')
    @patch('streamlit.write')
    @patch('streamlit.form')
    @patch('a01_structured_outputs_parse_schema.setup_common_ui')
    @patch('a01_structured_outputs_parse_schema.setup_sidebar_panels')
    def test_event_extraction_run(self, mock_sidebar, mock_common_ui, 
                                 mock_form, mock_write, mock_expander, demo_instance):
        """EventExtractionDemoのrun()メソッドのテスト"""
        
        mock_common_ui.return_value = "gpt-4o-mini"
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.text_area'), \
             patch('streamlit.form_submit_button', return_value=False):
            
            # run メソッドを直接呼び出し（デコレータなし）
            demo_instance.run.__wrapped__.__wrapped__(demo_instance)
            
            mock_common_ui.assert_called_once_with("イベント情報抽出")
            mock_sidebar.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('a01_structured_outputs_parse_schema.UIHelper')
    def test_process_extraction(self, mock_ui_helper, mock_success, mock_spinner, demo_instance):
        """_process_extractionメソッドのテスト"""
        from a01_structured_outputs_parse_schema import EventInfo
        
        # API応答のモック
        mock_response = MagicMock()
        mock_response.output_parsed = EventInfo(
            name="台湾フェス2025",
            date="5/3・5/4",
            participants=["王さん", "林さん", "佐藤さん"]
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_event_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_event_extraction': {'execution_count': 0}}):
            demo_instance._process_extraction("Test input", 0.1)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_event_result.assert_called_once_with(
                mock_response.output_parsed, mock_response
            )
            mock_success.assert_called_once()


class TestMathReasoningDemo:
    """MathReasoningDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """MathReasoningDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import MathReasoningDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_math_reasoning': 'gpt-4o-mini'}):
            
            demo = MathReasoningDemo("数学的思考ステップ")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_math_reasoning(self, mock_success, mock_spinner, demo_instance):
        """_process_math_reasoningメソッドのテスト"""
        from a01_structured_outputs_parse_schema import MathReasoning, Step
        
        # API応答のモック
        mock_response = MagicMock()
        mock_response.output_parsed = MathReasoning(
            steps=[
                Step(explanation="Step 1", output="8x = -30"),
                Step(explanation="Step 2", output="x = -3.75")
            ],
            final_answer="x = -3.75"
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_math_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_math_reasoning': {'execution_count': 0}}):
            demo_instance._process_math_reasoning("8x + 7 = -23", 0.2)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_math_result.assert_called_once()
            mock_success.assert_called_once()


class TestUIGenerationDemo:
    """UIGenerationDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """UIGenerationDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import UIGenerationDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_ui_generation': 'gpt-4o-mini'}):
            
            demo = UIGenerationDemo("UIコンポーネント生成")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_ui_generation(self, mock_success, mock_spinner, demo_instance):
        """_process_ui_generationメソッドのテスト"""
        from a01_structured_outputs_parse_schema import UIComponent, UIAttribute
        
        # API応答のモック
        mock_response = MagicMock()
        mock_response.output_parsed = UIComponent(
            type="form",
            label="ログインフォーム",
            children=[],
            attributes=[UIAttribute(name="method", value="POST")]
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_ui_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_ui_generation': {'execution_count': 0}}):
            demo_instance._process_ui_generation("ログインフォーム", 0.3)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_ui_result.assert_called_once()
            mock_success.assert_called_once()


class TestEntityExtractionDemo:
    """EntityExtractionDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """EntityExtractionDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import EntityExtractionDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_entity_extraction': 'gpt-4o-mini'}):
            
            demo = EntityExtractionDemo("エンティティ抽出")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_entity_extraction(self, mock_success, mock_spinner, demo_instance):
        """_process_entity_extractionメソッドのテスト"""
        from a01_structured_outputs_parse_schema import Entities
        
        # API応答のモック
        mock_response = MagicMock()
        mock_response.output_parsed = Entities(
            attributes=["quick", "lazy"],
            colors=["brown", "blue"],
            animals=["fox", "dog"]
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_entity_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_entity_extraction': {'execution_count': 0}}):
            demo_instance._process_entity_extraction("The quick brown fox", 0.1)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_entity_result.assert_called_once()
            mock_success.assert_called_once()


class TestConditionalSchemaDemo:
    """ConditionalSchemaDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ConditionalSchemaDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import ConditionalSchemaDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_conditional_schema': 'gpt-4o-mini'}):
            
            demo = ConditionalSchemaDemo("条件分岐スキーマ")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_conditional_schema_user_info(self, mock_success, mock_spinner, demo_instance):
        """_process_conditional_schemaメソッドのテスト（UserInfo）"""
        from a01_structured_outputs_parse_schema import ConditionalItem, UserInfo
        
        # API応答のモック（UserInfo）
        mock_response = MagicMock()
        mock_response.output_parsed = ConditionalItem(
            item=UserInfo(name="Alice", age=30)
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_conditional_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_conditional_schema': {'execution_count': 0}}):
            demo_instance._process_conditional_schema("Name: Alice, Age: 30", 0.1)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_conditional_result.assert_called_once()
            mock_success.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_conditional_schema_address(self, mock_success, mock_spinner, demo_instance):
        """_process_conditional_schemaメソッドのテスト（Address）"""
        from a01_structured_outputs_parse_schema import ConditionalItem, Address
        
        # API応答のモック（Address）
        mock_response = MagicMock()
        mock_response.output_parsed = ConditionalItem(
            item=Address(number="123", street="Main St", city="Tokyo")
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_conditional_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_conditional_schema': {'execution_count': 0}}):
            demo_instance._process_conditional_schema("123 Main St, Tokyo", 0.1)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_conditional_result.assert_called_once()
            mock_success.assert_called_once()


class TestModerationDemo:
    """ModerationDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ModerationDemoのインスタンスを作成"""
        from a01_structured_outputs_parse_schema import ModerationDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'model_moderation': 'gpt-4o-mini'}):
            
            demo = ModerationDemo("モデレーション＆拒否処理")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_moderation_allowed(self, mock_success, mock_spinner, demo_instance):
        """_process_moderationメソッドのテスト（許可）"""
        from a01_structured_outputs_parse_schema import ModerationResult
        
        # API応答のモック（許可）
        mock_response = MagicMock()
        mock_response.output_parsed = ModerationResult(
            refusal="",
            content="Hello, how can I help you today?"
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_moderation_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_moderation': {'execution_count': 0}}):
            demo_instance._process_moderation("Hello", 0.0)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_moderation_result.assert_called_once()
            mock_success.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_moderation_refused(self, mock_success, mock_spinner, demo_instance):
        """_process_moderationメソッドのテスト（拒否）"""
        from a01_structured_outputs_parse_schema import ModerationResult
        
        # API応答のモック（拒否）
        mock_response = MagicMock()
        mock_response.output_parsed = ModerationResult(
            refusal="Inappropriate content detected",
            content=None
        )
        
        demo_instance.call_api_parse = MagicMock(return_value=mock_response)
        demo_instance._display_moderation_result = MagicMock()
        
        with patch('streamlit.session_state', {'demo_state_moderation': {'execution_count': 0}}):
            demo_instance._process_moderation("Bad content", 0.0)
            
            demo_instance.call_api_parse.assert_called_once()
            demo_instance._display_moderation_result.assert_called_once()
            mock_success.assert_called_once()


class TestDemoManager:
    """DemoManagerクラスのテスト"""
    
    @patch('a01_structured_outputs_parse_schema.ConfigManager')
    def test_demo_manager_initialization(self, mock_config):
        """DemoManagerの初期化テスト"""
        from a01_structured_outputs_parse_schema import DemoManager
        
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        with patch('a01_structured_outputs_parse_schema.EventExtractionDemo'), \
             patch('a01_structured_outputs_parse_schema.MathReasoningDemo'), \
             patch('a01_structured_outputs_parse_schema.UIGenerationDemo'), \
             patch('a01_structured_outputs_parse_schema.EntityExtractionDemo'), \
             patch('a01_structured_outputs_parse_schema.ConditionalSchemaDemo'), \
             patch('a01_structured_outputs_parse_schema.ModerationDemo'):
            
            manager = DemoManager()
            
            assert hasattr(manager, 'config')
            assert hasattr(manager, 'demos')
            assert len(manager.demos) == 6
            assert "イベント情報抽出" in manager.demos
            assert "数学的思考ステップ" in manager.demos
    
    @patch('streamlit.sidebar.radio')
    @patch('a01_structured_outputs_parse_schema.SessionStateManager')
    @patch('a01_structured_outputs_parse_schema.ConfigManager')
    def test_demo_manager_run(self, mock_config, mock_session, mock_radio):
        """DemoManagerのrun()メソッドのテスト"""
        from a01_structured_outputs_parse_schema import DemoManager
        
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        mock_radio.return_value = "イベント情報抽出"
        
        # session_state を MagicMock に変更して属性アクセスを許可
        mock_session_state = MagicMock()
        mock_session_state.get.return_value = None  # current_demo の初期値
        
        with patch('a01_structured_outputs_parse_schema.EventExtractionDemo') as mock_event_demo, \
             patch('a01_structured_outputs_parse_schema.MathReasoningDemo'), \
             patch('a01_structured_outputs_parse_schema.UIGenerationDemo'), \
             patch('a01_structured_outputs_parse_schema.EntityExtractionDemo'), \
             patch('a01_structured_outputs_parse_schema.ConditionalSchemaDemo'), \
             patch('a01_structured_outputs_parse_schema.ModerationDemo'), \
             patch('streamlit.session_state', mock_session_state):
            
            mock_demo_instance = MagicMock()
            mock_event_demo.return_value = mock_demo_instance
            
            manager = DemoManager()
            manager._display_footer = MagicMock()
            
            # run メソッドを直接呼び出し（デコレータなし）
            manager.run.__wrapped__.__wrapped__(manager)
            
            mock_session.init_session_state.assert_called_once()
            mock_radio.assert_called_once()
            mock_demo_instance.run.assert_called_once()


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    @patch('a01_structured_outputs_parse_schema.config')
    def test_handle_error(self, mock_config, mock_error):
        """handle_errorメソッドのテスト"""
        from a01_structured_outputs_parse_schema import BaseDemo
        
        mock_config.get.side_effect = lambda key, default: {
            "i18n.default_language": "ja",
            "error_messages.ja.general_error": "エラーが発生しました",
            "experimental.debug_mode": False
        }.get(key, default)
        
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {}):
            
            demo = TestDemo("Test")
            error = Exception("Test error")
            demo.handle_error(error)
            
            mock_error.assert_called_once_with("エラーが発生しました: Test error")
    
    @patch('streamlit.error')
    @patch('streamlit.spinner')
    def test_api_error_handling(self, mock_spinner, mock_error):
        """API呼び出しエラー時の処理テスト"""
        from a01_structured_outputs_parse_schema import EventExtractionDemo
        
        with patch('a01_structured_outputs_parse_schema.ConfigManager'), \
             patch('a01_structured_outputs_parse_schema.OpenAIClient'), \
             patch('a01_structured_outputs_parse_schema.MessageManagerUI'), \
             patch('a01_structured_outputs_parse_schema.SessionStateManager'), \
             patch('streamlit.session_state', {'demo_state_event_extraction': {'execution_count': 0}}):
            
            demo = EventExtractionDemo("イベント情報抽出")
            demo.call_api_parse = MagicMock(side_effect=Exception("API Error"))
            demo.handle_error = MagicMock()
            
            demo._process_extraction("Test input", 0.1)
            
            demo.handle_error.assert_called_once()


class TestIntegration:
    """統合テスト"""
    
    @patch('os.getenv')
    @patch('streamlit.error')
    @patch('streamlit.info')
    @patch('streamlit.stop')
    def test_main_without_api_key(self, mock_stop, mock_info, mock_error, mock_getenv):
        """APIキーがない場合のmain関数のテスト"""
        from a01_structured_outputs_parse_schema import main
        
        mock_getenv.return_value = None
        
        main()
        
        mock_error.assert_called_once_with("環境変数 OPENAI_API_KEY が設定されていません。")
        # info が複数回呼ばれる可能性があるため、呼び出し回数を柔軟にチェック
        assert mock_info.call_count >= 1
        mock_stop.assert_called_once()
    
    @patch('os.getenv')
    @patch('a01_structured_outputs_parse_schema.DemoManager')
    @patch('a01_structured_outputs_parse_schema.SessionStateManager')
    def test_main_with_api_key(self, mock_session, mock_demo_manager, mock_getenv):
        """APIキーがある場合のmain関数のテスト"""
        from a01_structured_outputs_parse_schema import main
        
        mock_getenv.return_value = "test_api_key"
        mock_manager_instance = MagicMock()
        mock_demo_manager.return_value = mock_manager_instance
        
        main()
        
        mock_session.init_session_state.assert_called_once()
        mock_demo_manager.assert_called_once()
        mock_manager_instance.run.assert_called_once()


class TestPydanticModels:
    """Pydanticモデルのテスト"""
    
    def test_event_info_model(self):
        """EventInfoモデルのテスト"""
        from a01_structured_outputs_parse_schema import EventInfo
        
        event = EventInfo(
            name="Test Event",
            date="2025-01-01",
            participants=["Alice", "Bob", "Charlie"]
        )
        
        assert event.name == "Test Event"
        assert event.date == "2025-01-01"
        assert len(event.participants) == 3
        assert "Alice" in event.participants
    
    def test_math_reasoning_model(self):
        """MathReasoningモデルのテスト"""
        from a01_structured_outputs_parse_schema import MathReasoning, Step
        
        math_result = MathReasoning(
            steps=[
                Step(explanation="Step 1", output="x + 5 = 10"),
                Step(explanation="Step 2", output="x = 5")
            ],
            final_answer="x = 5"
        )
        
        assert len(math_result.steps) == 2
        assert math_result.steps[0].explanation == "Step 1"
        assert math_result.final_answer == "x = 5"
    
    def test_ui_component_model(self):
        """UIComponentモデルのテスト"""
        from a01_structured_outputs_parse_schema import UIComponent, UIAttribute
        
        ui = UIComponent(
            type="button",
            label="Submit",
            children=[],
            attributes=[UIAttribute(name="type", value="submit")]
        )
        
        assert ui.type == "button"
        assert ui.label == "Submit"
        assert len(ui.attributes) == 1
        assert ui.attributes[0].name == "type"
    
    def test_entities_model(self):
        """Entitiesモデルのテスト"""
        from a01_structured_outputs_parse_schema import Entities
        
        entities = Entities(
            attributes=["quick", "lazy"],
            colors=["brown", "blue"],
            animals=["fox", "dog"]
        )
        
        assert len(entities.attributes) == 2
        assert "brown" in entities.colors
        assert "fox" in entities.animals
    
    def test_conditional_item_model(self):
        """ConditionalItemモデルのテスト"""
        from a01_structured_outputs_parse_schema import ConditionalItem, UserInfo, Address
        
        # UserInfo の場合
        user_item = ConditionalItem(
            item=UserInfo(name="Alice", age=30)
        )
        assert isinstance(user_item.item, UserInfo)
        assert user_item.item.name == "Alice"
        
        # Address の場合
        address_item = ConditionalItem(
            item=Address(number="123", street="Main St", city="Tokyo")
        )
        assert isinstance(address_item.item, Address)
        assert address_item.item.city == "Tokyo"
    
    def test_moderation_result_model(self):
        """ModerationResultモデルのテスト"""
        from a01_structured_outputs_parse_schema import ModerationResult
        
        # 許可の場合
        allowed = ModerationResult(
            refusal="",
            content="Safe content"
        )
        assert allowed.refusal == ""
        assert allowed.content == "Safe content"
        
        # 拒否の場合
        refused = ModerationResult(
            refusal="Inappropriate content",
            content=None
        )
        assert refused.refusal == "Inappropriate content"
        assert refused.content is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])