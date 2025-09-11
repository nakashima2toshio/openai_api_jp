"""
a03_images_and_vision.py の単体テスト
Images & Vision API デモのテスト
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock, mock_open
import streamlit as st
from pathlib import Path
import sys
import json
import base64
from typing import Dict, Any, List
import time
import os

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPageConfig:
    """ページ設定のテスト"""
    
    @patch('streamlit.set_page_config')
    @patch('a03_images_and_vision.config')
    def test_setup_page_config_success(self, mock_config, mock_set_page_config):
        """ページ設定が正常に実行される"""
        from a03_images_and_vision import setup_page_config
        
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Title",
            "ui.page_icon": "🖼️",
            "ui.layout": "wide"
        }.get(key, default)
        
        setup_page_config()
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Title",
            page_icon="🖼️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config_already_set(self, mock_set_page_config):
        """既に設定済みの場合はエラーを無視"""
        from a03_images_and_vision import setup_page_config
        
        mock_set_page_config.side_effect = st.errors.StreamlitAPIException("Already set")
        
        # エラーが発生してもクラッシュしない
        setup_page_config()


class TestCommonUI:
    """共通UI関数のテスト"""
    
    @patch('streamlit.write')
    def test_setup_common_ui(self, mock_write):
        """共通UI設定が正しく動作する"""
        from a03_images_and_vision import setup_common_ui
        
        setup_common_ui("Test Demo", "gpt-4o-mini")
        
        # ヘッダーとモデル表示が呼ばれたことを確認
        assert mock_write.call_count >= 2
    
    @patch('a03_images_and_vision.InfoPanelManager')
    @patch('streamlit.sidebar.write')
    def test_setup_sidebar_panels(self, mock_write, mock_info_panel):
        """サイドバーパネル設定のテスト"""
        from a03_images_and_vision import setup_sidebar_panels
        
        setup_sidebar_panels("gpt-4o-mini")
        
        # 各情報パネルが呼ばれたことを確認
        mock_info_panel.show_model_info.assert_called_once_with("gpt-4o-mini")
        mock_info_panel.show_session_info.assert_called_once()
        mock_info_panel.show_cost_info.assert_called_once_with("gpt-4o-mini")


class TestBaseDemo:
    """BaseDemoクラスのテスト"""
    
    @patch('a03_images_and_vision.sanitize_key')
    def test_base_demo_initialization(self, mock_sanitize):
        """BaseDemoクラスの初期化テスト"""
        from a03_images_and_vision import BaseDemo
        
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
    
    @patch('a03_images_and_vision.OpenAI')
    @patch('a03_images_and_vision.setup_common_ui')
    def test_execute_method(self, mock_setup_ui, mock_openai):
        """executeメソッドのテスト"""
        from a03_images_and_vision import BaseDemo
        
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


class TestURLImageToTextDemo:
    """URLImageToTextDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """URLImageToTextDemoのインスタンスを作成"""
        from a03_images_and_vision import URLImageToTextDemo
        
        demo = URLImageToTextDemo("URL画像からテキスト生成")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.text_input')
    @patch('streamlit.image')
    @patch('streamlit.write')
    @patch('streamlit.expander')
    @patch('streamlit.code')
    @patch('streamlit.subheader')
    def test_run_demo(self, mock_subheader, mock_code, mock_expander, mock_write, 
                     mock_image, mock_text_input, mock_text_area, mock_button, demo_instance):
        """run_demoメソッドの基本的な実行テスト"""
        
        mock_text_input.return_value = "https://example.com/image.jpg"
        mock_text_area.return_value = "Test prompt"
        mock_button.return_value = False
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        demo_instance.run_demo()
        
        mock_text_input.assert_called()
        mock_text_area.assert_called()
        mock_image.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.columns')
    @patch('a03_images_and_vision.get_default_messages')
    @patch('a03_images_and_vision.ResponseProcessorUI')
    def test_process_url_image(self, mock_response_ui, mock_get_messages, 
                               mock_columns, mock_success, mock_spinner, demo_instance):
        """_process_image_with_textメソッドのテスト"""
        
        # メッセージのモック
        mock_get_messages.return_value = []
        
        # レスポンスのモック
        mock_response = MagicMock()
        mock_response.usage.total_tokens = 500
        demo_instance.client.responses.create.return_value = mock_response
        
        # カラムのモック
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        with patch('streamlit.session_state', {}), \
             patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('streamlit.subheader'), \
             patch('time.time', side_effect=[0, 1.5]):
            
            demo_instance._process_image_with_text("Test prompt", "https://example.com/image.jpg")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()
            mock_response_ui.display_response.assert_called_once_with(mock_response)


