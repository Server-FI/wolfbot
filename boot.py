import json,re,locale
from datetime import datetime
from sqlalchemy import create_engine, insert, select, update, Table, MetaData
locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
#Необязательная функция. Если вы не будете выкладывать токен в общий доступ, то можете прописывать токен сразу в AsyncTelebot
def access():
    with open("ВАШ ПУТЬ К JSON ФАЙЛУ С ТОКЕНОМ(АМИ)", "r",encoding="utf-8") as f:
        return json.load(f)

def write_log(text):
    with open("logs.txt","a",encoding="utf-8") as f:
        f.write(f"Время: {datetime.now().strftime('%d-%B-%Y %H:%M:%S')}. Действие: {text}\n")

def con():
    global engine
    engine=create_engine(f'mysql://{access()["login_tg"]}:{access()["password_tg"]}@{access()["ip"]}/telegram')

def add_group(a,b):
    try:
        table=Table("groups",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdGroup==a)
        resp1=insert(table).values(IdGroup=a,NameGroup=b,Warns=5)
        with engine.begin() as con:
            bf=con.execute(resp).fetchone()
            if bf==None:
                con.execute(resp1)
    except Exception as e:
        print(f"Ошибка: {e}")
    
def search_group(a):
    try:
        table=Table("groups",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdGroup==a)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[0]
    except Exception as e:
        print(f"Ошибка: {e}")

def update_group(a,b):
    try:
        table=Table("groups",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.IdGroup==a).values(NameGroup=b)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def update_filter(a,b):
    try:
        table=Table("filter",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.IdMember=="NULL",table.c.NameMember==b).values(IdMember=a)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def add_filter(a,b,c):
    try:
        table=Table("filter",MetaData(),autoload_with=engine)
        resp=insert(table).values(IdMember=a,NameMember=b,ReasonMember=c)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def add_user(a,b,c,d):
    group=search_group(c)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        resp1=insert(table).values(IdUser=a,NameUser=b,GroupUser=group,MoneyUser=0,WarnsUser=0,StatusUser=d)
        with engine.begin() as con:
            if con.execute(resp).fetchone()==None:
                con.execute(resp1)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_user(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[0]
    except Exception as e:
        print(f"Ошибка: {e}")

def search_username(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.NameUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[1]
    except Exception as e:
        print(f"Ошибка: {e}")

def search_userid(a):
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.KeyUser==a)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[1]
    except Exception as e:
        print(f"Ошибка: {e}")

def update_username(a,b):
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.IdUser==a).values(NameUser=b)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_filter(a,b):
    try:
        table=Table("filter",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdMember==a,table.c.NameMember==b)
        with engine.begin() as con:
            res=con.execute(resp).fetchone()
        if res==None:
            return None
        else:
            return res[0]
    except Exception as e:
        print(f"Ошибка: {e}")

