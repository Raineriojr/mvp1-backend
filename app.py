from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Info, Tag

from sqlalchemy.exc import IntegrityError

from models import Session, Contact
from logger import logger
from schemas import *
from flask_cors import CORS
from datetime import datetime

from schemas.contacts import ContactDeleteSchema

info = Info(
    title="API de contatos",
    description="API para MVP1 Eng. de Software",
    version="1.0.0",
)
app: Flask = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Status API", description="Retorna se API está ativa")
doc_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger",
)
contact_tag = Tag(
    name="Contatos", description="Adição, visualização e remoção de produtos da base"
)

@app.get("/", tags=[home_tag])
def index():
    """ "Retorna status da API"""
    return jsonify({"message": "Server running"})


@app.get("/doc", tags=[doc_tag])
def doc():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("openapi/swagger")


@app.get(
    "/api/contacts/list/all",
    tags=[contact_tag],
    responses={"200": ListContactSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def listAllContacts():
    """Lista todos os contatos registrados na base."""
    try:
        session = Session()

        contacts = (
            session.query(Contact)
            .group_by(Contact.firstname)
            .order_by(Contact.firstname.asc())
            .all()
        )

        if not contacts:
            return {"contacts": []}, 200
        else:
            return show_contacts(contacts), 200

    except Exception as e:
        logger.warning(f"Erro ao listar contatos: {e}")
        return {"error": f"Erro ao listar contatos: {e}"}, 400

    finally:
        session.close()
        

@app.post(
    "/api/contacts/create",
    tags=[contact_tag],
    responses={"200": ContactViewSchema, "404": ErrorSchema},
)
def createContact(body: ContactSchema):
    """Cadastra um novo contato"""
    try:
        contact_data = ContactSchema.parse_obj(request.get_json())
        contact = Contact(
            firstname=contact_data.firstname,
            lastname=contact_data.lastname,
            phone=contact_data.phone,
            phone_type=contact_data.phone_type,
            email=contact_data.email,
        )

        session = Session()

        session.add(contact)

        session.commit()

        return show_contact(contact), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao cadastrar novo contato: {e}")
        return {"IntegrityError": f"Erro ao cadastrar novo contato: {e}"}, 409

    except Exception as e:
        logger.warning(f"Erro ao cadastrar novo contato: {e}")
        return {"error": f"Erro ao cadastrar novo contato: {e}"}, 400
    

@app.put(
    "/api/contacts/<int:contact_id>/update",
    tags=[contact_tag],
    responses={"200": ContactSchema, "400": ErrorSchema},
)
def contactUpdate(path: QueryParams, body: ContactSchema):
    id_contact: int = request.view_args.get("contact_id")
    contact_data = ContactSchema.parse_obj(request.get_json())

    try:
        session = Session()

        with session.begin():
            contact: Contact = (
                session.query(Contact).filter(Contact.id == id_contact).first()
            )

            if not contact:
                logger.warning("Contato não existe na base.")
                return {"message": "Contato não existe na base."}, 404

            contact.firstname = contact_data.firstname
            contact.lastname = contact_data.lastname
            contact.phone = contact_data.phone
            contact.phone_type = contact_data.phone_type
            contact.email = contact_data.email
            contact.updated_at = datetime.now()

        session.commit()
        return (
            jsonify(**{"updated_at": contact.updated_at}, **show_contact(contact)),
            200,
        )

    except Exception as e:
        session.rollback()
        logger.warning(f"Falha ao alterar contato. {e}")
        return {"error": f"Falha ao alterar contato. {e}"}, 400

    finally:
        session.close()


@app.delete(
    "/api/contacts/<int:contact_id>/delete",
    tags=[contact_tag],
    responses={"200": ContactDeleteSchema, "400": ErrorSchema},
)
def deleteContact(path: QueryParams):
    contact_id: int = request.view_args.get("contact_id")

    try:
        session = Session()

        count = session.query(Contact).filter(Contact.id == contact_id).delete()

        session.commit()

        if count:
            return {"message": f"Contato removido - id: {contact_id}"}, 200
        else:
            logger.warning("Contato não existe na base")
            return {"message": "Contato não existe na base"}, 404

    except Exception as e:
        logger.warning(f"Falha ao deletar contato. {e}")
        return {"error": f"Falha ao deletar contato. {e}"}, 400

    finally:
        session.close()


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")