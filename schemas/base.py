from pydantic import model_validator
from sqlmodel import SQLModel
import re

from main.schemas import exceptions

class Base(SQLModel):
    @model_validator(mode='after')
    def check_passwords_match(self):

        for k, v in self.__dict__.items():

            if v:

                # XSS attacks against
                if type(v) == str:
                    x = re.search(r'''(\b)(on\S+)(\s*)=|javascript|<(|\/|[^\/>][^>]+|\/[^>][^>]+)>''', v)
                    if x:
                        raise exceptions.Value_XSSHacked('XSS Hacked')
                    
                # validate email
                if k == 'email':
                    x = re.search(r'''^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$''', v)
                    if not x:
                        raise exceptions.Value_InvalidEmail('Value invalid email address')
                    
        return self
