import logging

import psycopg2
from django.conf import settings

from .models import Person


def get_person_by_iin(iin: str):
    try:
        person = Person.objects.filter(iin=iin).first()
        if person is not None:
            return person
        with psycopg2.connect(
            host=settings.FR_DB_HOST,
            database=settings.FR_DB_NAME,
            user=settings.FR_DB_USER,
            password=settings.FR_DB_PASSWORD,
            port=settings.FR_DB_PORT,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT 
                           gr_code,
                           ud_code,
                           firstname,
                           secondname, 
                           lastname
                       FROM fr.unique_ud_gr WHERE gr_code=%(iin)s ORDER BY id LIMIT 1""",
                    {"iin": iin},
                )
                result = cursor.fetchone()
                if result:
                    iin, id_number, first_name, middle_name, last_name = result
                    person = Person.objects.create(
                        iin=iin,
                        id_number=id_number,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                    )
                    return person
                return None
    except Exception as e:
        logging.error(f"get_person_by_iin error: {str(e)}")
        return None
