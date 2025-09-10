"""
共通テストフィクスチャとテスト設定
"""
import os
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import pytest
import streamlit as st
from typing import Generator, Any, Dict
import tempfile
import yaml

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# テスト用環境変数の設定
os.environ["OPENAI_API_KEY"] = "test-api-key"
os.environ["OPENWEATHER_API_KEY"] = "test-weather-key"
os.environ["EXCHANGERATE_API_KEY"] = "test-exchange-key"


@pytest.fixture
def mock_openai_client():
    """OpenAIクライアントのモック"""
    with patch("openai.OpenAI") as mock_client:
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        
        # chat.completions.createのモック
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="Test response",
                    role="assistant",
                    function_call=None,
                    tool_calls=None
                ),
                finish_reason="stop"
            )
        ]
        mock_response.usage = MagicMock(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30
        )
        mock_response.model = "gpt-4o-mini"
        mock_response.id = "test-response-id"
        
        client_instance.chat.completions.create.return_value = mock_response
        
        yield client_instance


@pytest.fixture
def mock_streamlit_session_state():
    """Streamlit session stateのモック"""
    session_state = MagicMock()
    session_state.messages = []
    session_state.conversation_history = []
    session_state.token_count = 0
    session_state.execution_time = 0.0
    session_state.selected_model = "gpt-4o-mini"
    session_state.temperature = 0.7
    session_state.max_tokens = 1000
    
    with patch.object(st, "session_state", session_state):
        yield session_state


@pytest.fixture
def sample_config_data() -> Dict[str, Any]:
    """サンプル設定データ"""
    return {
        "models": {
            "frontier": {
                "gpt-5": {
                    "display_name": "GPT-5 (Latest Frontier)",
                    "description": "最新のフロンティアモデル",
                    "model_id": "gpt-5-latest",
                    "context_window": 200000,
                    "max_output_tokens": 32768,
                    "supports_vision": True,
                    "supports_function_calling": True,
                    "supports_structured_outputs": True,
                    "pricing": {
                        "input": 15.0,
                        "output": 60.0,
                        "cached_input": 7.5
                    }
                }
            },
            "standard": {
                "gpt-4o-mini": {
                    "display_name": "GPT-4o mini",
                    "description": "高速・低コストモデル",
                    "model_id": "gpt-4o-mini",
                    "context_window": 128000,
                    "max_output_tokens": 16384,
                    "supports_vision": True,
                    "supports_function_calling": True,
                    "supports_structured_outputs": True,
                    "pricing": {
                        "input": 0.15,
                        "output": 0.6,
                        "cached_input": 0.075
                    }
                }
            }
        },
        "sample_prompts": {
            "basic": [
                "こんにちは",
                "天気を教えて",
                "簡単な計算をして"
            ],
            "advanced": [
                "複雑な質問",
                "コードの生成",
                "データ分析"
            ]
        },
        "ui_settings": {
            "default_model": "gpt-4o-mini",
            "default_temperature": 0.7,
            "default_max_tokens": 1000,
            "enable_streaming": True
        }
    }


