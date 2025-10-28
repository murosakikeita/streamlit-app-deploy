import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- OPENAI_API_KEY の取得（Cloud & ローカル両対応） ---
# Cloud の場合は Secrets、ローカルでは環境変数を利用
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# --- Streamlitアプリ設定 ---
st.title("🏗️ 建設業界専門 LLMアドバイザー")
st.write("""
このアプリでは、建設業に特化した3タイプの専門AIがあなたの質問に答えます。  
左のラジオボタンで専門領域を選び、質問を入力してください。
""")

# --- 専門家の種類を選択 ---
expert = st.radio(
    "相談したい専門家を選択してください：",
    ("施工管理技士", "建築設計士", "建設経営コンサルタント")
)

# --- 入力フォーム ---
user_input = st.text_area("💬 質問を入力してください（例：現場の安全管理を改善したい など）")

# --- LLM応答関数 ---
def get_llm_response(role, text):
    """専門家タイプと質問をもとにLLMから回答を取得"""
    if not api_key:
        return "⚠️ APIキーが設定されていません。"

    # --- 専門家ごとのプロンプト ---
    if role == "施工管理技士":
        system_prompt = (
            "あなたは経験豊富な施工管理技士です。"
            "現場の安全管理・品質・コストに関する課題に、実務的かつ具体的なアドバイスをしてください。"
        )
    elif role == "建築設計士":
        system_prompt = (
            "あなたは優秀な建築設計士です。"
            "設計・構造・法規・環境設計などの観点から、技術的で創造的な助言を行ってください。"
        )
    elif role == "建設経営コンサルタント":
        system_prompt = (
            "あなたは建設業経営専門の経営コンサルタントです。"
            "人材不足・原価管理・入札戦略・DX化など経営面からアドバイスをしてください。"
        )
    else:
        system_prompt = "あなたは建設業界の専門家です。誠実に回答してください。"

    # --- LLM呼び出し ---
    try:
        llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text),
        ]
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"❌ エラーが発生しました: {e}"

# --- ボタン操作 ---
if st.button("回答を表示"):
    if user_input.strip():
        st.markdown("### 💡 回答：")
        st.write(get_llm_response(expert, user_input))
    else:
        st.warning("質問を入力してください。")

# --- フッター ---
st.caption("ver. 2025-10-28 / dotenv除去版（Cloud最適化済）")
