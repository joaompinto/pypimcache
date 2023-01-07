import typer

from .cli import cmd_clean, cmd_list, cmd_serial, cmd_update, main


def app_main():
    app = typer.Typer(short_help="Cool")

    app.command()(cmd_clean.clean)
    app.command()(cmd_list.list)
    app.command()(cmd_serial.serial)
    app.command()(cmd_update.update)
    app.callback()(main.main)
    app()


if __name__ == "__main__":
    app_main()
