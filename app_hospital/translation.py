from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name',)

@register(Specialty)
class SpecialtyTranslationOptions(TranslationOptions):
    fields = ('specialty_name',)

@register(MedicalAdvice)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('diagnosis', 'treatment', 'medication')