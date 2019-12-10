import datetime
import pandas as pd
from sanic import Sanic
from config.config import Config
from sanic_jinja2 import SanicJinja2

app = Sanic(__name__)
Config.init_conf(app)
tp = SanicJinja2(app)
FLAG_153 = Config.FLAG


@app.route("/")
async def status(request):
    while True:
        d = check_flag(request)
        return tp.render('index.html', request, data=d)


def get_status(df, datetime_field, status_field):
    """
    function of data source status
    :param df: flag DataFrame
    :param datetime_field: eg: daily_status_checker_datetime -- 跑完checker的时间
    :param status_field: eg: daily_status_checker -- 跑完checker会给出一个状态：0 or 1
    :return: date/status
    """
    TODAY = datetime.datetime.now().strftime('%Y-%m-%d')
    if not pd.isna(df[datetime_field].tolist()[-1]):
        data_date = df[datetime_field].tolist()[-1].split(' ')[0]
    else:
        try:
            data_date = df[datetime_field].tolist()[-2].split(' ')[0]
        except IndexError:
            data_date = '请检查flag.csv文件'
    data_checker_status = df[status_field].tolist()[-1]  # 0 or 1

    if data_date == TODAY and data_checker_status == 1:
        step_status = 1
    else:
        step_status = 0

    return [data_date, step_status]


def check_flag(request):
    df = pd.read_csv(FLAG_153)
    # 153 qlib status
    data_obj_153 = get_status(df, 'daily_status_checker_datetime', 'daily_status_checker')
    daily_data_date_153 = data_obj_153[0]
    data_153_step_status = data_obj_153[1]

    # 153 factor status
    factor_obj_153 = get_status(df, 'factor_status_checker_datetime', 'factor_status_checker')
    factor_data_date_153 = factor_obj_153[0]
    factor_153_step_status = factor_obj_153[1]

    # upload to 154 status
    upload_154_obj = get_status(df, 'qlib_data_154_datetime', 'qlib_data_154')
    upload_date_154 = upload_154_obj[0]
    upload_step_status_154 = upload_154_obj[1]

    # upload to 150 status
    upload_150_obj = get_status(df, 'qlib_data_150_datetime', 'qlib_data_150')
    upload_date_150 = upload_150_obj[0]
    upload_step_status_150 = upload_150_obj[1]

    # 154 cache status
    cache_154_obj = get_status(df, 'server_154_update_cache_datetime', 'server_154_update_cache')
    cache_data_date_154 = cache_154_obj[0]
    cache_154_step_status = cache_154_obj[1]

    # 150 cache status
    cache_150_obj = get_status(df, 'server_150_update_cache_datetime', 'server_150_update_cache')
    cache_data_date_150 = cache_150_obj[0]
    cache_150_step_status = cache_150_obj[1]

    status_ret = {'daily_date_153': daily_data_date_153,
                  'factor_date_153': factor_data_date_153,
                  'cache_date_154': cache_data_date_154,
                  'cache_date_150': cache_data_date_150,
                  'upload_date_154': upload_date_154,
                  'upload_date_150': upload_date_150,

                  'step_data_153': data_153_step_status,
                  'step_factor_153': factor_153_step_status,
                  'step_cache_status_154': cache_154_step_status,
                  'step_cache_status_150': cache_150_step_status,
                  'step_upload_status_154': upload_step_status_154,
                  'step_upload_status_150': upload_step_status_150
                  }

    return status_ret


if __name__ == "__main__":
    app.run(host="10.150.144.153", port=8053)
