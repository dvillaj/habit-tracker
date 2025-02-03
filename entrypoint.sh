#!/bin/sh
set -e

if [ -n "$PUID" ] && [ -n "$PGID" ]; then
    # Crear grupo si no existe
    if ! getent group "$PGID" >/dev/null; then
        groupadd -g "$PGID" appgroup
    fi

    # Crear usuario si no existe
    if ! id -u "$PUID" >/dev/null 2>&1; then
        useradd -u "$PUID" -g "$PGID" -d /app -s /bin/sh -M appuser
    fi

    # Asegurar permisos en /app
    chown -R "$PUID:$PGID" /app

    # Ejecutar el comando como el usuario
    exec gosu "$PUID:$PGID" "$@"
else
    # Ejecutar como root si no hay PUID/PGID
    exec "$@"
fi