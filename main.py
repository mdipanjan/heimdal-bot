
import os
from telegram.ext import Updater, CommandHandler
import subprocess
import psutil
TOKEN = os.environ['BOT_TOKEN']


def start(update, context):
    update.message.reply_text("""Hello! I am a bot that can monitor the CPU usage of your Linux VPS. 
    /cpu \uD83D\uDE4C command to see the current CPU usage.
    /processes \xF0\x9F\x92\xBB command to see the current running processes.
    """)


def cpu(update, context):
    usage = os.popen("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").read()
    update.message.reply_text(f'Current CPU usage: {usage}%')


def get_running_screens():
    screens = []
    try:
        output = subprocess.check_output(["screen", "-list"]).decode("utf-8")
        for line in output.split("\n"):
            if "." in line:
                screens.append(line.split(".")[0])
    except subprocess.CalledProcessError:
        pass

    return screens


def get_processes():
    screens = []
    for proc in psutil.process_iter():
        print(proc)
        if proc.name() == 'screen':
            print(proc)
            screens.append(proc.pid)
    return screens


def processes(update, context):

    running_processes = get_processes()
    update.message.reply_text(f'Current processes: {running_processes}')


def check_screen_status(screen_pid):
    for proc in psutil.process_iter():
        if proc.pid == int(screen_pid):
            return proc.status()


def status(update, context):
    screen_name = "12181"
    print(check_screen_status(screen_name))
    update.message.reply_text(check_screen_status(screen_name))


updater = Updater(BOT_TOKEN, use_context=True)
running_screens = get_running_screens()

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('cpu', cpu))
updater.dispatcher.add_handler(CommandHandler('processes', processes))
updater.dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling()
updater.idle()
