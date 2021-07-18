from typing import Dict

try:
    from zoneinfo import ZoneInfo


    def default_zone_info_serializer(obj: ZoneInfo, *_, **__) -> Dict[str, str]:
        """
        Serialize a ZoneInfo object.
        :return: a serialized ZoneInfo instance.
        """
        return {'key': obj.key}

except ImportError:
    default_zone_info_serializer = None
