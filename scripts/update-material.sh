curl -X POST \
     -F id=$1 \
     -F color='red' \
     -F grams_remaining=200 \
     -F link='https://www.microcenter.com/product/632388/inland-175mm-red-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)' \
     http://localhost:5000/api/material/update