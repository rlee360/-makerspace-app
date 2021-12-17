curl -X POST \
     -F type='filament' \
     -F material='PLA' \
     -F color='black' \
     -F brand='Inland' \
     -F grams_remaining=300 \
     -F link='https://www.microcenter.com/product/632388/inland-175mm-black-pla-pro-3d-printer-filament-1kg-spool-(22-lbs)' \
     -F valid_machines='FDM 1, FDM 2, FDM 3' \
     -F price=18.99 \
     http://localhost:5000/api/material/add