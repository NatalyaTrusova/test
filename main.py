import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, CheckConstraint, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError
from datetime import datetime

from telegram_logs import telegram_logger

user=os.environ["POSTGRES_USER"]
password=os.environ["POSTGRES_PASSWORD"]
dbname=os.environ["POSTGRES_DB"]
host="postgres_db"
port="5432"

def get_engine(user, password, host, port, dbname):
    try:
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        if not database_exists(url):
            create_database(url)
        engine = create_engine(url, echo=True)
        return engine
    except OperationalError:
        telegram_logger.critical(f"Something went wrong. User '{user}' is doing something strange in '{dbname}' "
                                 f"at {datetime.now()}! Probably, problem with authentication. Was it you?")

engine = get_engine(user, password, host, port, dbname)
Base = declarative_base()

class Column(Column):
    def __init__(self, *args, **kwargs):
        # Установим по дефолту не нулевые значения
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)

class HeroesWarfares(Base):
    __tablename__ = "heroes_warfares"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    hero_id = Column(Integer, ForeignKey("heroes.id"))
    warfare_id = Column(Integer, ForeignKey("warfares.id"))


class Heroes(Base):
    __tablename__ = "heroes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    birthday = Column(DateTime(timezone=True))
    side = Column(String(30))
    power = Column(Integer, nullable=True, default=None)
    update_dttm = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    children_slogans = relationship("Slogans", cascade="all, delete, delete-orphan")
    children_stories = relationship("Stories", uselist=False, back_populates="parent_heroes",
                                    cascade="all, delete, delete-orphan")
    children_warfares = relationship("Warfares", secondary="heroes_warfares", back_populates="parent_heroes")

    def __repr__(self):
        return f"{self.id}: {self.name} / {self.birthday} birthday / side {self.side} / power {self.power}"


class Slogans(Base):
    __tablename__ = "slogans"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey("heroes.id", ondelete="CASCADE"))
    moto = Column(Text)
    moto_id = Column(Integer)

    def __repr__(self):
        return f"{self.id} / {self.moto_id} slogan of {self.hero_id}: {self.moto}"


class Warfares(Base):
    __tablename__ = "warfares"

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer)
    hero_1_moto_id = Column(Integer, nullable=True)
    hero_2_id = Column(Integer)
    hero_2_moto_id = Column(Integer, nullable=True)
    winner = Column(Integer, nullable=True)

    # Уточним возможные значения для поля winner
    __table_args__ = (CheckConstraint(winner.in_([None, 1, 2])), {"extend_existing": True})

    parent_heroes = relationship("Heroes", secondary="heroes_warfares", back_populates="children_warfares")

    def __repr__(self):
        return f"{self.hero_1_id} vs {self.hero_2_id} / winner: {self.winner}"


class Stories(Base):
    __tablename__ = "stories"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    story = Column(Text)
    hero_id = Column(Integer, ForeignKey("heroes.id", ondelete="CASCADE"), unique=True)
    parent_heroes = relationship("Heroes", back_populates="children_stories")

    def __repr__(self):
        return f"{self.id} of hero {self.hero_id}: {self.story}"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def change_slogans_moto_id_before_insert(mapper, connection, target):
    """
    Trigger for automatic numeration of moto_id
    Возможно, не самая удачная идея с запросом в БД (при каждом добавлении надо делать этот запрос)
    Лучше разметить этот триггер в самой БД, к сожалению не успела доделать этот момент корректнее
    """
    with Session() as session:
        change_slogans_moto_id_query = session.query(Slogans.hero_id, func.count()).filter(
            Slogans.hero_id == target.hero_id).group_by(Slogans.hero_id).all()
        if (change_slogans_moto_id_query != []):
            target.moto_id = change_slogans_moto_id_query[0][1] + 1
        else:
            target.moto_id = 1
event.listen(Slogans, 'before_insert', change_slogans_moto_id_before_insert)



statistic_view_query = """
CREATE or REPLACE VIEW statistics_for_db as
(SELECT 'all_heroes' as measure, (Select count(*) FROM public.heroes) as value
union all
SELECT 'OP_heroes' as measure, (Select count(id) FROM public.heroes where side='Phoenix Order')
union all
SELECT 'DE_heroes' as measure, (Select count(id) FROM public.heroes where side='Death Eaters')
union all
SELECT 'all_warfares' as measure, (Select count(*) FROM public.warfares)
union all
SELECT 'OP_warfares' as measure, 
(SELECT count(*) FROM
	(Select hero_1_id, hero_2_id, winner, side1,
 		CASE WHEN winner=1 and side1='Death Eaters' THEN 'Death Eaters'
	         WHEN winner=1 and side1='Phoenix Order' THEN 'Phoenix Order'
	 		 WHEN winner=2 and side1='Death Eaters' THEN 'Phoenix Order'
	 		 WHEN winner=2 and side1='Phoenix Order' THEN 'Death Eaters'
	 	END
	    FROM (SELECT warfares.id, hero_1_id, hero_2_id, winner, heroes1.side as side1
			  FROM public.warfares join public.heroes as heroes1 
			  on public.warfares.hero_1_id=heroes1.id) as t) as v WHERE v.case='Phoenix Order')
union all
SELECT 'DE_warfares' as measure, 
(SELECT count(*) FROM
	(Select hero_1_id, hero_2_id, winner, side1,
 		CASE WHEN winner=1 and side1='Death Eaters' THEN 'Death Eaters'
	         WHEN winner=1 and side1='Phoenix Order' THEN 'Phoenix Order'
	 		 WHEN winner=2 and side1='Death Eaters' THEN 'Phoenix Order'
	 		 WHEN winner=2 and side1='Phoenix Order' THEN 'Death Eaters'
	 	END
	    FROM (SELECT warfares.id, hero_1_id, hero_2_id, winner, heroes1.side as side1
			  FROM public.warfares join public.heroes as heroes1 
			  on public.warfares.hero_1_id=heroes1.id) as t) as v WHERE v.case='Death Eaters')
union all
SELECT 'all_slogans' as measure, (SELECT count(*) FROM public.slogans)
union all
SELECT 'OP_slogans' as measure, 
(SELECT count(*) FROM
	(SELECT side
		FROM public.slogans join public.heroes 
		on public.slogans.hero_id=public.heroes.id) as v WHERE v.side='Phoenix Order')
union all
SELECT 'DE_slogans' as measure, 
(SELECT count(*) FROM
	(SELECT side
		FROM public.slogans join public.heroes 
		on public.slogans.hero_id=public.heroes.id) as v WHERE v.side='Death Eaters')
)
"""

engine.execute(statistic_view_query)