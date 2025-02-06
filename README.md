# Habit tracker

## Build

```bash
# Detener y eliminar contenedores previos
docker-compose down -v

docker build --no-cache -t dvillaj/habit-tracker:latest .  && docker-compose up 
```

## External shell

```
docker exec -it habit-tracker-web-1 /bin/sh
```