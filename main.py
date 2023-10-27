from cet import class_cet 
from ciscn import class_ciscn
from dayingsai import class_daying
from guosai import class_guosai
from lanqiaobei import class_lanqiao
from mcm import class_mcm
from nuedc import class_nuedc
from wsc import class_wsc
import concurrent.futures
import redis 
import time


conn = redis.Redis
def run_class(class_obj):
    instance = class_obj()
    instance.run()
    time.sleep(30)
        
def run():
    import time
    while True:
        pool_size = 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            executor.map(run_class, classes_to_run)
        print('############################所有程序已成功运行一次，现休眠24h...#################################')
        time.sleep(60*60*24)
        
if __name__ == '__main__':
    classes_to_run = [class_guosai, class_cet, class_ciscn, class_daying, class_lanqiao, class_mcm, class_nuedc, class_wsc]
    run()
    # pool_size = 2
    # with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
    #     executor.map(run_class, classes_to_run)

