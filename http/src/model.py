import enum
from typing import Any, Dict, Iterable, List, Optional, Union

from pydantic import BaseModel
from pydantic.main import create_model


class SupportedTypes(str, enum.Enum):
    VERSION = "version"
    MOLFILE = "molfile"
    SMILES = "smiles"
    SMARTS = "smarts"
    MOLFILE_LIST = "molfile_list"
    SMILES_LIST = "smiles_list"
    SMARTS_LIST = "smarts_list"
    REACTION = "reaction"
    QUERY_REACTION = "query_reaction"
    GROSSFORMULA = "gross_formula"
    COMMON_BITS = "common_bits"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


def create_types(types: Iterable[SupportedTypes]):
    return enum.Enum("Types", {t.name: t.value for t in types})


class AttributesModel(BaseModel):
    content: str


class DataBaseModel(BaseModel):
    type: Optional[SupportedTypes] = None

    @classmethod
    def with_types(cls, types: Iterable[SupportedTypes]):
        """
        Generates data model with `type` field restricted to specific types from SupportedTypes
        """

        TypesEnum = create_types(types)
        fields = {"type": (Optional[TypesEnum], None)}

        return create_model("DataModel", __base__=cls, **fields)


class DataModel(DataBaseModel):
    attributes: AttributesModel


class ReactionProductEnumerateAttributes(BaseModel):
    reaction: str
    monomers_table: List[List[str]]


class StructurePropsAttributes(AttributesModel):
    props: Optional[str] = None


class MolPairAttributes(BaseModel):
    mol1: str
    mol2: str


class AmbiguousHAttributes(BaseModel):
    molecule: Optional[str] = None
    reaction: Optional[str] = None


class StructurePropsDataModel(DataBaseModel):
    attributes: StructurePropsAttributes


class ReactionProductEnumerateDataModel(DataBaseModel):
    attributes: ReactionProductEnumerateAttributes


class MolPairDataModel(DataBaseModel):
    attributes: MolPairAttributes


class AmbiguousHDataModel(DataBaseModel):
    attributes: AmbiguousHAttributes


class IndigoBaseRequest(BaseModel):
    """
    base request model
    """

    data: DataModel

    @classmethod
    def with_types(cls, types: Iterable[SupportedTypes]):
        """
        Generates request model with `data.type` field restricted to specific types from SupportedTypes
        """

        DataModelClass = cls.__fields__.get("data").type_
        fields = {"data": (DataModelClass.with_types(types), ...)}

        return create_model("IndigoRequest", __base__=cls, **fields)


class IndigoReactionProductEnumerateRequest(IndigoBaseRequest):
    """
    request model for:
    - POST /reactionProductEnumerate
    """

    data: ReactionProductEnumerateDataModel


class IndigoStructurePropsRequest(IndigoBaseRequest):
    """
    request model for:
    - POST /nameToStructure
    - POST /checkStructure
    """

    data: StructurePropsDataModel


class IndigoMolPairRequest(IndigoBaseRequest):
    """
    request model for:
    - POST /commonBits
    - POST /exactMatch
    """

    data: MolPairDataModel


class IndigoAmbiguousHRequest(IndigoBaseRequest):
    """
    request model for:
    - POST /checkAmbiguousH
    """

    data: AmbiguousHDataModel


class Error(BaseModel):
    status: Optional[int] = None
    detail: Optional[str] = None


class ResponseAttributesModel(BaseModel):
    result: Any


class ResponseDataModel(DataBaseModel):
    type: Optional[SupportedTypes] = None
    attributes: Union[ResponseAttributesModel, List[ResponseAttributesModel]]


class IndigoBaseResponse(BaseModel):
    meta: Optional[Dict] = None
    errors: Optional[List[Error]] = None


class IndigoResponse(IndigoBaseResponse):
    data: Optional[ResponseDataModel] = None
