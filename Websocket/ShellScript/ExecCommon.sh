#!/usr/bin/bash
createVenv(){
  venvDir='../venv'
  # 仮想環境格納用のディレクトリがあるかチェック
  if [ ! -d $venvDir ]; then
    mkdir $venvDir
  fi

  venvPath="${venvDir}/Websocket"
  isCreateVenv=1
  # 実行用の仮想環境があるかチェック
  if [ ! -d $venvPath ]; then
      python3 -m venv $venvPath
      isCreateVenv=0
  fi

  echo $venvPath
  exit $isCreateVenv
}

pipInstall(){
  # 仮想環境の作成を行った場合、ライブラリをインストール
  requirementsPath='./Requirements'
  pip install -r "${requirementsPath}/01_requirements.txt"
  pip install -r "${requirementsPath}/02_requirements.txt"
}