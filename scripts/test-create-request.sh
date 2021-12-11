curl -X POST \
     -F files=@README.md \
     -F email='test1@cooper.edu, test2@cooper.edu' \
     -F name='henry son' \
     -F material='material1' \
     -F notes='here are some notes' \
     -F shells='2' \
     -F infill='3' \
     -F top_bottom='4' \
     -F filename='part.stl' \
     http://localhost:5000/request/create