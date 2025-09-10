"""
Streamlit UIコンポーネントのラッパークラス
テスト可能な形に分離
"""
import streamlit as st
from typing import Any, List, Tuple, Optional
from unittest.mock import MagicMock


class UIWrapper:
    """UIコンポーネントのラッパー"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.output_buffer: List[str] = []
        self.error_buffer: List[str] = []
        self.column_config: List[Tuple[int, ...]] = []
    
    def write(self, *args: Any, **kwargs: Any) -> None:
        """st.writeのラッパー"""
        if self.test_mode:
            # テストモードでは出力をバッファに保存
            self.output_buffer.append(str(args[0]) if args else "")
        else:
            st.write(*args, **kwargs)
    
    def error(self, message: str) -> None:
        """st.errorのラッパー"""
        if self.test_mode:
            self.error_buffer.append(message)
        else:
            st.error(message)
    
    def columns(self, spec: List[int]) -> List[Any]:
        """st.columnsのラッパー"""
        if self.test_mode:
            # テストモードではモックオブジェクトを返す
            self.column_config.append(tuple(spec))
            return [MagicMock() for _ in spec]
        else:
            return st.columns(spec)
    
    def container(self) -> Any:
        """st.containerのラッパー"""
        if self.test_mode:
            return MagicMock()
        else:
            return st.container()
    
    def button(self, label: str, key: Optional[str] = None) -> bool:
        """st.buttonのラッパー"""
        if self.test_mode:
            # テストモードでは常にTrueを返す（設定可能）
            return True
        else:
            return st.button(label, key=key)
    
    def text_area(self, label: str, value: str = "", key: Optional[str] = None) -> str:
        """st.text_areaのラッパー"""
        if self.test_mode:
            # テストモードではデフォルト値を返す
            return value or "Test input"
        else:
            return st.text_area(label, value=value, key=key)
    
    # テスト用ヘルパーメソッド
    def get_output(self) -> List[str]:
        """出力バッファの取得（テスト用）"""
        return self.output_buffer
    
    def get_errors(self) -> List[str]:
        """エラーバッファの取得（テスト用）"""
        return self.error_buffer
    
    def clear_buffers(self) -> None:
        """バッファのクリア（テスト用）"""
        self.output_buffer.clear()
        self.error_buffer.clear()


# 使用例：リファクタリング後のコード
def setup_common_ui_refactored(demo_name: str, ui: Optional[UIWrapper] = None) -> str:
    """テスト可能な共通UI設定"""
    ui = ui or UIWrapper()
    
    # ヘッダー表示
    ui.write(f"# {demo_name}")
    
    # モデル選択（簡略化）
    model = "gpt-4o-mini"  # UIHelperの代わりに直接設定
    ui.write("選択したモデル:", model)
    
    return model


class TextResponseDemoRefactored:
    """テスト可能なTextResponseDemo"""
    
    def __init__(self, ui: Optional[UIWrapper] = None, 
                 session: Optional['SessionStateWrapper'] = None):
        self.ui = ui or UIWrapper()
        # SessionStateWrapperをインポート
        from test_solutions.session_state_wrapper import SessionStateWrapper
        self.session = session or SessionStateWrapper()
        
    def run(self):
        """デモの実行"""
        self.ui.write("サブアプリ：：TextResponseDemo")
        
        # カラムレイアウト
        col1, col2 = self.ui.columns([3, 1])
        
        with col1:
            # テキスト入力
            prompt = self.ui.text_area("プロンプトを入力してください", 
                                       value="こんにちは、今日の天気はどうですか？")
            
            if self.ui.button("送信"):
                self._process_response(prompt)
    
    def _process_response(self, prompt: str):
        """レスポンス処理"""
        try:
            # 実際の処理（簡略化）
            response = f"入力されたプロンプト: {prompt}"
            self.ui.write(response)
        except Exception as e:
            self.ui.error(f"エラーが発生しました: {e}")