import sqlalchemy.orm as sao
from datetime import datetime, timedelta
from mtg_deck_editor import db
import time

def allow(service_name, max_count = 10, duration = 1):
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


class ServiceCache(db.Model):
    id : sao.Mapped[int] = sao.mapped_column(primary_key=True, autoincrement=True)
    service: sao.Mapped[str] = sao.mapped_column(nullable=False)
    method : sao.Mapped[str] = sao.mapped_column(nullable=False)
    expiry : sao.Mapped[datetime] = sao.mapped_column(nullable=False)

    scryfall_get_card : sao.WriteOnlyMapped["GetCardCached"] = sao.relationship(cascade="all,delete-orphan", passive_deletes=True)

    def __init__(self, service: str, method : str, expiry: datetime = datetime.now()):
        super().__init__()

        self.service = service
        self.method = method
        self.expiry = expiry

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_or_default(service: str, method_name: str) -> "ServiceCache":
        cache : ServiceCache = db.session.execute(
            db.select(ServiceCache)
            .where(ServiceCache.service == service)
            .where(ServiceCache.method == method_name)).scalar()
        if cache is not None and (datetime.now() - cache.expiry).days > 1:
            cache.delete()
            cache = None
        if cache is None:
            cache = ServiceCache(service, method_name)
            db.session.add(cache)
            db.session.commit()
        return cache