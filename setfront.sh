#!/bin/bash
source /Users/hong-gijun/opt/anaconda3/etc/profile.d/conda.sh
conda deactivate

deactivate 2>/dev/null || true

source /Users/hong-gijun/flaskbasic/bin/activate
cd /Users/hong-gijun/Desktop/project2/frontend

npm run start

