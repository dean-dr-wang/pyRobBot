#!/usr/bin/env python3
"""Commands supported by the package's script."""
import subprocess

from . import GeneralConstants
from .chat import Chat
from .chat_configs import ChatOptions


def accounting(args):
    """Show the accumulated costs of the chat and exit."""
    Chat.from_cli_args(cli_args=args).report_token_usage(current_chat=False)


def run_on_terminal(args):
    """Run the chat on the terminal."""
    chat = Chat.from_cli_args(cli_args=args)
    chat.start()
    if args.report_accounting_when_done:
        chat.report_token_usage(current_chat=True)


def run_on_ui(args):
    """Run the chat on the browser."""
    ChatOptions.from_cli_args(args).export(fpath=GeneralConstants.PARSED_ARGS_FILE)
    try:
        subprocess.run(
            [  # noqa: S603, S607
                "streamlit",
                "run",
                GeneralConstants.APP_PATH.as_posix(),
                "--",
                GeneralConstants.PARSED_ARGS_FILE.as_posix(),
            ],
            cwd=GeneralConstants.APP_DIR.as_posix(),
            check=True,
        )
    except (KeyboardInterrupt, EOFError):
        print("Exiting.")
