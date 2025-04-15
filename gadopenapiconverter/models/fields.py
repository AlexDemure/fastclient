import pydantic

from gadopenapiconverter import const
from gadopenapiconverter import enums
from gadopenapiconverter import typings
from gadopenapiconverter.utils import codegeneration


class Field(pydantic.BaseModel):
    required: bool
    priority: int
    python: list[enums.PythonType] = pydantic.Field(default_factory=list)
    wrappers: list[enums.TypingType] = pydantic.Field(default_factory=list)
    datamodels: list[typings.Model] = pydantic.Field(default_factory=list)
    default: typings.Default | None = None

    @property
    def string(self) -> str:
        annotation = const.SYMBOL_COMMA.join(self.python + self.datamodels)

        if self.wrappers:
            for wrapper in self.wrappers:
                annotation = codegeneration.settyping(wrapper.wrapp(annotation))

        if self.default:
            return codegeneration.setdefault(annotation, self.default)
        elif not self.required:
            return codegeneration.setempty(annotation)

        return annotation
