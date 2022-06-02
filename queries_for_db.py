from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import IntegrityError
import random
import fire

from main import engine, Heroes, Slogans, Warfares, Stories
import logging_configuraion
from telegram_logs import telegram_logger

engine = engine
Session = sessionmaker(bind=engine)

logger_info = logging_configuraion.my_logger_info
logger_error = logging_configuraion.my_logger_error

def add_new_hero(name: str, birthday: str, side: str, power: int=None) -> None:
    with Session() as session:
        birthday_as_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        session.add(Heroes(name=name, birthday=birthday_as_date, side=side, power=power))
        session.commit()
        logger_info.info(f"In Heroes added line: {name} | {birthday} | {side} | {power}")

def add_new_slogan(hero_id: int, moto: str) -> None:
    try:
        with Session() as session:
            session.add(Slogans(hero_id=hero_id, moto=moto))
            session.commit()
            logger_info.info(f"In Slogans added line: {hero_id} | {moto}")
    except IntegrityError:
        logger_error.error(f"Integrity error! There is no hero with {hero_id} id!")


def add_new_story(hero_id: int, story: str) -> None:
    try:
        with Session() as session:
            session.add(Stories(hero_id=hero_id, story=story))
            session.commit()
            logger_info.info(f"In Stories added line: {hero_id} | {story}")
    except IntegrityError:
        logger_error.error(f"Integrity error! There is no hero with {hero_id} id!")


def delete_hero(id: int) -> None:
    with Session() as session:
        session.query(Heroes).filter(Heroes.id==id).delete()
        session.commit()
        logger_info.warning(f"In Heroes was deleted line with id {id}")

def add_new_warfare() -> None:
    with Session() as session:
        warfare_hero_1 = session.query(Heroes).order_by(func.random()).limit(1).all()

        hero_1_id = warfare_hero_1[0].id
        hero_1_side = warfare_hero_1[0].side

        warfare_hero_2 = session.query(Heroes).filter(Heroes.side != hero_1_side).order_by(func.random()).limit(1).all()
        hero_2_id = warfare_hero_2[0].id

        hero_1_slogan = session.query(Slogans.id).filter(Slogans.hero_id == hero_1_id).order_by(func.random()).limit(1)\
            .scalar()
        hero_2_slogan = session.query(Slogans.id).filter(Slogans.hero_id == hero_2_id).order_by(func.random()).limit(1)\
            .scalar()

        possible_results = [1, 2, None]
        winner = random.choice(possible_results)

        session.add(Warfares(hero_1_id=hero_1_id, hero_1_moto_id=hero_1_slogan, hero_2_id=hero_2_id,
                             hero_2_moto_id=hero_2_slogan, winner=winner))
        session.commit()

        logger_info.info(f"In Warfares added line: {hero_1_id} | {hero_1_slogan} | {hero_2_id} | {hero_2_slogan} "
                         f"| {winner}")

def see_data_from_view() -> None:
    """
    Select data from view and returns it in more convenient way.
    """
    see_data_from_view_query="""SELECT * FROM public.statistics_for_db"""
    result_data = engine.execute(see_data_from_view_query)
    print("|_____measure_____|__value__|")
    # Выведем данные красивее, для этого запомним количество символов в заголовках таблицы
    # у measure - 17 вместе в буквами, у value - 9. Тогда к каждому новому значению прибавляем
    # необходимое количество пробелов с двух сторон, для красивого вывода
    for row in result_data:
        num_m=17-len(row[0])
        num_v=9-len(str(row[1]))
        first_half_m=num_m//2
        second_half_m=num_m-first_half_m
        first_half_v = num_v//2
        second_half_v = num_v - first_half_v
        print(f"|{' '*first_half_m}{row[0]}{' '*second_half_m}|{' '*first_half_v}{row[1]}{' '*second_half_v}|")

def function_for_admin_only(login, password):
    """
    Function for simple testing telegram alerts. Pass login="admin" and password="qwerty" for avoid alert and something
    different to raise it.
    """
    if login == "admin" and password == "qwerty":
        print("Hello, admin!")
    elif login == "admin" and password != "qwerty":
        telegram_logger.error(f"Admin tried to use function_for_admin_only, but the password '{password}' was incorrect!")
    else:
        telegram_logger.error(f"Warning! Not admin with login '{login}' tried to use function_for_admin_only!!!")


if __name__ == '__main__':
    # Необходимо для запуска функций в треминале. Команда вида "python queries_for_db.py function_name argument1
    # argument2"
    fire.Fire()




# add_new_hero(name="Harry Potter", birthday="1999-04-03", side="Phoenix Order", power=100)
# add_new_hero(name="Bellatrix Lestrange", birthday="1951-02-15", side="Death Eaters", power=90)
# add_new_hero(name="Sirius Black", birthday="1961-02-15", side="Phoenix Order", power=85)
# add_new_hero(name="Lucius Malfoy", birthday="1941-03-12", side="Death Eaters", power=80)
# add_new_hero(name="Ron Weasley", birthday="1981-03-14", side="Phoenix Order", power=99)
# add_new_hero(name="Draco Malfoy", birthday="1980-10-30", side="Death Eaters")
# add_new_hero(name="Albus Dumbledore", birthday="1920-10-30", side="Phoenix Order")
#
#add_new_story(hero_id=1, story="First survived Avada Kedavra. His parents were killed then he was a little boy.")
# add_new_story(hero_id=2, story="Death Eater, Voldemort's most zealous henchman.")
#
# add_new_slogan(hero_id=1, moto="But I'm Harry... Just a Harry!")
# add_new_slogan(hero_id=2, moto="I've killed Sirius Black!")
# add_new_slogan(hero_id=3, moto="Each has both a white and a black side.")
# add_new_slogan(hero_id=7, moto="Do you want lemon slices?")
#add_new_slogan(hero_id=1, moto="We'll save everyone!")
#
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
# add_new_warfare()
#add_new_warfare(test='yep')
#
# delete_hero(7)

##Ошибочный вариант
#add_new_slogan(hero_id=10, moto="I've killed Sirius Black!")

#see_data_from_view()