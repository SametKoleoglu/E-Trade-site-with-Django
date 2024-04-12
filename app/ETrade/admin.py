from django.contrib import admin

from . models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(TranslationAdmin):
    pass


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    pass


@admin.register(UseType)
class UseTypeAdmin(TranslationAdmin):
    pass


@admin.register(ProcessorModel)
class ProcessorModelAdmin(TranslationAdmin):
    pass


@admin.register(DiskQuantity)
class DiskQuantityAdmin(TranslationAdmin):
    pass


@admin.register(RamSize)
class RamSizeAdmin(TranslationAdmin):
    pass

@admin.register(ProductType)
class ProductTypeAdmin(TranslationAdmin):
    pass

