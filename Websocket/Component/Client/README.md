# Websocketクライアント環境構築

WebSocketクライアントで使用するパッケージは、一括でインストールを行うファイルがあるので、以下のコマンドを実行すること
なお、個々でインストールが行えるようにインストールコマンドについても記載を行う
``` bash
pip install -r requirements.txt
```
> [!NOTE]
> プログラム実行時、openCV関連ライブラリに関するエラーが発生が発生した場合、以下のライブラリをインストール
> ``` bash
> > sudo apt -y install libopencv-dev
> ```

* openCVインストール  
    ``` bash
    > pip install opencv-python
    ```
* Websocketインストール  
    ``` bash
    > pip install websockets
    ```
