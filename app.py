import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI APIキーの設定
def set_openai_key():
    """OpenAI APIキーを設定する"""
    try:
        # Streamlit Cloud用のsecrets
        if "OPENAI_API_KEY" in st.secrets:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
            return True
    except:
        pass
    
    # 環境変数から取得
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai.api_key = api_key
        return True
    
    return False

def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家タイプを受け取り、OpenAI APIからの回答を返す関数
    """
    
    # 専門家タイプに応じたシステムメッセージの定義
    system_messages = {
        "医療専門家": """
        あなたは経験豊富な医療専門家です。医学知識を基に、正確で信頼できる医療情報を提供してください。
        ただし、具体的な診断や治療の指示は避け、必要に応じて医療機関への相談を推奨してください。
        専門用語を使用する際は、分かりやすい説明も併記してください。
        """,
        
        "ITエンジニア": """
        あなたは経験豊富なITエンジニアです。プログラミング、システム設計、技術的な問題解決について
        実践的で具体的なアドバイスを提供してください。コードを書く際は、
        可読性が高く、ベストプラクティスに従った例を示してください。
        """,
        
        "経営コンサルタント": """
        あなたは経験豊富な経営コンサルタントです。ビジネス戦略、組織運営、マーケティング、
        財務管理などの経営課題に対して、実践的で戦略的なアドバイスを提供してください。
        データドリブンな視点と具体的なアクションプランを重視してください。
        """,
        
        "教育専門家": """
        あなたは経験豊富な教育専門家です。学習方法、教育手法、カリキュラム設計について
        効果的なアドバイスを提供してください。学習者のレベルや状況に応じた
        個別化された指導方針を重視してください。
        """,
        
        "心理カウンセラー": """
        あなたは経験豊富な心理カウンセラーです。メンタルヘルス、人間関係、
        ストレス管理について共感的で建設的なアドバイスを提供してください。
        傾聴の姿勢を保ち、必要に応じて専門機関への相談を推奨してください。
        """
    }
    
    try:
        # OpenAI APIを呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_messages[expert_type]},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}"

def main():
    # Streamlitページ設定
    st.set_page_config(
        page_title="AI専門家コンサルタント",
        page_icon="🤖",
        layout="wide"
    )
    
    # OpenAI APIキーの設定チェック
    if not set_openai_key():
        st.error("⚠️ OpenAI APIキーが設定されていません。下記の方法で設定してください。")
        with st.expander("🔑 APIキー設定方法"):
            st.markdown("""
            ### 設定方法
            1. [OpenAI公式サイト](https://platform.openai.com/api-keys)でAPIキーを取得
            2. **ローカルで実行する場合**: 
               ```bash
               export OPENAI_API_KEY="your-api-key-here"
               ```
            3. **Streamlit Cloudの場合**: アプリ設定の「Secrets」で設定
            """)
        return
    
    # タイトルと説明
    st.title("🤖 AI専門家コンサルタント")
    
    st.markdown("""
    ## 📖 アプリの概要
    
    このWebアプリは、様々な分野の専門家として振る舞うAIコンサルタントです。
    質問や相談内容に対して、選択した専門分野の知識と視点からアドバイスを提供します。
    
    ## 🚀 操作方法
    
    1. **専門家を選択**: 右側のラジオボタンから相談したい分野の専門家を選択してください
    2. **質問を入力**: 下のテキストエリアに質問や相談内容を入力してください  
    3. **回答を取得**: 「回答を取得」ボタンを押すと、選択した専門家の視点からAIが回答します
    
    ## ⚠️ ご注意
    - このアプリの回答は参考情報として提供されます
    - 重要な決定や専門的な診断については、必ず実際の専門家にご相談ください
    """)
    
    # レイアウト設定
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### 🎯 専門家を選択")
        expert_type = st.radio(
            "相談したい分野の専門家を選択してください：",
            ["医療専門家", "ITエンジニア", "経営コンサルタント", "教育専門家", "心理カウンセラー"],
            index=1  # デフォルトでITエンジニアを選択
        )
        
        # 選択された専門家の説明
        expert_descriptions = {
            "医療専門家": "🏥 医学知識に基づいた健康相談",
            "ITエンジニア": "💻 技術的な問題解決とプログラミング",
            "経営コンサルタント": "📈 ビジネス戦略と経営課題",
            "教育専門家": "📚 学習方法と教育手法",
            "心理カウンセラー": "🧠 メンタルヘルスと人間関係"
        }
        
        st.info(f"**選択中**: {expert_descriptions[expert_type]}")
    
    with col1:
        st.markdown("### 💬 質問・相談内容を入力")
        user_input = st.text_area(
            "質問や相談したい内容を詳しく入力してください：",
            height=150,
            placeholder="例：プロジェクトの進捗管理で困っています。チームメンバーのモチベーション維持と効率的なタスク管理の方法を教えてください。"
        )
        
        # 回答取得ボタン
        if st.button("🚀 回答を取得", type="primary", use_container_width=True):
            if user_input.strip():
                with st.spinner(f"{expert_type}として回答を生成中..."): 
                    response = get_llm_response(user_input, expert_type)
                    
                    st.markdown("### 🤖 AI専門家からの回答")
                    st.markdown(f"**{expert_type}からのアドバイス:**")
                    st.markdown(response)
                    
            else:
                st.warning("⚠️ 質問内容を入力してください。")

if __name__ == "__main__":
    main()