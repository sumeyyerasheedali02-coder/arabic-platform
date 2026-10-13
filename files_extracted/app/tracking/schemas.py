from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas import ClassSection


class Request(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class CycleCreate(Request):
    academic_year: str = Field(pattern=r"^20\d{2}-20\d{2}$")
    section: ClassSection

    @model_validator(mode="after")
    def consecutive_years(self):
        first, last = map(int, self.academic_year.split("-"))
        if last != first + 1:
            raise ValueError("العام الدراسي يجب أن يتكون من سنتين متتاليتين")
        return self


class Mutation(Request):
    revision: int = Field(ge=0)


class WeekCreate(Mutation):
    number: int = Field(ge=1, le=52)
    starts_on: date


class GradeEntry(Request):
    student_id: int = Field(gt=0)
    writing: float | None = Field(None, ge=0, le=10)
    class_activity: float | None = Field(None, ge=0, le=10)
    home_activity: float | None = Field(None, ge=0, le=10)
    language_lab: float | None = Field(None, ge=0, le=10)
    note: str = Field("", max_length=2000)


class WeekSave(Mutation):
    entries: list[GradeEntry] = Field(max_length=2000)
    publish: bool = False


class Publication(Mutation):
    published: bool


class ExamEntry(Request):
    student_id: int = Field(gt=0)
    score: float | None = Field(None, ge=0, le=60)


class TermSave(Mutation):
    first_week: int = Field(ge=1, le=52)
    last_week: int = Field(ge=1, le=52)
    entries: list[ExamEntry] = Field(max_length=2000)
    publish: bool = False

    @model_validator(mode="after")
    def ordered_range(self):
        if self.last_week < self.first_week:
            raise ValueError("نهاية الفصل يجب ألا تسبق بدايته")
        return self
