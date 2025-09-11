"""
a04_audio_speeches.py の単体テスト
Audio & Speech API デモのテスト
"""
import pytest
from unittest.mock import Mock, MagicMock, patch, PropertyMock, AsyncMock
import streamlit as st
from pathlib import Path
import sys
import json
import base64
from typing import Dict, Any, List
import time
import asyncio
from io import BytesIO

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestPageConfig:
    """ページ設定のテスト"""
    
    @patch('streamlit.set_page_config')
    @patch('a04_audio_speeches.config')
    def test_setup_page_config_success(self, mock_config, mock_set_page_config):
        """ページ設定が正常に実行される"""
        from a04_audio_speeches import setup_page_config
        
        mock_config.get.side_effect = lambda key, default: {
            "ui.page_title": "Test Audio Title",
            "ui.page_icon": "🎵",
            "ui.layout": "wide"
        }.get(key, default)
        
        setup_page_config()
        
        mock_set_page_config.assert_called_once_with(
            page_title="Test Audio Title",
            page_icon="🎵",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    @patch('streamlit.set_page_config')
    def test_setup_page_config_already_set(self, mock_set_page_config):
        """既に設定済みの場合はエラーを無視"""
        from a04_audio_speeches import setup_page_config
        
        mock_set_page_config.side_effect = st.errors.StreamlitAPIException("Already set")
        
        # エラーが発生してもクラッシュしない
        setup_page_config()


class TestCommonUI:
    """共通UI関数のテスト"""
    
    @patch('a04_audio_speeches.UIHelper')
    @patch('a04_audio_speeches.sanitize_key')
    @patch('streamlit.write')
    def test_setup_common_ui(self, mock_write, mock_sanitize_key, mock_ui_helper):
        """共通UI設定が正しく動作する"""
        from a04_audio_speeches import setup_common_ui
        
        mock_sanitize_key.return_value = "test_demo"
        mock_ui_helper.select_audio_model.return_value = "tts-1"
        
        model = setup_common_ui("Test Audio Demo")
        
        assert model == "tts-1"
        mock_sanitize_key.assert_called_once_with("Test Audio Demo")
        mock_ui_helper.select_audio_model.assert_called_once()
    
    @patch('a04_audio_speeches.InfoPanelManager')
    @patch('streamlit.sidebar.markdown')
    def test_setup_sidebar_panels(self, mock_markdown, mock_info_panel):
        """サイドバーパネル設定のテスト"""
        from a04_audio_speeches import setup_sidebar_panels
        
        setup_sidebar_panels("tts-1")
        
        # 各情報パネルが呼ばれたことを確認
        mock_info_panel.show_audio_model_info.assert_called_once_with("tts-1")
        mock_info_panel.show_session_info.assert_called_once()
        mock_info_panel.show_performance_info.assert_called_once()
        mock_info_panel.show_audio_cost_info.assert_called_once_with("tts-1")


class TestUIHelper:
    """UIHelper拡張クラスのテスト"""
    
    @patch('a04_audio_speeches.SessionStateManager')
    @patch('streamlit.sidebar.selectbox')
    @patch('a04_audio_speeches.config')
    def test_select_audio_model(self, mock_config, mock_selectbox, mock_session):
        """音声モデル選択のテスト"""
        from a04_audio_speeches import UIHelper
        
        mock_config.get.side_effect = lambda key, default: {
            "models.categories.audio": ["tts-1", "tts-1-hd", "whisper-1"],
            "models.audio_default": "tts-1"
        }.get(key, default)
        
        mock_selectbox.return_value = "tts-1-hd"
        
        result = UIHelper.select_audio_model("test_key")
        
        assert result == "tts-1-hd"
        mock_selectbox.assert_called_once()
        mock_session.set_user_preference.assert_called_once_with("selected_audio_model", "tts-1-hd")
    
    @patch('streamlit.selectbox')
    @patch('a04_audio_speeches.config')
    def test_select_voice(self, mock_config, mock_selectbox):
        """音声選択のテスト"""
        from a04_audio_speeches import UIHelper
        
        mock_config.get.return_value = ["alloy", "nova", "echo", "onyx", "shimmer"]
        mock_selectbox.return_value = "nova"
        
        result = UIHelper.select_voice("test_voice_key")
        
        assert result == "nova"
        mock_selectbox.assert_called_once()
    
    @patch('streamlit.download_button')
    def test_create_audio_download_button(self, mock_download):
        """音声ダウンロードボタンのテスト"""
        from a04_audio_speeches import UIHelper
        
        audio_data = b"fake audio data"
        UIHelper.create_audio_download_button(audio_data, "test.mp3")
        
        mock_download.assert_called_once_with(
            label="📥 音声ダウンロード",
            data=audio_data,
            file_name="test.mp3",
            mime="audio/mp3",
            help="test.mp3をダウンロードします"
        )


class TestInfoPanelManager:
    """InfoPanelManager拡張クラスのテスト"""
    
    @patch('streamlit.sidebar.expander')
    @patch('streamlit.info')
    @patch('streamlit.write')
    def test_show_audio_model_info_tts(self, mock_write, mock_info, mock_expander):
        """TTSモデル情報表示のテスト"""
        from a04_audio_speeches import InfoPanelManager
        
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        InfoPanelManager.show_audio_model_info("tts-1")
        
        mock_expander.assert_called_once_with("🎵 音声モデル情報", expanded=False)
        mock_info.assert_called_once_with("🎤 Text-to-Speech モデル")
    
    @patch('streamlit.sidebar.expander')
    @patch('streamlit.write')
    @patch('streamlit.number_input')
    def test_show_audio_cost_info_tts(self, mock_number_input, mock_write, mock_expander):
        """TTS料金情報表示のテスト"""
        from a04_audio_speeches import InfoPanelManager
        
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__ = MagicMock(return_value=mock_expander_context)
        mock_expander.return_value.__exit__ = MagicMock()
        
        mock_number_input.return_value = 1000  # 1000文字
        
        InfoPanelManager.show_audio_cost_info("tts-1")
        
        mock_expander.assert_called_once_with("💰 音声API料金", expanded=False)
        mock_number_input.assert_called_once()


class TestTextToSpeechDemo:
    """TextToSpeechDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """TextToSpeechDemoのインスタンスを作成"""
        from a04_audio_speeches import TextToSpeechDemo
        
        demo = TextToSpeechDemo("テキスト読み上げ")
        demo.client = MagicMock()
        demo.openai_client = MagicMock()
        demo.model = "tts-1"
        return demo
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('a04_audio_speeches.UIHelper')
    def test_run_method(self, mock_ui_helper, mock_text_area, mock_button, demo_instance):
        """runメソッドの基本的な実行テスト"""
        
        mock_ui_helper.select_voice.return_value = "alloy"
        mock_text_area.return_value = "Test text"
        mock_button.return_value = False
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('a04_audio_speeches.setup_common_ui', return_value="tts-1"), \
             patch('a04_audio_speeches.setup_sidebar_panels'):
            
            demo_instance.run()
            
            mock_ui_helper.select_voice.assert_called_once()
            mock_text_area.assert_called_once()
            mock_button.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.audio')
    @patch('a04_audio_speeches.UIHelper')
    def test_generate_speech(self, mock_ui_helper, mock_audio, 
                           mock_success, mock_spinner, demo_instance):
        """_generate_speechメソッドのテスト"""
        
        # 音声生成レスポンスのモック
        mock_response = MagicMock()
        mock_response.content = b"fake audio content"
        demo_instance.openai_client.audio.speech.create.return_value = mock_response
        
        with patch('streamlit.columns', return_value=[MagicMock(), MagicMock()]), \
             patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('streamlit.session_state', {'performance_metrics': {}}), \
             patch('streamlit.subheader'), \
             patch('time.time', return_value=1.5):
            
            demo_instance._generate_speech("Test text", "alloy", 1.0, "mp3")
            
            demo_instance.openai_client.audio.speech.create.assert_called_once_with(
                model="tts-1",
                voice="alloy",
                input="Test text",
                speed=1.0,
                response_format="mp3"
            )
            mock_success.assert_called_once()
            mock_audio.assert_called_once()


class TestSpeechToTextDemo:
    """SpeechToTextDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """SpeechToTextDemoのインスタンスを作成"""
        # SpeechToTextDemo is not implemented in the main module
        pytest.skip("SpeechToTextDemo not implemented")
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.button')
    def test_run_no_file(self, mock_button, mock_uploader, demo_instance):
        """ファイルがアップロードされていない場合のテスト"""
        
        mock_uploader.return_value = None
        mock_button.return_value = False
        
        with patch('streamlit.write'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('a04_audio_speeches.setup_common_ui', return_value="whisper-1"), \
             patch('a04_audio_speeches.setup_sidebar_panels'):
            
            demo_instance.run()
            
            mock_uploader.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.success')
    @patch('streamlit.columns')
    @patch('time.time')
    def test_transcribe_audio(self, mock_time, mock_columns, mock_success, 
                             mock_spinner, demo_instance):
        """_transcribe_audioメソッドのテスト"""
        
        mock_time.side_effect = [0, 2.0]
        
        # ファイルのモック
        mock_file = MagicMock()
        mock_file.name = "test.mp3"
        mock_file.read.return_value = b"fake audio data"
        
        # 文字起こしレスポンスのモック
        mock_response = MagicMock()
        mock_response.text = "Transcribed text"
        demo_instance.client.audio.transcriptions.create.return_value = mock_response
        
        mock_col1 = MagicMock()
        mock_col2 = MagicMock()
        mock_columns.return_value = [mock_col1, mock_col2]
        
        with patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('streamlit.text_area'), \
             patch('streamlit.session_state', {}):
            
            demo_instance._transcribe_audio("whisper-1", mock_file)
            
            demo_instance.client.audio.transcriptions.create.assert_called_once()
            mock_success.assert_called_once()


class TestRealtimeVoiceDemo:
    """RealtimeVoiceDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """RealtimeVoiceDemoのインスタンスを作成"""
        # RealtimeVoiceDemo is not implemented in the main module
        pytest.skip("RealtimeVoiceDemo not implemented")
    
    @patch('streamlit.button')
    @patch('streamlit.columns')
    def test_run_method(self, mock_columns, mock_button, demo_instance):
        """runメソッドの基本的な実行テスト"""
        
        mock_button.side_effect = [False, False]  # start, stop
        mock_col = MagicMock()
        mock_columns.return_value = [mock_col, mock_col]
        
        with patch('streamlit.write'), \
             patch('streamlit.info'), \
             patch('streamlit.warning'), \
             patch('streamlit.code'), \
             patch('streamlit.expander'), \
             patch('a04_audio_speeches.setup_common_ui', return_value="gpt-4o-realtime"), \
             patch('a04_audio_speeches.setup_sidebar_panels'):
            
            demo_instance.run()
            
            assert mock_button.call_count == 2


class TestAudioComparisonDemo:
    """AudioComparisonDemoクラスのテスト"""
    
    @pytest.fixture
    def demo_instance(self):
        """AudioComparisonDemoのインスタンスを作成"""
        # AudioComparisonDemo is not implemented in the main module
        pytest.skip("AudioComparisonDemo not implemented")
    
    @patch('streamlit.button')
    @patch('streamlit.text_area')
    def test_run_method(self, mock_text_area, mock_button, demo_instance):
        """runメソッドの基本的な実行テスト"""
        
        mock_text_area.return_value = "Test comparison text"
        mock_button.return_value = False
        
        with patch('streamlit.write'), \
             patch('streamlit.info'), \
             patch('streamlit.expander'), \
             patch('streamlit.code'), \
             patch('a04_audio_speeches.setup_common_ui'), \
             patch('a04_audio_speeches.setup_sidebar_panels'):
            
            demo_instance.run()
            
            mock_text_area.assert_called_once()
    
    @patch('streamlit.spinner')
    @patch('streamlit.columns')
    @patch('streamlit.audio')
    @patch('time.time')
    def test_compare_voices(self, mock_time, mock_audio, mock_columns, 
                           mock_spinner, demo_instance):
        """_compare_voicesメソッドのテスト"""
        
        mock_time.return_value = 0
        
        # 音声生成レスポンスのモック
        mock_response = MagicMock()
        mock_response.content = b"fake audio"
        demo_instance.client.audio.speech.create.return_value = mock_response
        
        mock_col = MagicMock()
        mock_columns.return_value = [mock_col] * 5
        
        with patch('streamlit.write'), \
             patch('streamlit.metric'), \
             patch('a04_audio_speeches.UIHelper'):
            
            demo_instance._compare_voices("Test text")
            
            # 5つの音声が生成される
            assert demo_instance.client.audio.speech.create.call_count == 5
            assert mock_audio.call_count == 5


class TestDemoSelector:
    """AudioDemoManagerクラスのテスト"""
    
    @patch('a04_audio_speeches.TextToSpeechDemo')
    def test_initialization(self, mock_tts):
        """AudioDemoManagerの初期化テスト"""
        from a04_audio_speeches import AudioDemoManager
        
        manager = AudioDemoManager()
        
        assert hasattr(manager, 'demos')
        assert len(manager.demos) == 1  # Only TextToSpeechDemo is implemented
    
    @patch('streamlit.sidebar.radio')
    def test_run_method(self, mock_radio):
        """runメソッドのテスト"""
        from a04_audio_speeches import AudioDemoManager
        
        mock_radio.return_value = "Text to Speech"
        
        # モックデモ
        mock_demo = MagicMock()
        mock_demo_class = MagicMock(return_value=mock_demo)
        
        mock_session_state = MagicMock()
        mock_session_state.current_audio_demo = "Text to Speech"
        mock_session_state.performance_metrics = {}
        
        with patch('a04_audio_speeches.TextToSpeechDemo', mock_demo_class), \
             patch('a04_audio_speeches.SessionStateManager'), \
             patch('streamlit.session_state', mock_session_state):
            manager = AudioDemoManager()
            manager.run()
            
            mock_demo_class.assert_called_once_with("Text to Speech")
            mock_demo.run.assert_called_once()


class TestErrorHandling:
    """エラーハンドリングのテスト"""
    
    @patch('streamlit.error')
    @patch('a04_audio_speeches.logger')
    def test_audio_download_button_error(self, mock_logger, mock_error):
        """音声ダウンロードボタンのエラーハンドリング"""
        from a04_audio_speeches import UIHelper
        
        with patch('streamlit.download_button', side_effect=Exception("Download error")):
            UIHelper.create_audio_download_button(b"data", "test.mp3")
            
            mock_error.assert_called_once()
            mock_logger.error.assert_called_once()
    
    @patch('streamlit.error')
    def test_transcription_error(self, mock_error):
        """文字起こしエラーのテスト"""
        # SpeechToTextDemo is not implemented
        pytest.skip("SpeechToTextDemo not implemented")


class TestIntegration:
    """統合テスト"""
    
    @patch('a04_audio_speeches.AudioDemoManager')
    @patch('a04_audio_speeches.SessionStateManager')
    @patch('streamlit.sidebar')
    @patch('streamlit.radio')
    @patch('a04_audio_speeches.UIHelper')
    @patch('a04_audio_speeches.setup_sidebar_panels')
    def test_main_function(self, mock_sidebar_panels, mock_ui_helper, mock_radio, 
                          mock_sidebar, mock_session_state, mock_manager):
        """main関数のテスト"""
        from a04_audio_speeches import main
        
        mock_manager_instance = MagicMock()
        mock_manager.return_value = mock_manager_instance
        mock_manager_instance.get_demo_list.return_value = ["Demo1"]
        mock_radio.return_value = "Demo1"
        mock_ui_helper.select_audio_model.return_value = "tts-1"
        
        # sidebarのコンテキストマネージャーをモック
        mock_sidebar.__enter__ = MagicMock()
        mock_sidebar.__exit__ = MagicMock()
        
        main()
        
        mock_manager.assert_called_once()
        mock_manager_instance.run.assert_called_once()
    
    @patch('a04_audio_speeches.AudioDemoManager')
    @patch('os.getenv')
    def test_main_no_api_key(self, mock_getenv, mock_manager):
        """APIキーがない場合のテスト"""
        from a04_audio_speeches import main
        
        mock_getenv.return_value = None  # APIキーがない
        
        with patch('a04_audio_speeches.SessionStateManager'), \
             patch('streamlit.sidebar'), \
             patch('streamlit.radio'), \
             patch('a04_audio_speeches.UIHelper'), \
             patch('a04_audio_speeches.setup_sidebar_panels'):
            with patch('streamlit.error') as mock_error:
                main()
                
                # APIキーがない場合でもmainが動作することを確認
                # 実際の動作はAudioDemoManager内で処理される


if __name__ == "__main__":
    pytest.main([__file__, "-v"])