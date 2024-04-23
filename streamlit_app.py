import subprocess
import streamlit as st
import openai
import asyncio

# 話者とIDの対応辞書
speakers = {
    "四国めたん": {
        "ノーマル": 2,
        "あまあま": 0,
        "ツンツン": 6,
        "セクシー": 4
    },
    "ずんだもん": {
        "ノーマル": 3,
        "あまあま": 1,
        "ツンツン": 7,
        "セクシー": 5
    },
    "春日部つむぎ": {
        "ノーマル": 8
    },
    "雨晴はう": {
        "ノーマル": 10
    },
    "波音リツ": {
        "ノーマル": 9
    },
    "玄野武宏": {
        "ノーマル": 11
    },
    "白上虎太郎": {
        "ノーマル": 12
    },
    "青山龍星": {
        "ノーマル": 13
    },
    "冥鳴ひまり": {
        "ノーマル": 14
    },
    "九州そら": {
        "ノーマル": 16,
        "あまあま": 15,
        "ツンツン": 18,
        "セクシー": 17,
        "ささやき": 19
    }
}


def get_chat_ai_answer(text_input):
    # ChatGPT APIのトークン読み込み/GPT-3.5 TurboのAPIキーを設定
    openai.api_key = st.secrets["chatgpt_api_key"]
    # ChatGPTによるテキスト生成
    messages = [{"role": "user", "content": text_input + "という大喜利に答えて。10文字以上50文字以内で答えよ"}]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response_data = completion["choices"][0]["message"]["content"].strip()
    # テキストをファイルに書き出す
    with open("text.txt", "w", encoding="utf-8") as f:
        f.write(response_data)
    return response_data


def generate_image(prompt):
    # 画像生成のAPIを呼び出して画像を生成する
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]
    return image_url


async def get_audio_query(speaker_id):
    # audio_queryコマンドを実行
    audio_query_cmd = f'curl -s -X POST "localhost:50021/audio_query?speaker={speaker_id}" --get --data-urlencode ' \
                      f'text@text.txt > query.json '
    subprocess.run(audio_query_cmd, shell=True, check=True)

    # synthesisコマンドを実行
    synthesis_cmd = f'curl -s -H "Content-Type: application/json" -X POST -d @query.json ' \
                    f'"localhost:50021/synthesis?speaker={speaker_id}" '
    response = subprocess.run(synthesis_cmd, shell=True, check=True, capture_output=True)

    # 音声をファイルに保存する
    with open("audio.wav", "wb") as file:
        file.write(response.stdout)


def main():
    # Streamlitアプリのタイトルとテキスト入力
    st.title("大喜利のお題にAIが答えてくれるアプリ")
    text_input = st.text_area("大喜利のお題入力欄", value="", key="text_input",
                              placeholder="ex) 東京大学で3ヶ月に1度しか提供されない学食のメニューとは")

    # 話者を選択するドロップダウンメニュー
    selected_speaker = st.selectbox("お題に答えてくれる人", list(speakers.keys()))

    if st.button("AIが回答して、イメージ画像が出るよ", key="generate_button"):  # keyを追加
        response_data = get_chat_ai_answer(text_input)

        # 画像を生成する
        st.spinner("画像生成中...")
        image_url = generate_image(response_data + "という返答のイメージ画像")
        st.success("画像生成が完了しました！")
        st.image(image_url, caption="Generated Image", use_column_width=True)

        # 非同期処理を実行する
        st.spinner("音声生成中...")
        speaker_id = speakers[selected_speaker]["ノーマル"]
        asyncio.run(get_audio_query(speaker_id))
        st.success("音声生成が完了しました！")
        st.audio("audio.wav", format="audio/wav")

        st.write("Response Data:", response_data)  # 追加


if __name__ == "__main__":
    main()
