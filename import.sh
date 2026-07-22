#!/bin/bash
conda env create -f environment.yml
# 获取yml里的环境名，也可以手动修改
ENV_NAME=$(grep '^name:' environment.yml | awk '{print $2}')
conda activate ${ENV_NAME}
pip install -r pip_requirements.txt
echo "环境部署完成！"