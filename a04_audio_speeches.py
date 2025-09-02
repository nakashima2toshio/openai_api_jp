# streamlit run a04_audio_speeches.py --server.port=8504
# --------------------------------------------------
# OpenAI Audio & Speech API デモアプリケーション
# Streamlitを使用したインタラクティブな音声APIテストツール
# 統一化改修版: a10_00_responses_api.pyの構成・構造・ライブラリ・エラー処理の完全統一
# --------------------------------------------------
import os
import sys
import asyncio
import base64
import time
import random
from io import BytesIO
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union
import logging
import textwrap

import streamlit as st

# プロジェクトディレクトリの設定
BASE_DIR = Path(__file__).resolve().parent.parent
THIS_DIR = Path(__file__).resolve().parent

# PYTHONPATHに親ディレクトリを追加
sys.path.insert(0, str(BASE_DIR))

# ヘルパーモジュールをインポート（統一化）
try:
    from helper_st import (
        UIHelper as BaseUIHelper,
        MessageManagerUI, ResponseProcessorUI,
        SessionStateManager, error_handler_ui, timer_ui,
        InfoPanelManager as BaseInfoPanelManager,
        safe_streamlit_json,
    )
    from helper_api import (
        config, logger, TokenManager, OpenAIClient,
        EasyInputMessageParam, ResponseInputTextParam,
        ConfigManager, MessageManager, sanitize_key,
        error_handler, timer, get_default_messages,
        ResponseProcessor, format_timestamp
    )
except ImportError as e:
    st.error(f"ヘルパーモジュールのインポートに失敗しました: {e}")
    st.info("必要なファイルが存在することを確認してください: helper_st.py, helper_api.py")
    st.stop()

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)

# ページ設定
def setup_page_config():
    """ページ設定（重複実行エラー回避）"""
    try:
        st.set_page_config(
            page_title=config.get("ui.page_title", "OpenAI Audio & Speech API Demo"),
            page_icon=config.get("ui.page_icon", "🎵"),
            layout=config.get("ui.layout", "wide"),
            initial_sidebar_state="expanded"
        )
    except st.errors.StreamlitAPIException:
        pass

setup_page_config()

# データディレクトリの設定
DATA_DIR = Path(config.get("paths.data", "data"))
DATA_DIR.mkdir(exist_ok=True)

# ==================================================
# 共通UI関数（統一化版）
# ==================================================
def setup_common_ui(demo_name: str) -> str:
    """共通UI設定（統一化版）"""
    safe_key = sanitize_key(demo_name)
    st.write(f"# {demo_name}")

    # モデル選択（音声用モデル選択）
    model = UIHelper.select_audio_model(f"model_{safe_key}")
    st.write("選択したモデル:", model)
    return model

def setup_sidebar_panels(selected_model: str):
    """サイドバーパネルの統一設定（音声API用）"""
    st.sidebar.markdown("### 🎵 Audio API 情報")  # ← expanded=False を削除
    InfoPanelManager.show_audio_model_info(selected_model)
    InfoPanelManager.show_session_info()
    InfoPanelManager.show_performance_info()
    InfoPanelManager.show_audio_cost_info(selected_model)
    InfoPanelManager.show_debug_panel()
    InfoPanelManager.show_settings()

# ==================================================
# UIHelper拡張（音声用）
# ==================================================
class UIHelper(BaseUIHelper):
    """UIHelper拡張（音声API用）"""

    @staticmethod
    def select_audio_model(key: str = "audio_model_selection") -> str:
        """音声API用モデル選択"""
        audio_models = config.get("models.categories.audio", [
            "tts-1", "tts-1-hd", "gpt-4o-mini-tts",
            "whisper-1", "gpt-4o-transcribe"
        ])
        default_model = config.get("models.audio_default", "tts-1")
        default_index = audio_models.index(default_model) if default_model in audio_models else 0

        selected = st.sidebar.selectbox(
            "音声モデルを選択",
            audio_models,
            index=default_index,
            key=key,
            help="利用するOpenAI音声モデルを選択してください",
        )
        SessionStateManager.set_user_preference("selected_audio_model", selected)
        return selected

    @staticmethod
    def select_voice(key: str = "voice_selection") -> str:
        """音声選択UI"""
        voices = config.get("audio.voices", ["alloy", "nova", "echo", "onyx", "shimmer"])
        return st.selectbox(
            "Voice",
            voices,
            index=0,
            key=key,
            help="音声の種類を選択してください"
        )

    @staticmethod
    def create_audio_download_button(audio_data: bytes, filename: str, label: str = "📥 音声ダウンロード"):
        """音声ダウンロードボタンの作成"""
        try:
            st.download_button(
                label=label,
                data=audio_data,
                file_name=filename,
                mime="audio/mp3",
                help=f"{filename}をダウンロードします"
            )
        except Exception as e:
            st.error(f"音声ダウンロードボタン作成エラー: {e}")
            logger.error(f"Audio download button error: {e}")

