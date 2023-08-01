from dataclasses import dataclass
from services.sql import DataBase
# from services.pSQL import DataBaseGeo
# from services.play_sql import DataBaseGeoUs

@dataclass
class Config:
    token: str = 'тут был токен'
    mychat_id: int = 438588745
    admin_id = 438588745
    admins_id = [438588745]
    banty = 6273449914
    chatMG_id: int = -1001943388426
    logchat: int = -1001825737431
    db = DataBase()
    MESS_MAX_LENGTH = 4096
    # dbGeo = DataBaseGeo()
    # dbGeoUs = DataBaseGeoUs()
    # jobstores = {
    #     'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
    #                              run_times_key='dispatched_trips_running',
    #                              db=2,
    #                              port=6379)
    # }
    # scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="Asia/Yekaterinburg", jobstores=jobstores))

