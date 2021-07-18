from jsons.exceptions import JsonsError

try:
    from zoneinfo import ZoneInfo


    def default_zone_info_deserializer(obj: ZoneInfo, *_, **__) -> ZoneInfo:
        """
        Deserialize a ZoneInfo.
        :param obj: a serialized ZoneInfo object.
        :return: an instance of ZoneInfo.
        """
        if not ZoneInfo:
            raise JsonsError('ZoneInfo is not available.')
        return ZoneInfo(obj['key'])

except ImportError:
    default_zone_info_deserializer = None
