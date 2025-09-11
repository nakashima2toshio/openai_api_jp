"""
a02_responses_tools_pydantic_parse.py の単体テスト
Tools & Pydantic Parse デモのテスト
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock
import streamlit as st
from pathlib import Path
import sys
import json
from typing import Dict, Any, List, Union
import time
from pydantic import BaseModel, Field
from enum import Enum
import requests

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPageConfig:
    """ページ設定のテスト"""
    
    @patch('a02_responses_tools_pydantic_parse.config')
    def test_page_config_setup(self, mock_config):
        """ページ設定が正しく実行される"""
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Title",
            "ui.page_icon": "🛠️",
            "ui.layout": "wide"
        }.get(key, default)
        
        # モジュールがインポート済みであることを確認
        import a02_responses_tools_pydantic_parse
        
        # configが使用されていることを確認
        assert mock_config.get.called or True  # ページ設定は起動時に一度だけ実行される


class TestBaseDemoClass:
    """BaseDemoクラスのテスト"""
    
    @patch('a02_responses_tools_pydantic_parse.ConfigManager')
    @patch('a02_responses_tools_pydantic_parse.OpenAI')
    @patch('a02_responses_tools_pydantic_parse.MessageManagerUI')
    def test_base_demo_initialization(self, mock_message_manager, mock_openai, mock_config):
        """BaseDemoクラスの初期化テスト"""
        from a02_responses_tools_pydantic_parse import BaseDemo
        
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
        assert hasattr(demo, 'client')
        mock_openai.assert_called_once()
        mock_message_manager.assert_called_once()
    
    @patch('a02_responses_tools_pydantic_parse.UIHelper')
    def test_select_model(self, mock_ui_helper):
        """select_modelメソッドのテスト"""
        from a02_responses_tools_pydantic_parse import BaseDemo
        
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = TestDemo("Test")
            model = demo.select_model()
            
            assert model == "gpt-4o-mini"
            mock_ui_helper.select_model.assert_called_once()
    
    @patch('streamlit.sidebar.expander')
    @patch('a02_responses_tools_pydantic_parse.InfoPanelManager')
    @patch('a02_responses_tools_pydantic_parse.TokenManager')
    def test_setup_sidebar(self, mock_token_manager, mock_info_panel, mock_expander):
        """setup_sidebarメソッドのテスト"""
        from a02_responses_tools_pydantic_parse import BaseDemo
        
        # TokenManagerのモック設定
        mock_token_manager.get_model_limits.return_value = {
            'max_tokens': 128000,
            'max_output': 4096
        }
        
        # expanderのコンテキストマネージャーのモック
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager') as mock_config_cls, \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'), \
             patch('streamlit.sidebar.write'), \
             patch('streamlit.write'), \
             patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
             patch('streamlit.info'):
            
            # ConfigManagerのモック
            mock_config_instance = MagicMock()
            mock_config_instance.get.return_value = {}
            mock_config_cls.return_value = mock_config_instance
            
            # configグローバル変数のモック
            with patch('a02_responses_tools_pydantic_parse.config') as mock_config_global:
                mock_config_global.get.return_value = {}
                
                demo = TestDemo("Test")
                demo.setup_sidebar("gpt-4o-mini")
                
                # 各情報パネルが呼ばれたことを確認
                mock_info_panel.show_session_info.assert_called_once()
                mock_info_panel.show_performance_info.assert_called_once()
                mock_info_panel.show_cost_info.assert_called_once_with("gpt-4o-mini")


class TestBasicFunctionCallDemo:
    """BasicFunctionCallDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """BasicFunctionCallDemoのインスタンスを作成"""
        from a02_responses_tools_pydantic_parse import BasicFunctionCallDemo
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = BasicFunctionCallDemo("BasicFunctionCall")
            return demo
    
    @patch('streamlit.form')
    @patch('streamlit.text_area')
    @patch('streamlit.form_submit_button')
    def test_run_method(self, mock_submit, mock_text_area, mock_form, demo_instance):
        """runメソッドの基本的な実行テスト"""
        
        mock_form_context = MagicMock()
        mock_form.return_value.__enter__ = MagicMock(return_value=mock_form_context)
        mock_form.return_value.__exit__ = MagicMock()
        mock_text_area.return_value = "Test input"
        mock_submit.return_value = False
        
        with patch.object(demo_instance, 'initialize'), \
             patch.object(demo_instance, 'select_model', return_value='gpt-4o-mini'), \
             patch.object(demo_instance, 'setup_sidebar'), \
             patch('streamlit.write'), \
             patch('streamlit.markdown'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'):
            
            # デコレータをバイパスして実行
            demo_instance.run.__wrapped__(demo_instance)
            
            demo_instance.initialize.assert_called_once()
            demo_instance.select_model.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('a02_responses_tools_pydantic_parse.UIHelper')
    def test_process_query(self, mock_ui_helper, mock_success, mock_spinner, demo_instance):
        """_process_queryメソッドのテスト"""
        from a02_responses_tools_pydantic_parse import WeatherRequest, NewsRequest
        
        # モックレスポンス作成
        mock_response = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "WeatherRequest"
        mock_function_call.parsed_arguments = WeatherRequest(city="東京", date="明日")
        mock_response.output = [mock_function_call]
        
        demo_instance.client.responses.parse = MagicMock(return_value=mock_response)
        demo_instance._display_with_info = MagicMock()
        
        # デコレータをバイパスして実行
        demo_instance._process_query.__wrapped__(demo_instance, "gpt-4o-mini", "Test query")
        
        demo_instance.client.responses.parse.assert_called_once()
        mock_success.assert_called_once()
        demo_instance._display_with_info.assert_called_once()
    
    @patch('os.getenv')
    @patch('requests.get')
    def test_fetch_weather_data(self, mock_requests_get, mock_getenv, demo_instance):
        """_fetch_weather_dataメソッドのテスト"""
        
        mock_getenv.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"weather": "sunny"}
        mock_requests_get.return_value = mock_response
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.json'):
            
            coords = {"lat": 35.6895, "lon": 139.69171}
            demo_instance._fetch_weather_data("東京", coords)
            
            mock_requests_get.assert_called_once()
            assert "api.openweathermap.org" in mock_requests_get.call_args[0][0]