# ==================================================
# InfoPanelManager拡張（音声用）
# ==================================================
class InfoPanelManager(BaseInfoPanelManager):
    """InfoPanelManager拡張（音声API用）"""

    @staticmethod
    def show_audio_model_info(selected_model: str):
        with st.sidebar.expander("🎵 音声モデル情報", expanded=False):
            if selected_model.startswith("tts-") or selected_model.startswith("gpt-4o-mini-tts"):
                st.info("🎤 Text-to-Speech モデル")
                model_info = {
                    "tts-1": "速度最適化モデル",
                    "tts-1-hd": "高品質モデル",
                    "gpt-4o-mini-tts": "GPT-4o搭載TTS"
                }
                st.write(f"**特徴**: {model_info.get(selected_model, '不明')}")
                st.write("**出力**: MP3")
                st.write("**最大文字数**: 4,096文字")
            else:
                st.info("🎧 Speech-to-Text モデル")
                model_info = {
                    "whisper-1": "標準音声認識",
                    "gpt-4o-transcribe": "高精度音声認識"
                }
                st.write(f"**特徴**: {model_info.get(selected_model, '不明')}")
                st.write("**入力**: MP3, WAV, M4A")
                st.write("**最大ファイルサイズ**: 25MB")

    @staticmethod
    def show_audio_cost_info(selected_model: str):
        with st.sidebar.expander("💰 音声API料金", expanded=False):
            if "tts" in selected_model:
                st.write("**TTS料金 (1000文字あたり)**")
                tts_pricing = {"tts-1": "$0.015", "tts-1-hd": "$0.030", "gpt-4o-mini-tts": "$0.025"}
                current_price = tts_pricing.get(selected_model, "不明")
                st.write(f"- {selected_model}: {current_price}")
                char_count = st.number_input("文字数", min_value=1, value=100, step=10, key="tts_char_count")
                if selected_model in tts_pricing:
                    price = float(tts_pricing[selected_model].replace("$", ""))
                    cost = (char_count / 1000) * price
                    st.write(f"**推定コスト**: ${cost:.6f}")
            else:
                st.write("**STT料金 (分あたり)**")
                st.write("- whisper-1: $0.006")
                st.write("- gpt-4o-transcribe: $0.010")
                duration_minutes = st.number_input("音声時間（分）", min_value=0.1, value=1.0, step=0.1, key="stt_duration")
                stt_pricing = {"whisper-1": 0.006, "gpt-4o-transcribe": 0.010}
                if selected_model in stt_pricing:
                    cost = duration_minutes * stt_pricing[selected_model]
                    st.write(f"**推定コスト**: ${cost:.6f}")

