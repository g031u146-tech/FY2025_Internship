# Websocketサーバ環境構築
  
WebSocketサーバで使用するパッケージは、一括でインストールを行うファイルがあるので、以下のコマンドを実行すること  
なお、個々でインストールが行えるようにインストールコマンドについても記載を行う
``` bash
> pip install -r 01_requirements.txt
> pip install -r 02_requirements.txt
```

> [!NOTE]
> プログラム実行時、「ImportError: libGL.so.1: cannot open shared object file」が発生した場合、以下のライブラリをインストール
>
> ``` bash
> > apt -y install libopencv-dev
> ```
* openCVインストール  
    ``` bash
    > pip install opencv-python
    ```
* Websocket Serverインストール  
    ``` bash
    > pip install websocket-server
    ```
> [!CAUTION]
> 実行するとエラーが発生するので、該当箇所を以下の通りに変更
> lib/python3.12/site-packages/websocket_server/websocket_server.py: 341行目
> ``` python
> opcode_handler(self, message_bytes.decode('utf8'))
> ```
> ↓
> ``` python
> try:
>     opcode_handler(self, message_bytes.decode('utf8'))
> except:
>     pass
> ```
* pymongoインストール  
    ``` bash
    > pip install pymongo
    ```
* pytorchインストール  
    * CPU   
        ``` bash  
        > pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu  
        ```
     * GPU  
        ``` bash  
        > pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        ```
* YOLOインストール  
    ``` bash
    > pip install ultralytics
    ```
