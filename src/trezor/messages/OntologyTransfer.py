# Automatically generated by pb2py
# fmt: off
import protobuf as p


class OntologyTransfer(p.MessageType):
    FIELDS = {
        1: ('asset', p.UVarintType, 0),
        2: ('amount', p.UVarintType, 0),
        3: ('from_address', p.UnicodeType, 0),
        4: ('to_address', p.UnicodeType, 0),
    }

    def __init__(
        self,
        asset: int = None,
        amount: int = None,
        from_address: str = None,
        to_address: str = None,
    ) -> None:
        self.asset = asset
        self.amount = amount
        self.from_address = from_address
        self.to_address = to_address
