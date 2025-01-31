# Habit tracker

## Build

```bash
# Detener y eliminar contenedores previos
docker-compose down -v

# Reconstruir con los nuevos cambios
docker-compose up --build
```

## External shell

```
docker exec -it habit-tracker-web-1 /bin/sh
```