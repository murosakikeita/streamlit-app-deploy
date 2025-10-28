import os
import streamlit as st
import openai

# --- APIキー設定 ---
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# --- アプリのヘッダー ---
st.title("🏗️ 建設業界専門 LLMアドバイザー")
st.write("""
このアプリでは、建設業に特化した3タイプの専門AIがあなたの質問に答えます。  
AIが実際の専門家のように、役割に応じて異なる視点で回答します。
""")

# --- 専門家タイプ選択 ---
expert = st.radio(
    "👷‍♂️ 相談したい専門家を選択してください：",
    ("施工管理技士", "建築設計士", "建設経営コンサルタント")
)

# --- ユーザー入力欄 ---
user_input = st.text_area("💬 質問を入力してください（例：現場の安全管理を改善したい など）")

# --- 回答生成関数 ---
def get_openai_response(role, text):
    """OpenAI APIから専門家の役割に応じた回答を取得する"""
    if not api_key:
        return "⚠️ APIキーが設定されていません。"

    # 役割に応じたシステムプロンプト
    if role == "施工管理技士":
        system_prompt = (
            "あなたは経験豊富な施工管理技士です。"
            "現場の安全管理・品質・コストに関する課題に、実務的かつ具体的なアドバイスをしてください。"
        )
    elif role == "建築設計士":
        system_prompt = (
            "あなたは優秀な建築設計士です。"
            "構造・法規・環境設計など、技術的で創造的な助言を行ってください。"
        )
    else:
        system_prompt = (
            "あなたは建設業経営専門の経営コンサルタントです。"
            "人材不足・原価管理・入札戦略・DX化など経営面からアドバイスをしてください。"
        )

    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
        )
        return completion.choices[0].message.content
    except Exceptio