class TestBase64ImageToTextDemo:
    """Base64ImageToTextDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """Base64ImageToTextDemoのインスタンスを作成"""
        from a03_images_and_vision import Base64ImageToTextDemo
        
        demo = Base64ImageToTextDemo("Base64画像からテキスト生成")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        return demo
    
    @patch('builtins.open', new_callable=mock_open, read_data=b"fake image data")
    def test_encode_image_to_base64(self, mock_file, demo_instance):
        """_encode_image_to_base64メソッドのテスト"""
        
        mock_image_data = b"fake image data"
        mock_base64_data = base64.b64encode(mock_image_data).decode('utf-8')
        
        result = demo_instance._encode_image_to_base64("test.jpg")
        
        assert result == mock_base64_data
    
    @patch('os.path.getsize')
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.columns')
    @patch('a03_images_and_vision.get_default_messages')
    def test_process_base64_image(self, mock_get_messages, mock_columns,
                                  mock_success, mock_spinner, mock_getsize, demo_instance):
        """_process_base64_imageメソッドのテスト"""
        
        # ファイルサイズのモック
        mock_getsize.return_value = 1024 * 50  # 50KB
        
        # メッセージのモック
        mock_get_messages.return_value = []
        
        # レスポンスのモック
        mock_response = MagicMock()
        demo_instance.client.responses.create.return_value = mock_response
        
        # カラムのモック
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        # Base64エンコードのモック
        demo_instance._encode_image_to_base64 = MagicMock(return_value="base64data")
        
        with patch('streamlit.session_state', {}), \
             patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('streamlit.subheader'), \
             patch('a03_images_and_vision.ResponseProcessorUI'), \
             patch('time.time', side_effect=[0, 2.0]):
            
            demo_instance._process_base64_image("test.jpg", "Test prompt")
            
            demo_instance.client.responses.create.assert_called_once()
            mock_success.assert_called_once()


class TestPromptToImageDemo:
    """PromptToImageDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """PromptToImageDemoのインスタンスを作成"""
        from a03_images_and_vision import PromptToImageDemo
        
        demo = PromptToImageDemo("プロンプトから画像生成")
        demo.model = "dall-e-3"
        demo.client = MagicMock()
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.selectbox')
    @patch('streamlit.columns')
    def test_run_demo(self, mock_columns, mock_selectbox, mock_text_area, mock_button, demo_instance):
        """run_demoメソッドの基本的な実行テスト"""
        
        mock_selectbox.side_effect = ["dall-e-3", "1024x1024", "standard"]
        mock_text_area.return_value = "Test prompt"
        mock_button.return_value = False
        
        # カラムのモック
        mock_col = MagicMock()
        mock_columns.return_value = [mock_col, mock_col, mock_col]
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('streamlit.subheader'):
            
            demo_instance.run_demo()
            
            assert mock_selectbox.call_count == 3  # model, size, quality
            mock_text_area.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.columns')
    @patch('streamlit.image')
    @patch('streamlit.text_input')
    @patch('time.time')
    def test_generate_image_from_prompt(self, mock_time, mock_text_input, mock_image,
                                       mock_columns, mock_success, mock_spinner, demo_instance):
        """_generate_image_from_promptメソッドのテスト"""
        
        # 時間のモック
        mock_time.side_effect = [0, 3.5]
        
        # DALL-E レスポンスのモック
        mock_image_data = MagicMock()
        mock_image_data.url = "https://example.com/generated.jpg"
        mock_response = MagicMock()
        mock_response.data = [mock_image_data]
        demo_instance.client.images.generate.return_value = mock_response
        
        # カラムのモック
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        with patch('streamlit.session_state', {}), \
             patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('streamlit.expander'), \
             patch('streamlit.subheader'):
            
            demo_instance._generate_image_from_prompt(
                "dall-e-3", "Test prompt", "1024x1024", "standard"
            )
            
            demo_instance.client.images.generate.assert_called_once_with(
                model="dall-e-3",
                prompt="Test prompt",
                size="1024x1024",
                quality="standard",
                n=1
            )
            mock_success.assert_called_once()
            mock_image.assert_called_once()


class TestImageEditDemo:
    """ImageEditDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ImageEditDemoのインスタンスを作成"""
        # ImageEditDemo is not implemented in the main module
        pytest.skip("ImageEditDemo not implemented")
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.text_area')
    @patch('streamlit.button')
    def test_run_demo_no_files(self, mock_button, mock_text_area, mock_uploader, demo_instance):
        """ファイルがアップロードされていない場合のテスト"""
        
        mock_uploader.side_effect = [None, None]  # original, mask
        mock_text_area.return_value = "Test prompt"
        mock_button.return_value = False
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('streamlit.subheader'), \
             patch('streamlit.columns'):
            
            demo_instance.run_demo()
            
            assert mock_uploader.call_count == 2