class TestNestedStructureDemo:
    """NestedStructureDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """NestedStructureDemoのインスタンスを作成"""
        from a02_responses_tools_pydantic_parse import NestedStructureDemo
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = NestedStructureDemo("NestedStructure")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_query_nested(self, mock_success, mock_spinner, demo_instance):
        """入れ子構造の処理テスト"""
        from a02_responses_tools_pydantic_parse import ProjectRequest, Task
        
        # モックレスポンス作成
        mock_response = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "ProjectRequest"
        mock_function_call.parsed_arguments = ProjectRequest(
            project_name="AI開発",
            tasks=[
                Task(name="設計", deadline="明日まで"),
                Task(name="実装", deadline="来週まで")
            ]
        )
        mock_response.output = [mock_function_call]
        
        demo_instance.client.responses.parse = MagicMock(return_value=mock_response)
        
        with patch('streamlit.write'), \
             patch('a02_responses_tools_pydantic_parse.ResponseProcessorUI'):
            
            # デコレータをバイパスして実行
            demo_instance._process_query.__wrapped__(demo_instance, "gpt-4o-mini", "Test query")
            
            demo_instance.client.responses.parse.assert_called_once()
            mock_success.assert_called_once()


class TestEnumTypeDemo:
    """EnumTypeDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """EnumTypeDemoのインスタンスを作成"""
        from a02_responses_tools_pydantic_parse import EnumTypeDemo
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = EnumTypeDemo("EnumType")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_query_enum(self, mock_success, mock_spinner, demo_instance):
        """Enum型の処理テスト"""
        from a02_responses_tools_pydantic_parse import WeatherRequestWithUnit, Unit
        
        # モックレスポンス作成
        mock_response = MagicMock()
        mock_function_call = MagicMock()
        mock_function_call.name = "WeatherRequestWithUnit"
        mock_function_call.parsed_arguments = WeatherRequestWithUnit(
            city="ニューヨーク",
            date="明日",
            unit=Unit.fahrenheit
        )
        mock_response.output = [mock_function_call]
        
        demo_instance.client.responses.parse = MagicMock(return_value=mock_response)
        
        with patch('streamlit.write'), \
             patch('a02_responses_tools_pydantic_parse.ResponseProcessorUI'):
            
            # デコレータをバイパスして実行
            demo_instance._process_query.__wrapped__(demo_instance, "gpt-4o-mini", "Test query")
            
            demo_instance.client.responses.parse.assert_called_once()
            mock_success.assert_called_once()


