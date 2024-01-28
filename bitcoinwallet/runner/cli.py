from __future__ import annotations

import uvicorn
from typer import Typer

from bitcoinwallet.runner.setup import init_app

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    uvicorn.run(host=host, port=port, app=init_app())
