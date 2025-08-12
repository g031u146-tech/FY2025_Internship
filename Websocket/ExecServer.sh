#!/usr/bin/bash
source ./ShellScript/ExecCommon.sh
# 仮想環境作成
venvPath=$(createVenv)
isExecVenv=$?

# 仮想環境を有効化
source "${venvPath}/bin/activate"

# 仮想環境を作成した場合
if [ $isExecVenv = 0 ]; then
    pipInstall
fi

# 実行
python ./Component/exec_server.py
# 仮想環境を無効化
deactivate
