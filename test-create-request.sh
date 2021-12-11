curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{
  "email": "test1@cooper.edu, test2@cooper.edu",
  "name": "",
  "material": "Material1",
  "notes": "asdfasdfasdf",
  "shells": "2",
  "infill": "4",
  "top_bottom": "7",
  "filename": "here.stl"
}' \
     http://localhost:5000/request/create