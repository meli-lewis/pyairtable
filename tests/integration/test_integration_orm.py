import pytest
import os
from pyairtable.orm import Model
from pyairtable.orm import fields as f


BASE_ID = "appaPqizdsNHDvlEm"


@pytest.fixture
def Address():
    class _Address(Model):
        street = f.TextField("Street")

        class Meta:
            base_id = BASE_ID
            api_key = os.environ["AIRTABLE_API_KEY"]
            table_name = "Address"

    yield _Address

    table = _Address.get_table()
    records = table.all()
    table.batch_delete([r["id"] for r in records])


@pytest.fixture
def Contact(Address):
    class _Contact(Model):
        first_name = f.TextField("First Name")
        last_name = f.TextField("Last Name")
        email = f.EmailField("Email")
        is_registered = f.CheckboxField("Registered")
        address = f.LinkField("Address", Address, lazy=True)
        birthday = f.DatetimeField("Birthday")

        class Meta:
            base_id = BASE_ID
            api_key = os.environ["AIRTABLE_API_KEY"]
            table_name = "Contact"

    yield _Contact

    table = _Contact.get_table()
    records = table.all()
    table.batch_delete([r["id"] for r in records])


@pytest.mark.integration
def test_integration_orm(Contact, Address):
    STREET = "123 Han"
    address = Address(street=STREET)
    address.save()

    contact = Contact(
        first_name="John",
        last_name="LastName",
        email="email@email.com",
        is_registered=True,
        address=[address],
    )

    assert contact.first_name == "John"
    assert contact.save()
    assert contact.id

    contact.first_name = "Not Gui"
    assert not contact.save()

    rv_address = contact.address[0]
    assert rv_address.exists()

    assert rv_address.id == contact.address[0].id == address.id
    rv_address.fetch()
    assert rv_address.street == contact.address[0].street == STREET
