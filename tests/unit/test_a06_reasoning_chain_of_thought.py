"""
a06_reasoning_chain_of_thought.py の単体テスト
Chain of Thought 推論パターンデモのテスト
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
    @patch('a06_reasoning_chain_of_thought.config')
    def test_setup_page_config_success(self, mock_config, mock_set_page_config):
        """ページ設定が正常に実行される"""
        from a06_reasoning_chain_of_thought import setup_page_config
        
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Reasoning Title",
            "ui.page_icon": "🧠",
            "ui.layout": "wide"
        }.get(key, default)
        
        setup_page_config()
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Reasoning Title",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config_already_set(self, mock_set_page_config):
        """既に設定済みの場合はエラーを無視"""
        from a06_reasoning_chain_of_thought import setup_page_config
        
        mock_set_page_config.side_effect = st.errors.StreamlitAPIException("Already set")
        
        # エラーが発生してもクラッシュしない
        setup_page_config()


class TestCommonUI:
    """共通UI関数のテスト"""
    
    @patch('streamlit.write')
    def test_setup_common_ui(self, mock_write):
        """共通UI設定が正しく動作する"""
        from a06_reasoning_chain_of_thought import setup_common_ui
        
        setup_common_ui("Test Demo", "gpt-4o-mini")
        
        # ヘッダーとモデル表示が呼ばれたことを確認
        assert mock_write.call_count >= 2
    
    @patch('a06_reasoning_chain_of_thought.InfoPanelManager')
    @patch('streamlit.sidebar.write')
    def test_setup_sidebar_panels(self, mock_write, mock_info_panel):
        """サイドバーパネル設定のテスト"""
        from a06_reasoning_chain_of_thought import setup_sidebar_panels
        
        setup_sidebar_panels("gpt-4o-mini")
        
        # 各情報パネルが呼ばれたことを確認
        mock_info_panel.show_model_info.assert_called_once_with("gpt-4o-mini")
        mock_info_panel.show_session_info.assert_called_once()
        mock_info_panel.show_cost_info.assert_called_once_with("gpt-4o-mini")
        mock_info_panel.show_performance_info.assert_called_once()
        mock_info_panel.show_debug_panel.assert_called_once()
        mock_info_panel.show_settings.assert_called_once()


class TestBaseDemo:
    """BaseDemoクラスのテスト"""
    
    @patch('a06_reasoning_chain_of_thought.sanitize_key')
    def test_base_demo_initialization(self, mock_sanitize):
        """BaseDemoクラスの初期化テスト"""
        from a06_reasoning_chain_of_thought import BaseDemo
        
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
    
    @patch('a06_reasoning_chain_of_thought.OpenAI')
    @patch('a06_reasoning_chain_of_thought.setup_common_ui')
    def test_execute_method(self, mock_setup_ui, mock_openai):
        """executeメソッドのテスト"""
        from a06_reasoning_chain_of_thought import BaseDemo
        
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


class TestStepByStepReasoningDemo:
    """StepByStepReasoningDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """StepByStepReasoningDemoのインスタンスを作成"""
        from a06_reasoning_chain_of_thought import StepByStepReasoningDemo
        
        demo = StepByStepReasoningDemo("段階的推論")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander, 
                     mock_write, mock_text_area, mock_button, demo_instance):
        """run_demoメソッドのテスト"""
        
        mock_text_area.return_value = "2X + 1 = 5のとき、Xはいくつ？"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called_once()
            mock_button.assert_called_once()
            mock_write.assert_called()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_step_by_step_reasoning(self, mock_rerun, mock_success, 
                                           mock_spinner, demo_instance):
        """_process_step_by_step_reasoningメソッドのテスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "test_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_step_by_step_reasoning("Test question")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"reasoning_response_{demo_instance.safe_key}"] == mock_response
    
    @patch('a06_reasoning_chain_of_thought.ResponseProcessorUI')
    @patch('streamlit.subheader')
    def test_display_reasoning_results(self, mock_subheader, mock_response_ui, demo_instance):
        """_display_reasoning_resultsメソッドのテスト"""
        
        mock_response = MagicMock()
        
        with patch('streamlit.session_state', {
            f"reasoning_response_{demo_instance.safe_key}": mock_response
        }):
            demo_instance._display_reasoning_results()
            
            mock_subheader.assert_called_once_with("🤖 段階的推論結果")
            mock_response_ui.display_response.assert_called_once_with(mock_response)


class TestHypothesisTestDemo:
    """HypothesisTestDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """HypothesisTestDemoのインスタンスを作成"""
        from a06_reasoning_chain_of_thought import HypothesisTestDemo
        
        demo = HypothesisTestDemo("仮説検証推論")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_input')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander,
                     mock_write, mock_text_area, mock_text_input, mock_button, demo_instance):
        """run_demoメソッドのテスト"""
        
        mock_text_area.return_value = "Webアプリの初回表示が3秒以上かかる"
        mock_text_input.return_value = "画像ファイルのサイズが大きすぎて読み込み時間を圧迫している"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called_once()
            mock_text_input.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_hypothesis_test(self, mock_rerun, mock_success, mock_spinner, demo_instance):
        """_process_hypothesis_testメソッドのテスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "hypothesis_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_hypothesis_test("Test problem", "Test hypothesis")
            
            # APIが正しく呼ばれたか確認
            demo_instance.client.responses.create.assert_called_once()
            call_args = demo_instance.client.responses.create.call_args
            
            # メッセージの内容を確認
            messages = call_args[1]['input']
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert messages[1]['role'] == 'user'
            
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()


class TestTreeOfThoughtDemo:
    """TreeOfThoughtDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """TreeOfThoughtDemoのインスタンスを作成"""
        from a06_reasoning_chain_of_thought import TreeOfThoughtDemo
        
        demo = TreeOfThoughtDemo("思考の木")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander,
                     mock_write, mock_text_area, mock_button, demo_instance):
        """run_demoメソッドのテスト"""
        
        mock_text_area.return_value = "4, 9, 10, 13 の数字を使って24を作る"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_tree_of_thought(self, mock_rerun, mock_success, mock_spinner, demo_instance):
        """_process_tree_of_thoughtメソッドのテスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "tree_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_tree_of_thought("Test goal")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"tree_response_{demo_instance.safe_key}"] == mock_response
    
    @patch('streamlit.columns')
    @patch('streamlit.metric')
    @patch('streamlit.write')
    @patch('streamlit.subheader')
    @patch('a06_reasoning_chain_of_thought.ResponseProcessorUI')
    def test_display_tree_results_with_right_pane(self, mock_response_ui, mock_subheader,
                                                  mock_write, mock_metric, mock_columns, demo_instance):
        """_display_tree_resultsメソッドの右ペイン表示テスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.usage = MagicMock()
        mock_response.usage.total_tokens = 1000
        
        # カラムのモック
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        with patch('streamlit.session_state', {
            f"tree_response_{demo_instance.safe_key}": mock_response,
            f"tree_goal_{demo_instance.safe_key}": "Test goal",
            f"tree_time_{demo_instance.safe_key}": 2.5
        }):
            demo_instance._display_tree_results()
            
            mock_subheader.assert_called_once_with("🤖 Tree of Thought 結果")
            mock_columns.assert_called_once_with([3, 1])
            mock_response_ui.display_response.assert_called_once_with(mock_response)
            
            # 右ペインのメトリクスを確認
            assert mock_metric.call_count >= 3