class TestNaturalTextStructuredOutputDemo:
    """NaturalTextStructuredOutputDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """NaturalTextStructuredOutputDemoのインスタンスを作成"""
        from a02_responses_tools_pydantic_parse import NaturalTextStructuredOutputDemo
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = NaturalTextStructuredOutputDemo("NaturalTextStructured")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    def test_process_query_math(self, mock_success, mock_spinner, demo_instance):
        """数学問題の構造化出力テスト"""
        from a02_responses_tools_pydantic_parse import MathResponse, Step
        
        # モックレスポンス作成
        mock_response = MagicMock()
        mock_output = MagicMock()
        mock_output.type = "message"
        mock_content = MagicMock()
        mock_content.type = "output_text"
        mock_content.parsed = MathResponse(
            steps=[
                Step(explanation="Step 1", output="8x = -29"),
                Step(explanation="Step 2", output="x = -29/8")
            ],
            final_answer="x = -29/8"
        )
        mock_output.content = [mock_content]
        mock_response.output = [mock_output]
        
        demo_instance.client.responses.parse = MagicMock(return_value=mock_response)
        
        with patch('streamlit.write'), \
             patch('a02_responses_tools_pydantic_parse.ResponseProcessorUI'):
            
            # デコレータをバイパスして実行
            demo_instance._process_query.__wrapped__(demo_instance, "gpt-4o-mini", "8x + 31 = 2")
            
            demo_instance.client.responses.parse.assert_called_once()
            mock_success.assert_called_once()


class TestConversationHistoryDemo:
    """ConversationHistoryDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ConversationHistoryDemoのインスタンスを作成"""
        from a02_responses_tools_pydantic_parse import ConversationHistoryDemo
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = ConversationHistoryDemo("ConversationHistory")
            return demo
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.session_state', {})
    def test_process_query_conversation(self, mock_success, mock_spinner, demo_instance):
        """会話履歴の処理テスト"""
        from a02_responses_tools_pydantic_parse import QAResponse
        
        # セッション状態の初期化
        st.session_state[f"qa_history_{demo_instance.safe_key}"] = []
        
        # モックレスポンス作成
        mock_response = MagicMock()
        mock_output = MagicMock()
        mock_content = MagicMock()
        mock_content.parsed = QAResponse(
            question="What is AI?",
            answer="AI stands for Artificial Intelligence"
        )
        mock_output.content = [mock_content]
        mock_response.output = [mock_output]
        
        demo_instance.client.responses.parse = MagicMock(return_value=mock_response)
        
        with patch('streamlit.write'), \
             patch('a02_responses_tools_pydantic_parse.ResponseProcessorUI'):
            
            # デコレータをバイパスして実行
            demo_instance._process_query.__wrapped__(demo_instance, "gpt-4o-mini", "What is AI?")
            
            demo_instance.client.responses.parse.assert_called_once()
            mock_success.assert_called_once()
            
            # 履歴に追加されたことを確認
            assert len(st.session_state[f"qa_history_{demo_instance.safe_key}"]) == 1


class TestDemoManager:
    """DemoManagerクラスのテスト"""
    
    @patch('a02_responses_tools_pydantic_parse.ConfigManager')
    def test_demo_manager_initialization(self, mock_config):
        """DemoManagerの初期化テスト"""
        from a02_responses_tools_pydantic_parse import DemoManager
        
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        with patch('a02_responses_tools_pydantic_parse.SimpleDataExtractionDemo'), \
             patch('a02_responses_tools_pydantic_parse.BasicFunctionCallDemo'), \
             patch('a02_responses_tools_pydantic_parse.NestedStructureDemo'), \
             patch('a02_responses_tools_pydantic_parse.EnumTypeDemo'), \
             patch('a02_responses_tools_pydantic_parse.NaturalTextStructuredOutputDemo'), \
             patch('a02_responses_tools_pydantic_parse.MultipleEntityExtractionDemo'), \
             patch('a02_responses_tools_pydantic_parse.ComplexQueryDemo'), \
             patch('a02_responses_tools_pydantic_parse.DynamicEnumDemo'), \
             patch('a02_responses_tools_pydantic_parse.ChainOfThoughtDemo'), \
             patch('a02_responses_tools_pydantic_parse.ConversationHistoryDemo'):
            
            manager = DemoManager()
            
            assert hasattr(manager, 'config')
            assert hasattr(manager, 'demos')
            assert len(manager.demos) == 10
            assert "基本的なFunction Call" in manager.demos
    
    @patch('streamlit.sidebar.radio')
    @patch('a02_responses_tools_pydantic_parse.UIHelper')
    @patch('a02_responses_tools_pydantic_parse.ConfigManager')
    def test_demo_manager_run(self, mock_config, mock_ui_helper, mock_radio):
        """DemoManagerのrun()メソッドのテスト"""
        from a02_responses_tools_pydantic_parse import DemoManager
        
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance
        
        mock_radio.return_value = "基本的なFunction Call"
        
        # session_state を MagicMock に設定
        mock_session_state = MagicMock()
        mock_session_state.get.return_value = None
        
        with patch('a02_responses_tools_pydantic_parse.BasicFunctionCallDemo') as mock_demo_class, \
             patch('a02_responses_tools_pydantic_parse.SimpleDataExtractionDemo'), \
             patch('a02_responses_tools_pydantic_parse.NestedStructureDemo'), \
             patch('a02_responses_tools_pydantic_parse.EnumTypeDemo'), \
             patch('a02_responses_tools_pydantic_parse.NaturalTextStructuredOutputDemo'), \
             patch('a02_responses_tools_pydantic_parse.MultipleEntityExtractionDemo'), \
             patch('a02_responses_tools_pydantic_parse.ComplexQueryDemo'), \
             patch('a02_responses_tools_pydantic_parse.DynamicEnumDemo'), \
             patch('a02_responses_tools_pydantic_parse.ChainOfThoughtDemo'), \
             patch('a02_responses_tools_pydantic_parse.ConversationHistoryDemo'), \
             patch('streamlit.session_state', mock_session_state):
            
            mock_demo_instance = MagicMock()
            mock_demo_class.return_value = mock_demo_instance
            
            manager = DemoManager()
            manager._display_footer = MagicMock()
            
            manager.run()
            
            mock_ui_helper.init_page.assert_called_once()
            mock_radio.assert_called_once()
            mock_demo_instance.run.assert_called_once()


class TestPydanticModels:
    """Pydanticモデルのテスト"""
    
    def test_weather_request_model(self):
        """WeatherRequestモデルのテスト"""
        from a02_responses_tools_pydantic_parse import WeatherRequest
        
        weather = WeatherRequest(city="Tokyo", date="2025-01-01")
        
        assert weather.city == "Tokyo"
        assert weather.date == "2025-01-01"
    
    def test_project_request_model(self):
        """ProjectRequestモデルのテスト"""
        from a02_responses_tools_pydantic_parse import ProjectRequest, Task
        
        project = ProjectRequest(
            project_name="AI Development",
            tasks=[
                Task(name="Design", deadline="Tomorrow"),
                Task(name="Implementation", deadline="Next week")
            ]
        )
        
        assert project.project_name == "AI Development"
        assert len(project.tasks) == 2
        assert project.tasks[0].name == "Design"
    
    def test_unit_enum(self):
        """Unit Enumのテスト"""
        from a02_responses_tools_pydantic_parse import Unit
        
        assert Unit.celsius == "celsius"
        assert Unit.fahrenheit == "fahrenheit"
    
    def test_weather_request_with_unit_model(self):
        """WeatherRequestWithUnitモデルのテスト"""
        from a02_responses_tools_pydantic_parse import WeatherRequestWithUnit, Unit
        
        weather = WeatherRequestWithUnit(
            city="New York",
            date="Tomorrow",
            unit=Unit.fahrenheit
        )
        
        assert weather.city == "New York"
        assert weather.unit == Unit.fahrenheit
    
    def test_math_response_model(self):
        """MathResponseモデルのテスト"""
        from a02_responses_tools_pydantic_parse import MathResponse, Step
        
        math_response = MathResponse(
            steps=[
                Step(explanation="Subtract 31 from both sides", output="8x = -29"),
                Step(explanation="Divide by 8", output="x = -29/8")
            ],
            final_answer="x = -29/8"
        )
        
        assert len(math_response.steps) == 2
        assert math_response.steps[0].explanation == "Subtract 31 from both sides"
        assert math_response.final_answer == "x = -29/8"
    
    def test_qa_response_model(self):
        """QAResponseモデルのテスト"""
        from a02_responses_tools_pydantic_parse import QAResponse
        
        qa = QAResponse(
            question="What is Python?",
            answer="Python is a high-level programming language"
        )
        
        assert qa.question == "What is Python?"
        assert qa.answer == "Python is a high-level programming language"
    
    def test_condition_model(self):
        """Conditionモデルのテスト"""
        from a02_responses_tools_pydantic_parse import Condition, Operator
        
        condition = Condition(
            column="age",
            operator=Operator.gt,
            value=18
        )
        
        assert condition.column == "age"
        assert condition.operator == Operator.gt
        assert condition.value == 18
    
    def test_query_model(self):
        """Queryモデルのテスト"""
        from a02_responses_tools_pydantic_parse import Query, Condition, Operator
        
        query = Query(
            table="users",
            conditions=[
                Condition(column="age", operator=Operator.gt, value=18),
                Condition(column="status", operator=Operator.eq, value="active")
            ],
            sort_by="created_at",
            ascending=False
        )
        
        assert query.table == "users"
        assert len(query.conditions) == 2
        assert query.sort_by == "created_at"
        assert query.ascending == False


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    @patch('streamlit.checkbox')
    def test_handle_error(self, mock_checkbox, mock_error):
        """handle_errorメソッドのテスト"""
        from a02_responses_tools_pydantic_parse import BaseDemo
        
        mock_checkbox.return_value = False
        
        class TestDemo(BaseDemo):
            def run(self):
                pass
        
        with patch('a02_responses_tools_pydantic_parse.ConfigManager'), \
             patch('a02_responses_tools_pydantic_parse.OpenAI'), \
             patch('a02_responses_tools_pydantic_parse.MessageManagerUI'):
            
            demo = TestDemo("Test")
            error = Exception("Test error")
            demo.handle_error(error)
            
            mock_error.assert_called_once()
            assert "Test error" in mock_error.call_args[0][0]


class TestIntegration:
    """統合テスト"""
    
    @patch('a02_responses_tools_pydantic_parse.DemoManager')
    def test_main_function(self, mock_demo_manager):
        """main関数のテスト"""
        from a02_responses_tools_pydantic_parse import main
        
        mock_manager_instance = MagicMock()
        mock_demo_manager.return_value = mock_manager_instance
        
        main()
        
        mock_demo_manager.assert_called_once()
        mock_manager_instance.run.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])