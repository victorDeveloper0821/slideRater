from apscheduler.schedulers.background import BackgroundScheduler

# 設置調度器和任務
def setup_scheduler():
    scheduler = BackgroundScheduler()

    # 添加解析 PPTX 的定時任務，使用 cron 表達式設定每天凌晨3點運行
    #scheduler.add_job(func=parse_pptx_and_save, trigger='cron', hour=3, minute=0)

    # 返回 scheduler 實例
    return scheduler