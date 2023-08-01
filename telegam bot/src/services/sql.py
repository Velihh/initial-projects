import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def output1(list):
    itog = []
    for i in list:
        try:
            itog.append(",".join(map(str, i)))
        except(TypeError):
            itog.append(",".join(map(str, 'Неопределен')))
    return itog

def output(list):
    itog = []
    for i in list:
        try:
            itog.append("^".join(map(str, i)).split('^'))
        except(TypeError):
            itog.append("^".join(map(str, 'Неопределен')).split('^'))
    return itog

class DataBase:
    def __init__(self):
        self.connect = psycopg2.connect(database='legends', user="postgres", password="Assas12")
        self.connect.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connect.cursor()

    async def add_users(self, user, character, tradition, tgid):
        with self.connect:
            return self.cursor.execute("""INSERT INTO users (name_user, hero, tradition,tgid) VALUES (%s, %s, %s, %s)""",
                                       (user, character, tradition, tgid))

    async def add_dis(self,name_, lat, lon, radius):
        with self.connect:
            return self.cursor.execute("""INSERT INTO geo (name_, charge, pt, radius) VALUES (%s, 50, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s)""",
                                       (name_, lon,lat, radius))

    async def get_name(self, tg_id):
        with self.connect:
            self.cursor.execute("""SELECT hero FROM users WHERE tgid=%s""", (tg_id,))
            f = self.cursor.fetchone()[0]
            return f

    async def get_one(self, tg_id, col):
        str_ = f"SELECT {col} FROM users WHERE tgid=%s"
        with self.connect:
            self.cursor.execute(str_, (tg_id,))
            f = self.cursor.fetchone()[0]
            return f

    async def get_tgid(self, id_):
        str_ = f"SELECT tgid FROM users WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (id_,))
            f = self.cursor.fetchone()[0]
            return f

    async def get_name_max_on_id(self, id_):
        str_ = f"SELECT hero, max_charge FROM users WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (id_,))
            f = self.cursor.fetchone()
            return f

    async def get_name_on_id(self, id_):
        str_ = f"SELECT hero FROM users WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (id_,))
            f = self.cursor.fetchone()[0]
            return f



    async def get_state(self, tg_id):
        with self.connect:
            self.cursor.execute("""SELECT hero, tradition, charge, max_charge, district FROM users WHERE tgid=%s""", (tg_id,))
            f = self.cursor.fetchone()
            return f

    async def get_dis(self):
        with self.connect:
            self.cursor.execute("""SELECT id, timer  FROM districts""")
            f = output(self.cursor.fetchall())
            return f

    async def get_dis_max(self, id_):
        with self.connect:
            self.cursor.execute("""SELECT dis, max_charge FROM districts WHERE id=%s""", (id_,))
            f = self.cursor.fetchone()
            return f

    def get_stateA(self, id):
        with self.connect:
            self.cursor.execute("""SELECT id, name_user, hero, tradition, charge, max_charge, district FROM users WHERE id=%s""", (id,))
            df = self.cursor.fetchone()
            f = f"id {df[0]} Игрок: {df[1]}\n" \
                f"Персонаж: {df[2]}\n" \
                f"Традиция: {df[3]}\n" \
                f"Зарядов: {df[4]}\n" \
                f"Максимальное количество зарядов: {df[5]}\n" \
                f"Район: {df[6]}"
            return f

    def get_statedis(self, id):
        with self.connect:
            self.cursor.execute("""SELECT id, dis, timer, notes, charge, max_charge FROM districts WHERE id=%s""", (id,))
            df = self.cursor.fetchone()
            f = f"id {df[0]} Район: {df[1]}\n" \
                f"Зарядов: {df[4]}\n" \
                f"Максимальное количество зарядов: {df[5]}\n" \
                f"Цикл района: {df[2]} минут\n" \
                f"Аномалии: {df[3]}"
            return f

    async def change_charge(self, tg_id, count):
        with self.connect:
            self.cursor.execute("""UPDATE users SET charge=charge-%s WHERE tgid=%s""",
                                (count, tg_id))
            self.cursor.execute("""SELECT charge FROM users WHERE tgid=%s""", (tg_id,))
            f = self.cursor.fetchone()[0]
        return f

    async def up_geo(self, tg_id, lat, lon):
        with self.connect:
            self.cursor.execute("""SELECT live_time FROM users WHERE tgid=%s""", (tg_id,))
            live_time = self.cursor.fetchone()[0]
            self.cursor.execute("""
            WITH dist AS (
            SELECT dis
                FROM districts
                WHERE ST_Within((SELECT pt
                    FROM users
                    WHERE tgid=%s), geom)
                LIMIT 1
            )
            
            UPDATE users SET live_time=1, 
            pt=ST_SetSRID(ST_MakePoint(%s, %s), 4326), 
            district= CASE WHEN (SELECT dis from dist) ='' THEN 'Неопределен' ELSE (SELECT dis from dist) END
            WHERE tgid=%s""",
                                (tg_id, lon, lat, tg_id))
        return live_time

    async def null_power(self, tgid):
        with self.connect:
            self.cursor.execute('''UPDATE users SET power = 0 WHERE tgid=%s
                        ''', (tgid,))

    async def up_charge(self, tg_id, dis):
        with self.connect:
            self.cursor.execute("""
            UPDATE districts 
            SET charge = CASE WHEN charge <-1 THEN charge ELSE charge - 1 END 
            WHERE dis=%s;
            
            UPDATE users 
            SET charge = CASE WHEN (SELECT charge FROM districts WHERE dis = %s) <-1 THEN charge WHEN charge < max_charge THEN charge+1 ELSE charge END WHERE tgid=%s;
            
            """,(dis, dis,tg_id))

            self.cursor.execute('''SELECT charge FROM users WHERE tgid=%s
            ''', (tg_id,))
            charge_us = self.cursor.fetchone()[0]
            self.cursor.execute('''SELECT charge FROM districts WHERE dis=%s
                        ''', (dis,))
            charge_geo = self.cursor.fetchone()[0]
            return charge_us, charge_geo

    async def up_charge_rit(self, tg_id, dis):
        with self.connect:
            self.cursor.execute("""
            UPDATE districts SET charge = CASE WHEN charge <=-10 THEN charge ELSE charge - 1 END WHERE dis=%s;
            
            UPDATE users 
            SET 
            charge = CASE WHEN (SELECT charge FROM districts WHERE dis=%s) <=-10 THEN charge WHEN charge < max_charge THEN charge+1 ELSE charge END, 
            power = CASE WHEN (SELECT charge FROM districts WHERE dis=%s) <=-10 THEN power WHEN charge < max_charge THEN power+1 ELSE power END
            WHERE tgid=%s;
 
            """,(dis,dis, dis,tg_id))

            self.cursor.execute('''SELECT power FROM users WHERE tgid=%s
                                    ''', (tg_id,))
            power = self.cursor.fetchone()[0]
            self.cursor.execute('''SELECT charge FROM districts WHERE dis=%s
                        ''', (dis,))
            charge_geo = self.cursor.fetchone()[0]
            return charge_geo, power

    async def stop_live(self, tg_id):
        with self.connect:
            self.cursor.execute("""UPDATE users SET live_time=0, pt=%s,district=%s WHERE tgid=%s""",
                                (None, 'Неопределен', tg_id))

    async def stop_live_all(self):
        with self.connect:
            self.cursor.execute("""UPDATE users SET live_time=0, pt=%s,district=%s""",
                                (None, 'Неопределен'))

    async def up_one_on_id(self, col, zna, id_):
        str_ = f"UPDATE users SET {col}=%s WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (zna, id_))

    async def up_dis_on_id(self, col, zna, id_):
        str_ = f"UPDATE districts SET {col}=%s WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (zna, id_))

    async def up_disChar_on_id(self, zna, id_):
        str_ = f"UPDATE districts SET charge=charge + %s WHERE id=%s"
        with self.connect:
            self.cursor.execute(str_, (zna, id_))
            self.cursor.execute('''SELECT charge FROM districts WHERE id=%s''', (id_,))
            return self.cursor.fetchone()[0]

    async def up_acive_dis(self, id_):
        with self.connect:
            self.cursor.execute("""
            WITH dist AS (
            SELECT charge, geom FROM districts WHERE id=%s
            ), count_ AS (
            SELECT COUNT(districts.charge) AS Co FROM districts, dist 
            WHERE ST_Intersects(dist.geom, districts.geom)
            AND districts.charge > 0
            
            )
            
            UPDATE districts SET charge = charge - CEILING((SELECT ABS(charge) FROM dist) / (SELECT CEILING(Co) FROM count_) / 5)
            WHERE 
            id IN (SELECT id FROM districts, dist WHERE dist.charge < -4 AND ST_Intersects(dist.geom, districts.geom)) 
            AND id!=%s
            AND districts.charge > 0;
            
            UPDATE districts SET charge = CASE 
            WHEN charge >= max_charge THEN max_charge 
            WHEN charge <-4 THEN charge + FLOOR(ABS(charge) / 5)
            ELSE charge + 1 
            END
            WHERE id=%s""", (id_,id_,id_))

    async def get_names(self, search_query: str = None):
        statement = "SELECT id, name_user, hero FROM users"
        with self.connect:
            if search_query != None:
                statement += f" WHERE name_user LIKE %s OR hero LIKE %s"
                self.cursor.execute(statement, (f'%{search_query}%', f'%{search_query}%'))
            else:
                statement += f" ORDER BY hero"
                self.cursor.execute(statement)

            return output(self.cursor.fetchall())

    async def get_dist(self):
        statement = "SELECT id, dis FROM districts ORDER BY dis"
        with self.connect:
            self.cursor.execute(statement)
            return output(self.cursor.fetchall())

    async def transfer_of_charges(self, tgid):
        statement = f"SELECT id, hero FROM users " \
                    f"WHERE 1000 >= ST_DistanceSphere(pt, (SELECT pt FROM users WHERE tgid={tgid})) " \
                    f"AND  tgid != '{tgid}'" \
                    f"ORDER BY hero"
        with self.connect:
            self.cursor.execute(statement)
            return output(self.cursor.fetchall())

    async def get_tarif(self, tg_id, id):
        str_ = f"""SELECT charge - CASE WHEN tradition = (SELECT tradition FROM users WHERE id=%s) THEN 1 ELSE 2 END 
        FROM users WHERE tgid=%s"""
        with self.connect:
            self.cursor.execute(str_, (id, tg_id))
            f = self.cursor.fetchone()[0]
        return f

    async def transfer_of_charges1(self, tgid, id_, charge):
        with self.connect:
            self.cursor.execute("""
            UPDATE users SET charge=charge - CASE WHEN tradition = (SELECT tradition FROM users WHERE id=%s) THEN 1 ELSE 2 END - %s
            WHERE tgid = %s
            """,(id_, charge, tgid))
            self.cursor.execute("""
            UPDATE users SET charge = CASE WHEN max_charge <= charge + %s THEN max_charge ELSE charge + %s END
            WHERE id = %s
            """, (charge,charge, id_))
            self.cursor.execute("""SELECT charge FROM users WHERE tgid=%s""", (tgid,))
            f = self.cursor.fetchone()[0]
        return f

    async def up_us_charge(self, charge,id):
        with self.connect:
            self.cursor.execute("""
            UPDATE users SET charge = %s WHERE id=%s
            """,(charge, id))

    async def up_us_maxcharge(self, charge,id):
        with self.connect:
            self.cursor.execute("""
            UPDATE users SET max_charge = %s WHERE id=%s
            """,(charge, id))

    async def print_spesh_geo(self, id):
        with self.connect:
            self.cursor.execute("""SELECT ST_AsGeoJSON(pt) FROM users WHERE id=%s""", (id,))
            f = self.cursor.fetchone()[0]
            return f

    async def tochseach(self, lat, lon, id_us):
        with self.connect:
            self.cursor.execute(f"SELECT ST_DistanceSphere(ST_SetSRID(ST_MakePoint({lat}, {lon}), 4326), e.pt) AS t "
                    f"FROM geo"
                    f"WHERE (radius >= ST_DistanceSphere(ST_SetSRID(ST_MakePoint({lat}, {lon}), 4326), e.pt) "
                    f"ORDER BY t ")
        return self.cursor.fetchone()

    async def save_msg(self, id, tgid, text, m_id):
        with self.connect:
            return self.cursor.execute("""INSERT INTO base_message (id, tgid, text, m_id) VALUES (%s, %s, %s, %s)""",
                                       (id, tgid, text, m_id))

    async def get_msq(self, id):
        with self.connect:
            self.cursor.execute("""SELECT * FROM base_message WHERE id=%s""", (id,))
            f = self.cursor.fetchone()
            return f

    async def get_map(self):
        with self.connect:
            self.cursor.execute("""SELECT dis, charge, notes FROM districts""")
            coor = output(self.cursor.fetchall())
            return coor

    async def admin_get_map(self):
        with self.connect:
            self.cursor.execute("""SELECT dis, charge, notes, max_charge,timer  FROM districts""")
            coor = output(self.cursor.fetchall())
            return coor

    def print_geo(self):
        with self.connect:
            self.cursor.execute("""
                            SELECT hero, ST_AsGeoJSON(pt)
                            FROM users
                            WHERE pt IS NOT NULL
                            ;
                            """)
            return output(self.cursor.fetchall())

    async def add_geo(self, user_id, lat, lon, user_id1, lat1, lon1):
        with self.connect:
            self.cursor.execute("""
            UPDATE users SET pt=ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE tgid=(%s) ;
                """, (lon, lat, user_id))
            self.cursor.execute("""
                        UPDATE users SET pt=ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE tgid=(%s) ;
                            """, (lon1, lat1, user_id1))