class TestProsConsDecisionDemo:
    """ProsConsDecisionDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ProsConsDecisionDemoのインスタンスを作成"""
        from a06_reasoning_chain_of_thought import ProsConsDecisionDemo
        
        demo = ProsConsDecisionDemo("賛否比較決定")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.selectbox')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander,
                     mock_write, mock_text_area, mock_selectbox, mock_button, demo_instance):
        """run_demoメソッドのテスト"""
        
        mock_text_area.return_value = "リモートワークとオフィス出社、どちらを選ぶべきか？"
        mock_selectbox.return_value = "一般的"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called_once()
            mock_selectbox.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('time.time')
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_pros_cons_decision(self, mock_rerun, mock_success, 
                                       mock_spinner, mock_time, demo_instance):
        """_process_pros_cons_decisionメソッドのテスト"""
        
        # 時間のモック
        mock_time.side_effect = [0, 2.5]  # 開始時刻と終了時刻
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "decision_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_pros_cons_decision("Test topic", "一般的")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"decision_response_{demo_instance.safe_key}"] == mock_response
            assert st.session_state[f"decision_decision_{demo_instance.safe_key}"] == "Test topic"
            assert st.session_state[f"decision_time_{demo_instance.safe_key}"] == 2.5


class TestPlanExecuteReflectDemo:
    """PlanExecuteReflectDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """PlanExecuteReflectDemoのインスタンスを作成"""
        from a06_reasoning_chain_of_thought import PlanExecuteReflectDemo
        
        demo = PlanExecuteReflectDemo("計画実行振り返り")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.selectbox')
    @patch('streamlit.text_area')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander,
                     mock_write, mock_text_area, mock_selectbox, mock_button, demo_instance):
        """run_demoメソッドのテスト"""
        
        mock_text_area.return_value = "3週間以内にプログラミングスキルを向上させてWebアプリを完成させる"
        mock_selectbox.return_value = "標準"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        with patch('streamlit.session_state', {}):
            demo_instance.run_demo()
            
            mock_text_area.assert_called_once()
            mock_selectbox.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.rerun')
    def test_process_plan_execute_reflect(self, mock_rerun, mock_success, 
                                         mock_spinner, demo_instance):
        """_process_plan_execute_reflectメソッドのテスト"""
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.id = "reflect_response_id"
        demo_instance.client.responses.create.return_value = mock_response
        
        with patch('streamlit.session_state', {}):
            demo_instance._process_plan_execute_reflect("Test objective", "標準")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_rerun.assert_called_once()
            
            # セッション状態の確認
            assert st.session_state[f"reflect_response_{demo_instance.safe_key}"] == mock_response


class TestDemoManager:
    """DemoManagerクラスのテスト"""
    
    @patch('a06_reasoning_chain_of_thought.StepByStepReasoningDemo')
    @patch('a06_reasoning_chain_of_thought.HypothesisTestDemo')
    @patch('a06_reasoning_chain_of_thought.TreeOfThoughtDemo')
    @patch('a06_reasoning_chain_of_thought.ProsConsDecisionDemo')
    @patch('a06_reasoning_chain_of_thought.PlanExecuteReflectDemo')
    def test_demo_manager_initialization(self, mock_plan, mock_pros, mock_tree, 
                                        mock_hypothesis, mock_step):
        """DemoManagerの初期化テスト"""
        from a06_reasoning_chain_of_thought import DemoManager
        
        manager = DemoManager()
        
        assert hasattr(manager, 'demos')
        assert len(manager.demos) == 5
        assert "段階的推論（Step-by-Step）" in manager.demos
        assert "仮説検証推論（Hypothesis-Test）" in manager.demos
        assert "思考の木（Tree of Thought）" in manager.demos
        assert "賛否比較決定（Pros-Cons-Decision）" in manager.demos
        assert "計画実行振り返り（Plan-Execute-Reflect）" in manager.demos
    
    def test_get_demo_list(self):
        """get_demo_listメソッドのテスト"""
        from a06_reasoning_chain_of_thought import DemoManager
        
        manager = DemoManager()
        demo_list = manager.get_demo_list()
        
        assert isinstance(demo_list, list)
        assert len(demo_list) == 5
    
    def test_run_demo_method(self):
        """run_demoメソッドのテスト"""
        from a06_reasoning_chain_of_thought import DemoManager
        
        # モックデモクラス
        mock_demo_class = MagicMock()
        mock_demo_instance = MagicMock()
        mock_demo_class.return_value = mock_demo_instance
        
        manager = DemoManager()
        manager.demos = {"テストデモ": mock_demo_class}
        
        # run_demoメソッドの実行
        manager.run_demo("テストデモ", "gpt-4o-mini")
        
        # デモインスタンスが作成され実行されることを確認
        mock_demo_class.assert_called_once_with("テストデモ")
        mock_demo_instance.execute.assert_called_once_with("gpt-4o-mini")


class TestReasoningPatterns:
    """推論パターンのテスト"""
    
    def test_step_by_step_system_prompt(self):
        """Step-by-Step推論のシステムプロンプト確認"""
        from a06_reasoning_chain_of_thought import StepByStepReasoningDemo
        
        demo = StepByStepReasoningDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        
        with patch('streamlit.spinner'), \
             patch('streamlit.success'), \
             patch('streamlit.rerun'), \
             patch('streamlit.session_state', {}):
            
            demo._process_step_by_step_reasoning("Test question")
            
            # システムプロンプトの内容を確認
            call_args = demo.client.responses.create.call_args
            messages = call_args[1]['input']
            system_message = messages[0]['content']
            
            assert "段階的に問題を解く" in system_message
            assert "Step 1:" in system_message
            assert "Answer:" in system_message
            assert "信頼度" in system_message
    
    def test_hypothesis_test_system_prompt(self):
        """仮説検証推論のシステムプロンプト確認"""
        from a06_reasoning_chain_of_thought import HypothesisTestDemo
        
        demo = HypothesisTestDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        
        with patch('streamlit.spinner'), \
             patch('streamlit.success'), \
             patch('streamlit.rerun'), \
             patch('streamlit.session_state', {}):
            
            demo._process_hypothesis_test("Problem", "Hypothesis")
            
            # システムプロンプトの内容を確認
            call_args = demo.client.responses.create.call_args
            messages = call_args[1]['input']
            system_message = messages[0]['content']
            
            assert "仮説検証" in system_message
            assert "Evidence" in system_message
            assert "Evaluation" in system_message
            assert "Conclusion" in system_message
            assert "Confidence Score" in system_message
    
    def test_tree_of_thought_system_prompt(self):
        """Tree of Thought推論のシステムプロンプト確認"""
        from a06_reasoning_chain_of_thought import TreeOfThoughtDemo
        
        demo = TreeOfThoughtDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        
        with patch('streamlit.spinner'), \
             patch('streamlit.success'), \
             patch('streamlit.rerun'), \
             patch('streamlit.session_state', {}):
            
            demo._process_tree_of_thought("Test goal")
            
            # システムプロンプトの内容を確認
            call_args = demo.client.responses.create.call_args
            messages = call_args[1]['input']
            system_message = messages[0]['content']
            
            assert "Tree-of-Thoughts" in system_message
            assert "分岐" in system_message
            assert "評価" in system_message
            assert "最適パス" in system_message


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    @patch('a06_reasoning_chain_of_thought.config')
    def test_api_error_handling(self, mock_config, mock_error):
        """APIエラーハンドリングのテスト"""
        from a06_reasoning_chain_of_thought import StepByStepReasoningDemo
        
        mock_config.get.return_value = False
        
        demo = StepByStepReasoningDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        demo.client.responses.create.side_effect = Exception("API Error")
        
        with patch('streamlit.spinner'):
            demo._process_step_by_step_reasoning("Test question")
            
            mock_error.assert_called()
            assert "API Error" in mock_error.call_args[0][0]
    
    @patch('streamlit.error')
    @patch('streamlit.exception')
    @patch('a06_reasoning_chain_of_thought.config')
    def test_debug_mode_exception(self, mock_config, mock_exception, mock_error):
        """デバッグモードでの例外表示テスト"""
        from a06_reasoning_chain_of_thought import HypothesisTestDemo
        
        mock_config.get.return_value = True  # debug_mode = True
        
        demo = HypothesisTestDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        demo.client.responses.create.side_effect = Exception("Test Error")
        
        with patch('streamlit.spinner'):
            demo._process_hypothesis_test("Problem", "Hypothesis")
            
            mock_error.assert_called()
            mock_exception.assert_called()  # デバッグモードで例外詳細が表示される


class TestIntegration:
    """統合テスト"""
    
    @patch('streamlit.error')
    @patch('streamlit.sidebar.radio')
    @patch('a06_reasoning_chain_of_thought.UIHelper')
    @patch('a06_reasoning_chain_of_thought.setup_sidebar_panels')
    @patch('a06_reasoning_chain_of_thought.SessionStateManager')
    @patch('a06_reasoning_chain_of_thought.DemoManager')
    def test_main_function(self, mock_demo_manager, mock_session_state, mock_sidebar_panels,
                          mock_ui_helper, mock_radio, mock_error):
        """main関数のテスト"""
        from a06_reasoning_chain_of_thought import main
        
        # モックの設定
        mock_manager_instance = MagicMock()
        mock_demo_manager.return_value = mock_manager_instance
        mock_manager_instance.get_demo_list.return_value = ["段階的推論（Step-by-Step）"]
        mock_radio.return_value = "段階的推論（Step-by-Step）"
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        # main関数の実行
        main()
        
        # 各コンポーネントが呼ばれたことを確認
        mock_session_state.init_session_state.assert_called_once()
        mock_demo_manager.assert_called_once()
        mock_manager_instance.get_demo_list.assert_called_once()
        mock_manager_instance.run_demo.assert_called_once_with("段階的推論（Step-by-Step）", "gpt-4o-mini")
    
    @patch('streamlit.error')
    def test_main_no_api_key(self, mock_error):
        """APIキーなしでのmain関数実行テスト"""
        from a06_reasoning_chain_of_thought import main
        
        with patch('a06_reasoning_chain_of_thought.OpenAI') as mock_openai:
            mock_openai.side_effect = Exception("No API key")
            
            with patch('streamlit.sidebar.radio') as mock_radio, \
                 patch('a06_reasoning_chain_of_thought.UIHelper') as mock_ui_helper, \
                 patch('a06_reasoning_chain_of_thought.SessionStateManager'), \
                 patch('a06_reasoning_chain_of_thought.setup_sidebar_panels'):
                
                mock_radio.return_value = "段階的推論（Step-by-Step）"
                mock_ui_helper.select_model.return_value = "gpt-4o-mini"
                
                # エラーが発生してもクラッシュしない
                main()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])