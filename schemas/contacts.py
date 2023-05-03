from pydantic import BaseModel
from typing import Optional, List
from models.contacts import Contact


class ContactSchema(BaseModel):
    """Define os parâmetros para criação de novo contato"""

    firstname: str = "Rainério"
    lastname: Optional[str] = "Costa"
    phone: str = "(96) 98100-0000"
    phone_type: str = "celular"
    email: Optional[str] = "email@example.com"


class UpdateContactSchema(BaseModel):
    """Define os parâmetros para criação de novo contato"""

    firstname: str = "Rainério Júnior"
    lastname: Optional[str] = "Costa"
    phone: str = "(96) 98100-1111"
    phone_type: str = "celular"
    email: Optional[str] = "email@example.com"

    class Config:
        orm_mode = True
        exclude_unset = True


class QueryParams(BaseModel):
    """Define o contact_id para route param"""

    contact_id: int


class ContactViewSchema(BaseModel):
    """Define como será retornado um contato com primeiro e ultimo nome"""

    id: int = 1
    name: str = "Rainério Costa"
    phone: str = "(96) 98855-2200"
    phone_type: str = "celular"
    email: Optional[str] = "email@email.com"


class ContactDeleteSchema(BaseModel):
    """Define como deve ser a estrutura de retorno após uma requisição de remoção"""

    message: str


class ListContactSchema(BaseModel):
    """Define os parâmetros para listagem de contatos"""

    contacts: List[ContactSchema]


def show_contacts(contacts: List[Contact]):
    """Retorna a representação dos contatos como definido em ContactViewSchema"""
    result = []
    for contact in contacts:
        result.append(
            {
                "id": contact.id,
                "name": contact.firstname + " " + contact.lastname,
                "phone": contact.phone,
                "phone_type": contact.phone_type,
                "email": contact.email,
            }
        )
    return {"contacts": result}


def show_contact(contact: Contact):
    """Retorna a representação de um contato como definido em ContactViewSchema"""
    return {
        "id": contact.id,
        "name": contact.firstname + " " + contact.lastname,
        "phone": contact.phone,
        "phone_type": contact.phone_type,
        "email": contact.email,
    }
