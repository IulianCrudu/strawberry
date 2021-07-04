import pytest

import pydantic

import strawberry
from strawberry.types.types import TypeDefinition


@pytest.mark.parametrize(
    "pydantic_type, field_type",
    [
        (pydantic.ConstrainedInt, int),
        (pydantic.PositiveInt, int),
        (pydantic.NegativeInt, int),
        (pydantic.StrictInt, int),
        (pydantic.StrictStr, str),
        (pydantic.ConstrainedStr, str),
        (pydantic.SecretStr, str),
        (pydantic.StrictBool, bool),
        (pydantic.ConstrainedBytes, bytes),
        (pydantic.SecretBytes, bytes),
        (pydantic.EmailStr, str),
        (pydantic.AnyUrl, str),
        (pydantic.AnyHttpUrl, str),
        (pydantic.HttpUrl, str),
        (pydantic.PostgresDsn, str),
        (pydantic.RedisDsn, str),
    ],
)
def test_types(pydantic_type, field_type):
    class Model(pydantic.BaseModel):
        field: pydantic_type

    @strawberry.experimental.pydantic.type(Model, fields=["field"])
    class Type:
        pass

    definition: TypeDefinition = Type._type_definition

    assert definition.name == "Type"
    assert len(definition.fields) == 1

    assert definition.fields[0].python_name == "field"
    assert definition.fields[0].graphql_name is None
    assert definition.fields[0].type is field_type
    assert definition.fields[0].is_optional is False


@pytest.mark.parametrize(
    "pydantic_type, field_type",
    [(pydantic.NoneStr, str)],
)
def test_types_optional(pydantic_type, field_type):
    class Model(pydantic.BaseModel):
        field: pydantic_type

    @strawberry.experimental.pydantic.type(Model, fields=["field"])
    class Type:
        pass

    definition: TypeDefinition = Type._type_definition

    assert definition.name == "Type"
    assert len(definition.fields) == 1

    assert definition.fields[0].python_name == "field"
    assert definition.fields[0].graphql_name is None
    assert definition.fields[0].type is field_type
    assert definition.fields[0].is_optional is True


def test_conint():
    class Model(pydantic.BaseModel):
        field: pydantic.conint(lt=100)

    @strawberry.experimental.pydantic.type(Model, fields=["field"])
    class Type:
        pass

    definition: TypeDefinition = Type._type_definition

    assert definition.name == "Type"
    assert len(definition.fields) == 1

    assert definition.fields[0].python_name == "field"
    assert definition.fields[0].graphql_name is None
    assert definition.fields[0].type is int
    assert definition.fields[0].is_optional is False


def test_constr():
    class Model(pydantic.BaseModel):
        field: pydantic.constr(max_length=100)

    @strawberry.experimental.pydantic.type(Model, fields=["field"])
    class Type:
        pass

    definition: TypeDefinition = Type._type_definition

    assert definition.name == "Type"
    assert len(definition.fields) == 1

    assert definition.fields[0].python_name == "field"
    assert definition.fields[0].graphql_name is None
    assert definition.fields[0].type is str
    assert definition.fields[0].is_optional is False


@pytest.mark.parametrize(
    "pydantic_type",
    [
        pydantic.StrBytes,
        pydantic.NoneStrBytes,
        pydantic.PyObject,
        pydantic.FilePath,
        pydantic.DirectoryPath,
        pydantic.Json,
        pydantic.PaymentCardNumber,
        pydantic.ByteSize,
        # pydantic.ConstrainedList,
        # pydantic.ConstrainedSet,
        # pydantic.JsonWrapper,
    ],
)
def test_unsupported_types(pydantic_type):
    class Model(pydantic.BaseModel):
        field: pydantic_type

    with pytest.raises(
        strawberry.experimental.pydantic.exceptions.UnsupportedTypeError
    ):

        @strawberry.experimental.pydantic.type(Model, fields=["field"])
        class Type:
            pass
