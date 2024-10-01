from cats.application.common.transaction import Transaction


class FakeTransaction(Transaction):
    def __init__(self) -> None:
        self.committed = False
        self.flushed = False

    async def commit(self) -> None:
        self.committed = True

    async def flush(self) -> None:
        self.flushed = True
