----------
このプログラムはChatGPTのAPIを使っているため、forkする際にはSecretなどの情報などをPushしないように気をつけてください。
このプログラムを用いて何らかの損害が発生した場合も自分は責任を取りませんので、ご注意ください。
----------

前提条件は以下です。
* Voicevoxを以下からダウンロードし、起動していること
  * https://voicevox.hiroshiba.jp/
* ChatGPTのAPI_KEYを自分のもので記載する。
  * secrets.toml.sampleをコピーして、secrets.tomlに名前を変更し、自分のAPIキーに変更してください。
    * chatgpt_api_key = "XXXXXXX"
* ライブラリを以下のコマンドでインストール
  ```
  pip install -r requirements.txt
  ```

以下で起動します。
```
streamlit run streamlit_app.py
```

その他
* 簡易的なプログラムということで、streamlitというライブラリを用いてUIを作成しています。
* ライブラリの依存は雑に以下で作成しているので不要なものが入っている可能性もありますので、ご容赦ください。
```
pip3 freeze > requirements.txt
```
