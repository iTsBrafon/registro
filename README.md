# Bot de Registro de Auditoría de Discord

Este bot monitorea y muestra los registros de auditoría de tu servidor de Discord en un canal específico.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Token de bot de Discord
- Permisos de administrador en el servidor

## Instalación

1. Clona este repositorio o descarga los archivos
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
DISCORD_TOKEN=tu_token_aqui
LOG_CHANNEL_ID=id_del_canal_aqui
```

## Configuración

1. Crea un nuevo bot en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications)
2. Obtén el token del bot y colócalo en el archivo `.env`
3. Habilita los "Privileged Gateway Intents" en la sección de "Bot" del portal de desarrolladores
4. Invita el bot a tu servidor con los permisos necesarios
5. Crea un canal de texto donde se mostrarán los logs
6. Copia el ID del canal y colócalo en el archivo `.env`

## Uso

1. Ejecuta el bot:
```bash
python bot.py
```

2. El bot comenzará a monitorear y mostrar los registros de auditoría en el canal especificado

## Características

- Muestra información detallada sobre cada acción de auditoría
- Incluye el usuario que realizó la acción
- Muestra los cambios realizados
- Formato embebido para mejor visualización
- Timestamps en cada registro #   r e g i s t r o  
 