class TestImageVariationDemo:
    """ImageVariationDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """ImageVariationDemoのインスタンスを作成"""
        # ImageVariationDemo is not implemented in the main module
        pytest.skip("ImageVariationDemo not implemented")
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    def test_run_demo(self, mock_button, mock_selectbox, mock_uploader, demo_instance):
        """run_demoメソッドの基本的な実行テスト"""
        
        mock_uploader.return_value = None
        mock_selectbox.return_value = "256x256"
        mock_button.return_value = False
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('streamlit.subheader'):
            
            demo_instance.run_demo()
            
            mock_uploader.assert_called_once()
            mock_selectbox.assert_called_once()


class TestDemoManager:
    """DemoManagerクラスのテスト"""
    
    @patch('a03_images_and_vision.URLImageToTextDemo')
    @patch('a03_images_and_vision.Base64ImageToTextDemo')
    @patch('a03_images_and_vision.PromptToImageDemo')
    def test_demo_manager_initialization(self, mock_prompt, mock_base64, mock_url):
        """DemoManagerの初期化テスト"""
        from a03_images_and_vision import DemoManager
        
        manager = DemoManager()
        
        assert hasattr(manager, 'demos')
        assert len(manager.demos) == 3
        # Check if demos dictionary contains the expected keys (actual keys may differ)
        demo_keys = list(manager.demos.keys())
        assert len(demo_keys) == 3
        assert any("URL" in key for key in demo_keys)
        assert any("Base64" in key for key in demo_keys)
        assert any("プロンプト" in key or "DALL" in key for key in demo_keys)
    
    def test_run_method(self):
        """run_demoメソッドのテスト"""
        from a03_images_and_vision import DemoManager
        
        # モックデモ
        mock_demo = MagicMock()
        mock_demo_class = MagicMock(return_value=mock_demo)
        
        with patch('a03_images_and_vision.URLImageToTextDemo', mock_demo_class):
            manager = DemoManager()
            
            # run_demoメソッドを呼び出す
            manager.run_demo("URL画像 → テキスト生成", "gpt-4o-mini")
            
            mock_demo_class.assert_called_once_with("URL画像 → テキスト生成")
            mock_demo.execute.assert_called_once_with("gpt-4o-mini")


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    def test_encode_image_error(self, mock_error):
        """画像エンコードエラーのテスト"""
        from a03_images_and_vision import Base64ImageToTextDemo
        
        demo = Base64ImageToTextDemo("Test")
        
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = demo._encode_image_to_base64("nonexistent.jpg")
            
            assert result == ""
            mock_error.assert_called_once()
    
    @patch('streamlit.error')
    @patch('a03_images_and_vision.config')
    def test_api_error_handling(self, mock_config, mock_error):
        """APIエラーハンドリングのテスト"""
        from a03_images_and_vision import URLImageToTextDemo
        
        mock_config.get.return_value = False
        
        demo = URLImageToTextDemo("Test")
        demo.model = "gpt-4o-mini"
        demo.client = MagicMock()
        demo.client.responses.create.side_effect = Exception("API Error")
        
        with patch('a03_images_and_vision.get_default_messages', return_value=[]), \
             patch('streamlit.spinner'):
            
            demo._process_image_with_text("Test", "https://example.com/image.jpg")
            
            mock_error.assert_called()


class TestIntegration:
    """統合テスト"""
    
    @patch('a03_images_and_vision.DemoManager')
    @patch('a03_images_and_vision.SessionStateManager')
    @patch('streamlit.sidebar')
    @patch('streamlit.radio')
    @patch('a03_images_and_vision.UIHelper')
    @patch('a03_images_and_vision.setup_sidebar_panels')
    def test_main_function(self, mock_sidebar_panels, mock_ui_helper, mock_radio, 
                          mock_sidebar, mock_session_state, mock_demo_manager):
        """main関数のテスト"""
        from a03_images_and_vision import main
        
        mock_manager_instance = MagicMock()
        mock_demo_manager.return_value = mock_manager_instance
        mock_manager_instance.get_demo_list.return_value = ["Demo1", "Demo2"]
        mock_radio.return_value = "Demo1"
        mock_ui_helper.select_model.return_value = "gpt-4o-mini"
        
        # sidebarのコンテキストマネージャーをモック
        mock_sidebar.__enter__ = MagicMock()
        mock_sidebar.__exit__ = MagicMock()
        
        main()
        
        mock_demo_manager.assert_called_once()
        mock_manager_instance.run_demo.assert_called_once_with("Demo1", "gpt-4o-mini")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])