import time
import calendar
from datetime import datetime
from xid import Xid, generate_deterministic_id

bucket_date = '2018-06-07'
report_id = "20180530T101600Z_AS44244_rZjYh4A1aLzv0qPhH9IWFsiVim1KgS11bNLdTXUTMGvSgFZ4ck"
measurement_start_time = "2018-06-06 10:15:19"
index = 10

def gen_measurement_id(report_id, bucket_date, measurement_start_time, entry_index):
    date_str = '{} {}'.format(bucket_date, measurement_start_time.split(' ')[-1])
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # the gotcha is to use calendar.timegm otherwise it will only work on a machine
    # that has a timezone set in UTC
    timestamp = calendar.timegm(dt.timetuple())

    return generate_deterministic_id(timestamp, report_id, entry_index)

def test_ids_are_unique():
    ids = []
    ids_set = set()
    for i in range(10000):
        # As a timestamp we use the bucket_date and the timestamp of the
        # measurement_start_time. This is to ensure that ordering of IDs is
        # done based on when the measurement is processed and not when it was
        # submitted.
        msmt_id = gen_measurement_id(report_id, bucket_date, measurement_start_time, i)
        ids.append(msmt_id)
        ids_set.add(msmt_id)
    assert len(ids) == len(ids_set)

if __name__ == '__main__':
    test_ids_are_unique()
    print('id: {}'.format(gen_measurement_id(report_id, bucket_date, measurement_start_time, 0)))
