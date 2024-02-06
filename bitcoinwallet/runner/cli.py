from __future__ import annotations

import uvicorn
from typer import Typer

from bitcoinwallet.core.repository.repository_factory import RepositoryFactory
from bitcoinwallet.runner.setup import init_app
from definitions import DB_NAME
from resources.db.sql import db_setup

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    db_setup(DB_NAME)
    uvicorn.run(host=host, port=port, app=init_app(RepositoryFactory.get_instance()))
