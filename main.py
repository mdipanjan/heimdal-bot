import os
from telegram.ext import Updater, CommandHandler
import subprocess
TOKEN = os.environ['BOT_TOKEN']


def start(update, context):
    update.message.reply_text("""Hello! I am a bot that can monitor the CPU usage of your Linux VPS. 
    /cpu command to see the current CPU usage.
    /processes command to see the current running processes.
    """)


def cpu(update, context):
    usage = os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read()
    update.message.reply_text(f'Current CPU usage: {usage}%')


def processes(update, context):
    running_processes = subprocess.check_output(['pgrep', '-f', 'screen'])
    update.message.reply_text(f'Current processes: {running_processes}%')


updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('cpu', cpu))
updater.dispatcher.add_handler(CommandHandler('processes', processes))

updater.start_polling()
updater.idle()
