#!/bin/bash
if [ $# -ne 1 ]; then
    echo "用法: bash export_conda_env.sh <环境名称>"
    echo "示例: bash export_conda_env.sh py310"
    exit 1
fi

ENV_NAME=$1

# 激活conda（适配bash/zsh）
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ${ENV_NAME}

echo "===== 正在导出 conda 环境 ${ENV_NAME} ====="
# 导出yml，移除prefix行
conda env export --no-builds | grep -v "^prefix: " > environment.yml

echo "===== 正在导出 pip 依赖 ====="
pip freeze > pip_requirements.txt

echo "导出完成！生成文件："
echo " - environment.yml"
echo " - pip_requirements.txt"
echo ""
echo "【对方部署命令】"
echo "conda env create -f environment.yml"
echo "conda activate ${ENV_NAME}"
echo "pip install -r pip_requirements.txt"