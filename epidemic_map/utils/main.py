from .get_data import Get_data


data = Get_data()
data.get_data()
time_in, time_out = data.get_time()
data.parse_data()

from . import execution

execution.china_map(time_in)
execution.province_map(time_in)