# ==================================================
# 基底クラス（統一化版）
# ==================================================
class BaseDemo(ABC):
    """デモ機能の基底クラス（音声用統一化版）"""

    def __init__(self, demo_name: str):
        self.demo_name = demo_name
        self.config = ConfigManager("config.yml")
        try:
            self.client = OpenAIClient()
            self.openai_client = OpenAI()
            self.async_client = AsyncOpenAI()
        except Exception as e:
            st.error(f"OpenAIクライアントの初期化に失敗しました: {e}")
            st.stop()

        self.safe_key = sanitize_key(demo_name)
        self.message_manager = MessageManagerUI(f"messages_{self.safe_key}")
        self.model = None

        SessionStateManager.init_session_state()
        self._initialize_session_state()

    def _initialize_session_state(self):
        session_key = f"demo_state_{self.safe_key}"
        if session_key not in st.session_state:
            st.session_state[session_key] = {
                'initialized': True,
                'model': self.config.get("models.audio_default", "tts-1"),
                'execution_count': 0,
                'last_audio_file': None
            }

    def get_model(self) -> str:
        return st.session_state.get(f"model_{self.safe_key}", config.get("models.audio_default", "tts-1"))

    def initialize(self):
        self.model = setup_common_ui(self.demo_name)
        setup_sidebar_panels(self.model)

    def handle_error(self, e: Exception):
        lang = config.get("i18n.default_language", "ja")
        error_msg = config.get(f"error_messages.{lang}.general_error", "エラーが発生しました")
        st.error(f"{error_msg}: {str(e)}")
        if config.get("experimental.debug_mode", False):
            with st.expander("🔧 詳細エラー情報", expanded=False):
                st.exception(e)

    @error_handler_ui
    @timer_ui
    def safe_audio_api_call(self, api_func: callable, *args, **kwargs):
        max_retries = config.get("api.max_retries", 3)
        delay = config.get("api.retry_delay", 1)
        for attempt in range(max_retries):
            try:
                return api_func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"音声API呼び出し失敗 (試行 {attempt + 1}/{max_retries}): {e}")
                time.sleep(delay)
                delay *= 2 + random.random()

    @abstractmethod
    def run(self):
        pass

# ==================================================
# Text to Speech デモ（統一化版）
# ==================================================
class TextToSpeechDemo(BaseDemo):
    """Text to Speech API のデモ（統一化版）"""

    @error_handler_ui
    @timer_ui
    def run(self):
        self.initialize()

        st.write("## Text-to-Speech デモ")
        st.write("テキストから音声を生成します。")

        # 入力エリア
        st.subheader("📤 入力")
        
        # テキスト入力
        text_input = st.text_area(
            "音声化するテキストを入力してください：",
            value="こんにちは、OpenAI Text-to-Speech APIのデモンストレーションです。",
            height=100,
            max_chars=4096,
            key=f"tts_text_{self.safe_key}"
        )
        
        # 音声設定
        col1, col2, col3 = st.columns(3)
        with col1:
            voice = UIHelper.select_voice(f"voice_{self.safe_key}")
        with col2:
            speed = st.slider(
                "速度",
                min_value=0.25,
                max_value=4.0,
                value=1.0,
                step=0.25,
                key=f"speed_{self.safe_key}"
            )
        with col3:
            response_format = st.selectbox(
                "出力形式",
                ["mp3", "opus", "aac", "flac"],
                key=f"format_{self.safe_key}"
            )
        
        # 生成ボタン
        if st.button("🎵 音声を生成", key=f"generate_{self.safe_key}"):
            if text_input:
                self._generate_speech(text_input, voice, speed, response_format)
    
    def _generate_speech(self, text: str, voice: str, speed: float, response_format: str):
        """音声生成の実行"""
        try:
            # 実行時間の計測開始
            start_time = time.time()
            
            # セッション状態に保存
            st.session_state[f"tts_text_{self.safe_key}"] = text
            st.session_state[f"tts_voice_{self.safe_key}"] = voice
            
            with st.spinner("音声を生成中..."):
                response = self.openai_client.audio.speech.create(
                    model=self.model,
                    voice=voice,
                    input=text,
                    speed=speed,
                    response_format=response_format
                )
            
            # 実行時間の計算
            generation_time = time.time() - start_time
            
            # 音声データを取得
            audio_data = response.content
            
            st.success("音声を生成しました")
            st.subheader("🎵 生成結果")
            
            # メインコンテンツと右ペイン
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # 音声プレイヤー
                st.audio(audio_data, format=f"audio/{response_format}")
                
                # ダウンロードボタン
                filename = f"speech_{int(time.time())}.{response_format}"
                UIHelper.create_audio_download_button(
                    audio_data, 
                    filename,
                    "📥 音声をダウンロード"
                )
                
                # 生成テキストの表示
                with st.expander("生成したテキスト"):
                    st.write(text)
                
            with col2:
                # 情報パネル
                st.write("**📊 生成情報**")
                
                # モデル情報
                st.metric("使用モデル", self.model.upper())
                
                # 生成時間
                st.metric("生成時間", f"{generation_time:.2f}秒")
                
                # 音声設定
                st.write("**🎵 音声設定**")
                st.write(f"Voice: {voice}")
                st.write(f"速度: {speed}x")
                st.write(f"形式: {response_format}")
                
                # テキスト情報
                st.write("**📝 テキスト情報**")
                st.metric("文字数", len(text))
                
                # ファイルサイズ
                file_size = len(audio_data) / 1024  # KB単位
                st.metric("ファイルサイズ", f"{file_size:.1f} KB")
                
                # コスト推定
                st.write("**💰 コスト推定**")
                tts_pricing = {
                    "tts-1": 0.015,
                    "tts-1-hd": 0.030,
                    "gpt-4o-mini-tts": 0.025
                }
                if self.model in tts_pricing:
                    cost = (len(text) / 1000) * tts_pricing[self.model]
                    st.write(f"${cost:.6f}")
            
        except Exception as e:
            st.error(f"音声生成エラー: {e}")
            if config.get("experimental.debug_mode", False):
                st.exception(e)


