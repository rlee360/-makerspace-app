# Docker
Only the database and backend are containerized as of now.

## Prerequisite 
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

## Usage
### Spin up database and backend
```bash
docker-compose up -d
```
You will now be able to access the backend through localhost:5000 and the database through localhost:27017.

### Spin down database and backend
```bash
docker-compose down
```

### Enter backend
```bash
docker exec -it backend bash
```

### View Flask logs 
```bash
docker logs backend
```
