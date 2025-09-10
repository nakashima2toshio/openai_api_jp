"""
Streamlit session_stateのラッパークラス
テスト可能な形に分離
"""
import streamlit as st
from typing import Any, Dict, Optional


class SessionStateWrapper:
    """セッション状態管理のラッパー"""
    
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self._test_storage: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """値の取得"""
        if self.test_mode:
            return self._test_storage.get(key, default)
        else:
            if hasattr(st, 'session_state'):
                return st.session_state.get(key, default)
            return default
    
    def set(self, key: str, value: Any) -> None:
        """値の設定"""
        if self.test_mode:
            self._test_storage[key] = value
        else:
            if hasattr(st, 'session_state'):
                st.session_state[key] = value
    
    def exists(self, key: str) -> bool:
        """キーの存在確認"""
        if self.test_mode:
            return key in self._test_storage
        else:
            if hasattr(st, 'session_state'):
                return key in st.session_state
            return False
    
    def initialize(self, key: str, initial_value: Dict[str, Any]) -> None:
        """初期化"""
        if not self.exists(key):
            self.set(key, initial_value)


# 使用例：リファクタリング後のBaseDemo
class BaseDemoRefactored:
    """テスト可能なBaseDemoクラス"""
    
    def __init__(self, demo_name: str, session_wrapper: Optional[SessionStateWrapper] = None):
        self.demo_name = demo_name
        self.session = session_wrapper or SessionStateWrapper()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """セッション状態の初期化"""
        session_key = f"demo_state_{self.demo_name}"
        self.session.initialize(session_key, {
            'initialized': True,
            'model': 'gpt-4o-mini',
            'execution_count': 0
        })
    
    def get_execution_count(self) -> int:
        """実行回数の取得"""
        session_key = f"demo_state_{self.demo_name}"
        state = self.session.get(session_key, {})
        return state.get('execution_count', 0)
    
    def increment_execution_count(self) -> None:
        """実行回数の増加"""
        session_key = f"demo_state_{self.demo_name}"
        state = self.session.get(session_key, {})
        state['execution_count'] = state.get('execution_count', 0) + 1
        self.session.set(session_key, state)