def add_warn(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            warns=con.execute(resp).fetchone()[7]+1
            resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(WarnsUser=warns)
            con.execute(resp1)
    except Exception as e:
        print(f"Ошибка: {e}")

def add_money(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            money=con.execute(resp).fetchone()[4]+5
            resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(MoneyUser=money)
            con.execute(resp1)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_money(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[4]
    except Exception as e:
        print(f"Ошибка: {e}")

def minus_money(a,b,c):
    group=search_group(b)
    money=search_money(a,b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(MoneyUser=money-c)
        with engine.begin() as con:
            write_log(f"Пользователь под id {a} потратил {c} монет")
            return con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_warn(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[7]
    except Exception as e:
        print(f"Ошибка: {e}")

def search_warn_group(a):
    try:
        table=Table("groups",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdGroup==a)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[2]
    except Exception as e:
        print(f"Ошибка: {e}")

def change_warn_group(a,b):
    try:
        table=Table("groups",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.IdGroup==a).values(Warns=b)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def support():
    sup=""
    try:
        table=Table("support",MetaData(),autoload_with=engine)
        resp=select(table)
        with engine.begin() as con:
            com=con.execute(resp).fetchall()
        for i in com:
            sup+=f"[{i[1]}](https://t.me/{i[2]})\n"
        return sup
    except Exception as e:
        print(f"Ошибка: {e}")

def search_items(a,b):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(resp).fetchone()[6]
    except Exception as e:
        print(f"Ошибка: {e}")

def add_item(a,b,c,d):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            inv=con.execute(resp).fetchone()[6]
        if inv==None:
            resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(Items=f"{c}:{d},")
            with engine.begin() as con:
                con.execute(resp1)
        else:
            n_inv=""
            for i in inv.split(","):
                item=i.split(":")
                match len(item[0]):
                    case 0:
                        None
                    case _:
                        if c==item[0]:
                            c_count=int(item[1])+d
                            n_inv+=f"{item[0]}:{str(c_count)},"
                        else:
                            n_inv+=f"{item[0]}:{item[1]},"
            if re.search(str(c),n_inv)==None:
                n_inv+=f"{str(c)}:{str(d)},"
            else:
                None
            resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(Items=n_inv)
            with engine.begin() as con:
                con.execute(resp1)
        write_log(f"В инвентарь пользователя под id {a} добавлен предмет {c} в количестве {d}")
    except Exception as e:
        print(f"Ошибка: {e}")

def search_item(a):
    try:
        table=Table("magazin",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.NameItem==a)
        with engine.begin() as con:
            return con.execute(resp).fetchone()
    except Exception as e:
        print(f"Ошибка: {e}")

def minus_item(a,b):
    count=search_item(a)[2]
    try:
        table=Table("magazin",MetaData(),autoload_with=engine)
        resp=update(table).where(table.c.NameItem==a).values(CountItem=count-b)
        with engine.begin() as con:
            write_log(f"Из магазина выкуплен {a} в количестве {b}")
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_magazin():
    try:
        table=Table("magazin",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.CountItem>0)
        with engine.begin() as con:
            return con.execute(resp).fetchall()
    except Exception as e:
        print(f"Ошибка: {e}")

def update_magazin():
    try:
        table=Table("magazin",MetaData(),autoload_with=engine)
        resp=select(table)
        with engine.begin() as con:
            mag=con.execute(resp)
            for i in mag:
                resp1=update(table).where(table.c.NameItem==i[1]).values(CountItem=i[3])
                con.execute(resp1)
        write_log("Магазин обновлён")
    except Exception as e:
        print(f"Ошибка: {e}")

def add_read(a,b,c,d,e):
    try:
        table=Table("journal",MetaData(),autoload_with=engine)
        group=search_group(b)
        user=search_user(a,b)
        resp=insert(table).values(Date=e,IdUser=user,GroupUser=group,Type=c,Reason=d)
        with engine.begin() as con:
            con.execute(resp)
    except Exception as e:
        print(f"Ошибка: {e}")

def search_guilds(a):
    try:
        table=Table("guilds",MetaData(),autoload_with=engine)
        group=search_group(a)
        resp=select(table).where(table.c.GroupGuild==group)
        with engine.begin() as con:
            return con.execute(resp).fetchall()
    except Exception as e:
        print(f"Ошибка: {e}")

def create_new_guild(a,b,c,d):
    try:
        owner=search_user(a,b)
        group=search_group(b)
        table=Table("guilds",MetaData(),autoload_with=engine)
        table1=Table("users",MetaData(),autoload_with=engine)
        new_guild=insert(table).values(NameGuild=c,TypeGuild=d,GroupGuild=group,Owner=owner,CountMember=1,MaxCount=5)
        id_guild=search_guild(c,b)
        with engine.begin() as con:
            con.execute(new_guild)
            con.execute(update(table1).where(table1.c.KeyUser==owner).values(GuildUser=id_guild[0]))
    except Exception as e:
        print(f"Ошибка: {e}")

def search_guild(a,b):
    try:
        group=search_group(b)
        table=Table("guilds",MetaData(),autoload_with=engine)
        guild=select(table).where(table.c.NameGuild==a,table.c.GroupGuild==group)
        with engine.begin() as con:
            return con.execute(guild).fetchone()
    except Exception as e:
        print(f"Ошибка: {e}")

def check_user_guild(a,b):
    try:
        group=search_group(b)
        table=Table("users",MetaData(),autoload_with=engine)
        user=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(user).fetchone()[5]
    except Exception as e:
        print(f"Ошибка: {e}")

def search_owner(a):
    try:
        table=Table("guilds",MetaData(),autoload_with=engine)
        guild=select(table).where(table.c.KeyGuild==a)
        with engine.begin() as con:
            return con.execute(guild).fetchone()[4]
    except Exception as e:
        print(f"Ошибка: {e}")

def join_ex_guild(a,b,c):
    try:
        group=search_group(b)
        table=Table("users",MetaData(),autoload_with=engine)
        table1=Table("guilds",MetaData(),autoload_with=engine)
        guild=select(table1).where(table1.c.NameGuild==c,table1.c.GroupGuild==group)
        with engine.begin() as con:
            info=con.execute(guild).fetchone()
            con.execute(update(table1).where(table1.c.NameGuild==c,table1.c.GroupGuild==group).values(CountMember=info[5]+1))
            con.execute(update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(GuildUser=info[0]))
    except Exception as e:
        print(f"Ошибка: {e}")

def leave_ex_guild(a,b,c):
    try:
        group=search_group(b)
        table=Table("users",MetaData(),autoload_with=engine)
        table1=Table("guilds",MetaData(),autoload_with=engine)
        guild=select(table1).where(table1.c.KeyGuild==c)
        with engine.begin() as con:
            info=con.execute(guild).fetchone()
            con.execute(update(table1).where(table1.c.NameGuild==c,table1.c.GroupGuild==group).values(CountMember=info[5]-1))
            con.execute(update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(GuildUser="NULL"))
    except Exception as e:
        print(f"Ошибка: {e}")

def search_info_user(a,b):
    try:
        group=search_group(b)
        table=Table("users",MetaData(),autoload_with=engine)
        user=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            return con.execute(user).fetchone()
    except Exception as e:
        print(f"Ошибка: {e}")

def search_info_guild(a):
    try:
        table=Table("guilds",MetaData(),autoload_with=engine)
        table1=Table("users",MetaData(),autoload_with=engine)
        guild=select(table).where(table.c.KeyGuild==a)
        users=select(table1).where(table1.c.GuildUser==a)
        with engine.begin() as con:
            return con.execute(guild).fetchone(),con.execute(users).fetchall()
    except Exception as e:
        print(f"Ошибка: {e}")

def change_rights(a,b):
    try:
        table=Table("guilds",MetaData(),autoload_with=engine)
        guild=update(table).where(table.c.KeyGuild==b).values(Owner=a)
        with engine.begin() as con:
            con.execute(guild)
    except Exception as e:
        print(f"Ошибка: {e}")

def add_guild_item(a,b,c):
    try:
        table=Table("guilds",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.KeyGuild==a)
        with engine.begin() as con:
            inv=con.execute(resp).fetchone()[-1]
        if inv==None:
            resp1=update(table).where(table.c.KeyGuild==a).values(Items=f"{b}:{c},")
            with engine.begin() as con:
                con.execute(resp1)
        else:
            n_inv=""
            for i in inv.split(","):
                item=i.split(":")
                match len(item[0]):
                    case 0:
                        pass
                    case _:
                        if b==item[0]:
                            c_count=int(item[1])+c
                            n_inv+=f"{item[0]}:{str(c_count)},"
                        else:
                            n_inv+=f"{item[0]}:{item[1]},"
            if re.search(str(b),n_inv)==None:
                n_inv+=f"{str(b)}:{str(c)},"
            else:
                pass
            resp1=update(table).where(table.c.KeyGuild==a).values(Items=n_inv)
            with engine.begin() as con:
                con.execute(resp1)
        write_log(f"В инвентарь гильдии под id {a} добавлен предмет {b} в количестве {c}")
    except Exception as e:
        print(f"Ошибка: {e}")

def minus_user_item(a,b,c,d):
    group=search_group(b)
    try:
        table=Table("users",MetaData(),autoload_with=engine)
        resp=select(table).where(table.c.IdUser==a,table.c.GroupUser==group)
        with engine.begin() as con:
            inv=con.execute(resp).fetchone()[6]
        n_inv=""
        for i in inv.split(","):
            item=i.split(":")
            match len(item[0]):
                case 0:
                    pass
                case _:
                    if c==item[0]:
                        c_count=int(item[1])-d
                        match c_count:
                            case 0:
                                pass
                            case _:
                                n_inv+=f"{item[0]}:{str(c_count)},"
                    else:
                        n_inv+=f"{item[0]}:{item[1]},"
            match len(n_inv):
                case 0:
                    resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(Items=None)
                case _:
                    resp1=update(table).where(table.c.IdUser==a,table.c.GroupUser==group).values(Items=n_inv)
            with engine.begin() as con:
                con.execute(resp1)
        write_log(f"Из инвентаря пользователя под id {a} взят предмет {c} в количестве {d}")
    except Exception as e:
        print(f"Ошибка: {e}")