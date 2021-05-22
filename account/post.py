import enum


class Position(enum.Enum):
    CMO = 'Старший менеджер по обслуживанию'
    BMO = 'Ведущий менеджер по обслуживанию'
    MO = 'Менеджер по обслуживанию'
    CKM = 'Старший клиентский менеджер'
    KM = 'Клиентский менеджер'
    K = 'Консультант'


class PostCode(enum.IntEnum):
    BIR = 4157
    HAB = 9070
    PRIM = 8635
    BLAG = 8636
    SAKH = 8567
    WEST = 8645
    CHUK = 8557
    KAM = 8556
