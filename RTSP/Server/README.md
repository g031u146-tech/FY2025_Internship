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
        > pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
        ```
* YOLOインストール  
    ``` bash
    > pip install ultralytics
    ```
