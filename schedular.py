from apscheduler.schedulers.background import BackgroundScheduler

# 設置調度器和任務
def setup_scheduler():
    scheduler = BackgroundScheduler()

    # 添加解析 PPTX 的定時任務，使用 cron 表達式設定每天凌晨3點運行
    scheduler.add_job(id='testing_echo',func=testing_echo, trigger='cron', minute='*')

    # 返回 scheduler 實例
    return scheduler

def testing_echo():
    print('Testing from schedular')