from datetime import date

from agriweather.basis.rdbms import RDBStorage


class AsparagusStorage(RDBStorage):
    def __init__(
        self,
        db_host: str,
        db_user: str,
        db_password: str,
        db_name: str,
        log_path: str,
        log_level: str,
    ) -> None:
        super().__init__(
            db_host,
            3306,
            db_user,
            db_password,
            db_name,
            log_path,
            log_level,
        )

    def _get_today(self) -> str:
        today = date.today()
        return today.strftime("%Y-%m-%d")

    def get_forecast(self, farm_id: str) -> dict:
        sql = "SELECT * FROM `weather_forcast` WHERE farm_id='{0}';".format(farm_id)

        forecast = super().show_data(sql)
        return forecast
