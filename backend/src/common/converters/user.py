from typing import Optional
from datetime import datetime

from backend.src.common.types import DTOType


def none_filter(data: Optional[DTOType | dict]) -> dict:
    return {k: v for k, v in data.model_dump().items() if v}


def convert_sending(data: dict) -> dict:
    date_format = '%Y-%m-%d %H:%M:%S.%f'

    data['is_superuser'] = str(data['is_superuser'])

    for field in ['created_at', 'updated_at']:
        if field in data and isinstance(data[field], datetime):
            data[field] = data[field].strftime(date_format)

    return data


def convert_receiving(data: dict) -> dict:
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    bool_map = {
        'True': True,
        'False': False,
    }

    data['is_superuser'] = bool_map[data['is_superuser']]

    for field in ['created_at', 'updated_at']:
        if field in data:
            data[field] = datetime.strptime(data[field], date_format)

    return data


