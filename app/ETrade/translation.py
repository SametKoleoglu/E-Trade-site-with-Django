from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('model', 'description')


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('brand',)


@register(Color)
class ColorTranslationOptions(TranslationOptions):
    fields = ('color',)


@register(UseType)
class UseTypeTranslationOptions(TranslationOptions):
    fields = ('use_type',)


@register(ProcessorModel)
class ProcessorModelTranslationOptions(TranslationOptions):
    fields = ('processor_model',)


@register(DiskQuantity)
class DiskQuantityTranslationOptions(TranslationOptions):
    fields = ('disk_quantity',)


@register(RamSize)
class RamSizeTranslationOptions(TranslationOptions):
    fields = ('ram_size',)
    
@register(ProductType)
class ProductTypeTranslationOptions(TranslationOptions):
    fields = ('product_type',)
