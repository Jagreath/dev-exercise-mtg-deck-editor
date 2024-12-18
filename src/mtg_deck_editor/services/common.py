import sqlalchemy.orm as sao
from datetime import datetime, timedelta
from mtg_deck_editor import db

def check_rate_limit(service_name, max_count = 10, duration = 1):
    with db.session.begin_nested() as st:
        rl_entry = db.session.execute(
            db.select(RateLimit)
            .filter(RateLimit.service == service_name)).scalar()
        if rl_entry is None:
            rl_entry = RateLimit(service=service_name, limit_window=(datetime.now() + timedelta(seconds=duration)))
            db.session.add(rl_entry)
        if rl_entry.limit_window < datetime.now():
            rl_entry.count = 0
            rl_entry.limit_window = datetime.now() + timedelta(seconds=duration)
        if rl_entry.count < max_count:
            rl_entry.count += 1
            st.commit()
            return True
        return False

# def allow_wait(service_name, max_count = 10, duration = 1, timeout = 10):
#     start_time = datetime.now()
#     while not allow(service_name, max_count, duration):
#         if (datetime.now() - start_time).seconds > timeout:
#             raise "Timeout"
#         time.sleep(duration) # or something, I don't know
        

class RateLimit(db.Model):
    service: sao.Mapped[str] = sao.mapped_column(primary_key=True)
    count: sao.Mapped[int] = sao.mapped_column(nullable=False, default=0)
    limit_window: sao.Mapped[datetime] = sao.mapped_column(nullable=False)

    def __init__(self, service : str ="None", count : int =0, limit_window : datetime =datetime.min):
        super().__init__()
        self.service = service
        self.count = count
        self.limit_window = limit_window
