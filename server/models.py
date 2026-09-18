from datetime import datetime, timezone

from sqlalchemy import Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from config import Config

engine = create_engine(Config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class RouteRequest(Base):
    __tablename__ = "route_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_lat: Mapped[float] = mapped_column(Float)
    start_lng: Mapped[float] = mapped_column(Float)
    end_lat: Mapped[float] = mapped_column(Float)
    end_lng: Mapped[float] = mapped_column(Float)
    profile: Mapped[str] = mapped_column(String, default="cycling-regular")
    distance_m: Mapped[float] = mapped_column(Float)
    duration_s: Mapped[float] = mapped_column(Float)
    ascent_m: Mapped[float] = mapped_column(Float)
    descent_m: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "start": [self.start_lat, self.start_lng],
            "end": [self.end_lat, self.end_lng],
            "profile": self.profile,
            "distance_m": self.distance_m,
            "duration_s": self.duration_s,
            "ascent_m": self.ascent_m,
            "descent_m": self.descent_m,
            "created_at": self.created_at.isoformat(),
        }