# ==================================================
# デモマネージャー（統一化版）
# ==================================================
class AudioDemoManager:
    """音声デモの管理クラス（統一化版）"""

    def __init__(self):
        self.config = ConfigManager("config.yml")
        self.demos = self._initialize_demos()

    def _initialize_demos(self) -> Dict[str, BaseDemo]:
        return {
            "Text to Speech": TextToSpeechDemo("Text to Speech"),
        }

    @error_handler_ui
    @timer_ui
    def run(self):
        try:
            SessionStateManager.init_session_state()
            demo_name = st.sidebar.radio("[a04_audio_speeches.py] Audio Demo", list(self.demos.keys()), key="audio_demo_selection")

            if "current_audio_demo" not in st.session_state:
                st.session_state.current_audio_demo = demo_name
            elif st.session_state.current_audio_demo != demo_name:
                st.session_state.current_audio_demo = demo_name

            demo = self.demos.get(demo_name)
            if demo:
                demo.run()
            else:
                st.error(f"デモ '{demo_name}' が見つかりません")

            self._display_footer()
        except Exception as e:
            st.error(f"アプリケーションの実行中にエラーが発生しました: {str(e)}")
            logger.error(f"Audio application execution error: {e}")
            if config.get("experimental.debug_mode", False):
                with st.expander("🔧 詳細エラー情報", expanded=False):
                    st.exception(e)

    def _display_footer(self):
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🎵 Audio API 情報")
        with st.sidebar.expander("📁 ファイル情報"):
            audio_files = list(DATA_DIR.glob("*.mp3")) + list(DATA_DIR.glob("*.wav"))
            txt_files = list(DATA_DIR.glob("*.txt"))
            st.write(f"**データディレクトリ**: {DATA_DIR}")
            st.write(f"**音声ファイル数**: {len(audio_files)}")
            st.write(f"**テキストファイル数**: {len(txt_files)}")

        with st.sidebar.expander("現在の設定"):
            safe_streamlit_json({
                "data_directory": str(DATA_DIR),
                "audio_models": config.get("models.categories.audio"),
                "supported_formats": config.get("audio.supported_formats"),
                "debug_mode": config.get("experimental.debug_mode"),
            })

        st.sidebar.markdown("### バージョン")
        st.sidebar.markdown("- OpenAI Audio & Speech Demo v3.1 (統一化版)")
        st.sidebar.markdown("- Streamlit " + st.__version__)
        st.sidebar.markdown("### リンク")
        st.sidebar.markdown("[OpenAI Audio API](https://platform.openai.com/docs/guides/speech-to-text)")
        st.sidebar.markdown("[Realtime API](https://platform.openai.com/docs/guides/realtime)")

# ==================================================
# メイン関数（統一化版）
# ==================================================
def main():
    try:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        if not os.getenv("OPENAI_API_KEY"):
            st.error("環境変数 OPENAI_API_KEY が設定されていません。")
            st.info("export OPENAI_API_KEY='your-api-key' を実行してください。")
            st.stop()

        SessionStateManager.init_session_state()
        manager = AudioDemoManager()
        manager.run()
    except Exception as e:
        st.error(f"アプリケーションの起動に失敗しました: {str(e)}")
        logger.error(f"Audio application startup error: {e}")
        if config.get("experimental.debug_mode", False):
            with st.expander("🔧 詳細エラー情報", expanded=False):
                st.exception(e)

if __name__ == "__main__":
    main()

# streamlit run a04_audio_speeches.py --server.port=8504
