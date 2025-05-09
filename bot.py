import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime

# Cargar variables de entorno
load_dotenv()

# Diccionario de traducciones para acciones de auditoría
AUDIT_ACTIONS = {
    'member_update': '👤 Actualización de Miembro',
    'member_role_update': '🎭 Cambio de Roles',
    'member_disconnect': '🔌 Desconexión de Usuario',
    'member_move': '🔄 Movimiento de Canal',
    'member_mute': '🔇 Silenciado',
    'member_deafen': '🎧 Ensordecido',
    'member_ban_add': '🔨 Baneo',
    'member_ban_remove': '✅ Desbaneo',
    'member_kick': '👢 Expulsión',
    'channel_create': '📝 Canal Creado',
    'channel_delete': '🗑️ Canal Eliminado',
    'channel_update': '📝 Canal Actualizado',
    'role_create': '⭐ Rol Creado',
    'role_delete': '💫 Rol Eliminado',
    'role_update': '🌟 Rol Actualizado',
    'message_delete': '🗑️ Mensaje Eliminado',
    'message_bulk_delete': '📚 Mensajes Eliminados',
    'message_pin': '📌 Mensaje Fijado',
    'message_unpin': '📍 Mensaje Desfijado',
    'invite_create': '📨 Invitación Creada',
    'invite_delete': '🚫 Invitación Eliminada',
    'webhook_create': '🎣 Webhook Creado',
    'webhook_update': '🔄 Webhook Actualizado',
    'webhook_delete': '❌ Webhook Eliminado',
    'emoji_create': '😀 Emoji Creado',
    'emoji_delete': '😶 Emoji Eliminado',
    'emoji_update': '😄 Emoji Actualizado',
}

# Diccionario de traducción para los cambios principales
CAMBIOS_TRAD = {
    'deaf': '🎧 Ensordecido',
    'mute': '🔇 Silenciado',
    'ban': '🔨 Baneado',
    'nick': '📝 Apodo',
    'roles': '🎭 Roles',
    'name': '📝 Nombre',
    'channel': '📺 Canal',
    'topic': '📝 Tema',
    'nsfw': '🔞 NSFW',
    'user_limit': '👥 Límite de usuarios',
    'bitrate': '🎵 Bitrate',
    'color': '🎨 Color',
    'hoist': '📌 Separador',
    'mentionable': '📢 Mencionable',
    'permissions': '🔑 Permisos',
}

def formatea_valor(valor):
    if isinstance(valor, bool):
        return 'Sí' if valor else 'No'
    if valor is None:
        return 'Ninguno'
    return str(valor)

# Configuración del bot con todos los intents necesarios
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('------')
    print('Intents activados:')
    print(f'- Message Content: {intents.message_content}')
    print(f'- Guilds: {intents.guilds}')
    print(f'- Members: {intents.members}')
    print(f'- Guild Messages: {intents.guild_messages}')

@bot.event
async def on_audit_log_entry_create(entry):
    try:
        channel_id = int(os.getenv('LOG_CHANNEL_ID'))
        channel = bot.get_channel(channel_id)
        
        if channel:
            embed = discord.Embed(
                title="📋 Registro de Auditoría",
                color=discord.Color.blurple(),
                timestamp=datetime.datetime.now(datetime.UTC)
            )
            # Avatar y nombre del usuario que realizó la acción
            if entry.user and hasattr(entry.user, 'avatar') and entry.user.avatar:
                embed.set_author(name=f"{entry.user.name}", icon_url=entry.user.avatar.url)
            elif entry.user:
                embed.set_author(name=f"{entry.user.name}")
            # Miniatura temática
            # embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1828/1828919.png")
            # Acción
            action_name = AUDIT_ACTIONS.get(entry.action.name.lower(), f'⚡ {entry.action.name}')
            embed.add_field(name="Acción", value=action_name, inline=True)
            embed.add_field(name="👤 Usuario", value=entry.user.name if entry.user else "Desconocido", inline=True)
            if entry.target:
                embed.add_field(name="🎯 Objetivo", value=str(entry.target), inline=True)
            if entry.reason:
                embed.add_field(name="📝 Razón", value=entry.reason, inline=True)
            # Separador visual
            embed.add_field(name='', value='━━━━━━━━━━━━━━━━━━━━━━', inline=False)
            # Cambios
            if hasattr(entry, 'before') and hasattr(entry, 'after'):
                changes_text = ""
                for attr in dir(entry.before):
                    if not attr.startswith('_'):
                        before_value = getattr(entry.before, attr, None)
                        after_value = getattr(entry.after, attr, None)
                        if before_value != after_value:
                            nombre = CAMBIOS_TRAD.get(attr, f'**{attr}**')
                            changes_text += f"{nombre}: {formatea_valor(before_value)} → {formatea_valor(after_value)}\n"
                if changes_text:
                    embed.add_field(name="📊 Cambios", value=changes_text, inline=False)
            await channel.send(embed=embed)
    except Exception as e:
        print(f"Error al procesar el log de auditoría: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        if hasattr(entry, 'before'):
            print(f"Atributos de before: {dir(entry.before)}")
        if hasattr(entry, 'after'):
            print(f"Atributos de after: {dir(entry.after)}")

@bot.command()
async def ping(ctx):
    await ctx.send('¡Pong! 🏓')

token = os.getenv('DISCORD_TOKEN')
if not token:
    print("Error: No se encontró el token del bot en el archivo .env")
else:
    bot.run(token) 