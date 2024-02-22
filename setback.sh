#!/bin/bash
source /Users/hong-gijun/opt/anaconda3/etc/profile.d/conda.sh
conda deactivate

deactivate 2>/dev/null || true

source /Users/hong-gijun/flaskbasic/bin/activate
cd /Users/hong-gijun/Desktop/project2/backend
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run