# FY2025_Internship
このリポジトリは、2025年度インターンシップ型授業で使用する。  
開発環境については、UbuntuおよびRaspberry Pi OSのLinux環境をベースに記載する。  

## 1. Docker環境構築

* インストール

    ``` bash
    > curl -fsSL https://get.docker.com -o get-docker.sh
    > sudo sh get-docker.sh
    ```

* ユーザ権限で実行できるように設定

    ``` bash
    > sudo gpasswd -a $USER docker
    > newgrp docker
    ```

上記のコマンドをすべて実行後、再起動を行う。

## 2.RTSP

### 2.1. クライアント環境構築

#### 2.1.1. RTSPサーバ構築

* 設定関連
    **/etc/modules** に以下の内容を追記し、再起動を行う

    ``` conf
    bcm2835-v4l2
    ```

* 必要モジュールのインストール

    ``` bash
    > sudo apt -y install git
    > sudo apt -y install cmake
    > sudo apt -y install liblivemedia-dev
      ※ Ubuntuの場合、3つ目のモジュールがないのでインストール不要
    ```

* コンパイル及びインストール

    ``` bash
    > git clone https://github.com/mpromonet/h264_v4l2_rtspserver.git
    > cd h264_v4l2_rtspserver
    > sudo cmake .
    > sudo make install
    ```

インストール後、再起動を行う。

> [!NOTE]
> 以下のコマンドを実行することで、RTSPサーバを起動することができる  
> オプション指定がない場合、**rtps://<URL・IPアドレス>:8554/unicast**でアクセスできる
>
>``` bash
> > sudo systemctl start v4l2rtspserver
> ```
>
> or
>
> ``` bash
> > sudo v4l2rtspserver
> ```
>
> また、下記のコマンドにより、自動起動が可能となる
>
> ```bash
> > sudo systemctl enable v4l2rtspserver.service
> ```

### 2.2. サーバ環境構築

#### 2.2.1. ffmpeg

* ffmpegインストール

    ``` bash
    > sudo apt -y install ffmpeg
    ```

#### 2.2.2. nginx

* nginxインストール

    ``` bash
    > sudo apt -y install nginx
    ```

* **/etc/nginx/conf.d/** に以下の内容のconfファイルを作成

    ``` bash
    > sudo vi /etc/nginx/conf.d/99-config.conf
    ```

    ``` conf
    server {  
        location / {  
            root /var/www/html;  
       }
    }
    types {
       application/vnd.apple.mpegurl m3u8;
       video/mp2t ts;
        text/html html;
    }
    ```

## 3. Python

### 3.1. Pythonのバージョン指定

* 必要なプログラムをインストール

   ``` bash
   > sudo apt update
   > sudo apt install software-properties-common
   ```

* Repositoryを登録

   ``` bash
   > sudo add-apt-repository ppa:deadsnakes/ppa
   ```

* 指定バージョンをインストール（20250128現在の最新は、3.13）

   ``` bash
   > sudo apt install python3.xx
   ```

* 指定バージョンを使用

   ``` bash
   > python3.xx --version
   ```

> [!NOTE]
> 以下の通りにコマンド実行を行うと、デフォルトバージョンのPythonで実行される。
>
> ``` bash
> > python3 --version
> ```

### 3.2. 仮想環境構築

Pythonは、仮想環境を使用することを推奨している。  
本プロジェクトでは、venvという仮想環境を使用する。  
なお、ここでのPythonのバージョンは3.5以降のものとする。

* 仮想環境の作成

   ``` bash
   > mkdir 仮想環境構築ディレクトリ
   > cd 仮想環境構築ディレクトリ
   > python3 -m venv 仮想環境名
   ```

* 仮想環境の有効化

   ``` bash
   > cd 仮想環境構築ディレクトリ
   > source 仮想環境名/bin/activate
   ```

* 仮想環境の無効化

   ``` bash
   > deactive
   ```

> [!NOTE]
> 仮想環境の作成コマンドを実行した際、エラーが発生した場合は以下のライブラリをインストール
>
> ``` bash
> > sudo apt install python3-venv
> ```

### 3.3. pip関係

pipは、Pythonのパッケージ管理システムである  
下記の内容については、必要に応じて実行すること

* pipインストール  

    ``` bash
    > sudo apt -y install python3-pip
    ```

* pip設定(PEP 686対策)  

    ``` bash
    > mkdir ~/.pip  
    > vi ~/.pip/pip.conf
    ```

    ``` conf
    > [global]
    > break-system-packages = true
    ```

* パッケージ一括インストール
パッケージを一括でインストールを行うファイル(ex. requirements.txt )が用意されている場合は、以下のコマンドを実行するとまとめてパッケージインストールできる

   ``` bash
   > pip install -r requirements.txt
   ```

## 4. node.js

### 4.1. node.jsのインストール

Ubuntuのパッケージソフトのnode.JSおよびnode.jsのパッケージ管理システムのnpmのバージョンが最新ではないため、以下のコマンドでインストールを行う。

* 現行バージョンをインストール

    ``` bash
    > sudo apt install -y nodejs npm
    ```

* nをインストール（バージョン管理）

    ``` bash
    > sudo npm install n -g
    ```

* 最新のnode.jsとnpmをインストール

    ``` bash
    > sudo n stable
    ```

* 最初にインストールしたものをアンインストール

    ``` bash
    > sudo apt purge -y nodejs npm
    > sudo apt autoremove -y
    ```

### 4.2. Angularのインストール

   ``` bash
   > sudo npm install -g @angular/cli
   ```

### 4.3. NestJSのインストール

   ``` bash
   > sudo npm install -g @nestjs/cli
   ```