@pytest.fixture
def temp_config_file(sample_config_data) -> Generator[Path, None, None]:
    """一時的な設定ファイル"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(sample_config_data, f, allow_unicode=True)
        temp_path = Path(f.name)
    
    yield temp_path
    
    # クリーンアップ
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def mock_helper_api():
    """helper_api.pyのクラスのモック"""
    with patch("helper_api.ConfigManager") as mock_config_manager, \
         patch("helper_api.MessageManager") as mock_message_manager, \
         patch("helper_api.TokenManager") as mock_token_manager, \
         patch("helper_api.ResponseProcessor") as mock_response_processor, \
         patch("helper_api.OpenAIClient") as mock_openai_client:
        
        # ConfigManagerのモック設定
        config_instance = MagicMock()
        config_instance.get_model_config.return_value = {
            "model_id": "gpt-4o-mini",
            "display_name": "GPT-4o mini",
            "pricing": {"input": 0.15, "output": 0.6}
        }
        config_instance.get_all_models.return_value = ["gpt-4o-mini", "gpt-4o"]
        mock_config_manager.return_value = config_instance
        
        # MessageManagerのモック設定
        message_instance = MagicMock()
        message_instance.add_message.return_value = None
        message_instance.get_messages.return_value = []
        mock_message_manager.return_value = message_instance
        
        # TokenManagerのモック設定
        token_instance = MagicMock()
        token_instance.count_tokens.return_value = 100
        token_instance.calculate_cost.return_value = 0.015
        mock_token_manager.return_value = token_instance
        
        # ResponseProcessorのモック設定
        response_instance = MagicMock()
        response_instance.process_response.return_value = {
            "content": "Test response",
            "role": "assistant",
            "tokens": {"prompt": 10, "completion": 20, "total": 30},
            "cost": 0.015
        }
        mock_response_processor.return_value = response_instance
        
        # OpenAIClientのモック設定
        client_instance = MagicMock()
        client_instance.create_completion.return_value = MagicMock()
        mock_openai_client.return_value = client_instance
        
        yield {
            "ConfigManager": config_instance,
            "MessageManager": message_instance,
            "TokenManager": token_instance,
            "ResponseProcessor": response_instance,
            "OpenAIClient": client_instance
        }


@pytest.fixture
def mock_helper_st():
    """helper_st.pyのクラスのモック"""
    with patch("helper_st.UIHelper") as mock_ui_helper, \
         patch("helper_st.SessionStateManager") as mock_session_manager, \
         patch("helper_st.ResponseProcessorUI") as mock_response_ui, \
         patch("helper_st.InfoPanelManager") as mock_info_panel:
        
        # UIHelperのモック設定
        ui_instance = MagicMock()
        ui_instance.create_model_selector.return_value = "gpt-4o-mini"
        ui_instance.create_parameter_controls.return_value = (0.7, 1000)
        mock_ui_helper.return_value = ui_instance
        
        # SessionStateManagerのモック設定
        session_instance = MagicMock()
        session_instance.initialize.return_value = None
        session_instance.get.return_value = None
        session_instance.set.return_value = None
        mock_session_manager.return_value = session_instance
        
        # ResponseProcessorUIのモック設定
        response_ui_instance = MagicMock()
        response_ui_instance.display_response.return_value = None
        mock_response_ui.return_value = response_ui_instance
        
        # InfoPanelManagerのモック設定
        info_panel_instance = MagicMock()
        info_panel_instance.display_metrics.return_value = None
        mock_info_panel.return_value = info_panel_instance
        
        yield {
            "UIHelper": ui_instance,
            "SessionStateManager": session_instance,
            "ResponseProcessorUI": response_ui_instance,
            "InfoPanelManager": info_panel_instance
        }


@pytest.fixture(autouse=True)
def reset_streamlit():
    """各テスト前にStreamlitの状態をリセット"""
    # Streamlitのキャッシュをクリア
    st.cache_data.clear()
    st.cache_resource.clear()
    
    yield
    
    # テスト後のクリーンアップ
    st.cache_data.clear()
    st.cache_resource.clear()


@pytest.fixture
def mock_file_upload():
    """ファイルアップロードのモック"""
    mock_file = MagicMock()
    mock_file.name = "test.txt"
    mock_file.type = "text/plain"
    mock_file.size = 1024
    mock_file.read.return_value = b"Test file content"
    mock_file.getvalue.return_value = b"Test file content"
    
    return mock_file


@pytest.fixture
def mock_audio_file():
    """音声ファイルのモック"""
    mock_audio = MagicMock()
    mock_audio.name = "test.mp3"
    mock_audio.type = "audio/mpeg"
    mock_audio.size = 2048
    mock_audio.read.return_value = b"Mock audio data"
    
    return mock_audio


@pytest.fixture
def mock_image_file():
    """画像ファイルのモック"""
    mock_image = MagicMock()
    mock_image.name = "test.png"
    mock_image.type = "image/png"
    mock_image.size = 4096
    mock_image.read.return_value = b"Mock image data"
    
    return mock_image