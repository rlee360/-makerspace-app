curl -X POST \
     -F id=$1 \
     -F material_used=120 \
     -F machine='FDM_2' \
     -F operator='henry son' \
     http://localhost:5000/api/request/update