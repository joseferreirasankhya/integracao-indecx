from datetime import datetime

class DateUtils:
    @staticmethod
    def convert_to_date(date_str: str) -> str:
        """
        Convert a date string to a date object
        """
        if date_str.endswith('Z'):
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
        else:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')

    @staticmethod
    def convert_to_date_time(date_str: str) -> str:
        """
        Convert a date string to a date object
        """
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
