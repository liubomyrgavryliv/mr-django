from django.contrib import admin
from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from api.models import *
from django.forms import TextInput, Textarea
from decimal import *
import re
from django.forms import ModelForm, BaseModelFormSet
from django.contrib.admin.filters import RelatedFieldListFilter
from django.forms import modelformset_factory

# Register your models here.
admin.site.register(MineralCountry)

class DropdownFilter(RelatedFieldListFilter):
    template = 'dropdown_filter.html'

class StatusListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'mineral status'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'status_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        status_list = []
        [status_list.append((status.status_id, '{} - {}'.format(status.status_id, status.description_short),)) for status in StatusList.objects.all()]
        return status_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(status__status_id=self.value())
        else:
            return queryset

class IonListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'ion'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'ion_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        ion_list = []
        [ion_list.append((ion.ion_id, '{} - {}'.format(ion.ion_id, ion.formula),)) for ion in IonList.objects.all()]
        return ion_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(ion_theoretical__ion_id=self.value())
        else:
            return queryset

class NsClassListFilter(admin.SimpleListFilter):
    title = 'NS class'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'id_class'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        statuses_list = []
        [statuses_list.append((status.status_id, '{} - {}'.format(status.status_id, status.description_short),)) for status in StatusList.objects.all()]
        return statuses_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(status__status_id=self.value())
        else:
            return queryset

class MineralStatusInline(admin.TabularInline):
    model = MineralStatus
    autocomplete_fields = ('status_id',)
    fields = ('status_id',)
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('status_id')
        return qs

class MineralIonTheoreticalForm(forms.ModelForm):
    anions = forms.ModelChoiceField(queryset=IonList.objects.filter(ion_type_id__ion_type_name__exact='Anion'))
    
    class Meta:
        model = IonList
        fields = ('ion_id',)


class MineralIonTheoreticalInline(admin.TabularInline):
    model = MineralIonTheoretical
    # form = MineralIonTheoreticalForm
    fields = ('ion_id',)
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('ion_id')
        return qs

class MineralImpurityInline(admin.TabularInline):
    model = MineralImpurity
    fields = ('ion_id', 'ion_quantity', 'rich_poor',)
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('ion_id')
        return qs

class MineralCountryInline(admin.TabularInline):
    model = MineralCountry
    autocomplete_fields = ('country_id',)
    fields = ('country_id','note',)
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         qs = qs.select_related('country_id', 'mineral_id')
#         return qs

class MineralRelationInline(admin.TabularInline):
    model = MineralRelation
    # model = MineralLog.relations.through
    raw_id_fields = ('relation_id',)
    # fields = ('relation_id', 'relation_type_id')
    ordering = ('relation_id__mineral_name',)
    fk_name = 'mineral_id'
    extra = 0
    # exclude = ('relation_id',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     qs = qs.select_related('mineral_id', 'relation_id', 'relation_type_id')
    #     # qs = qs.prefetch_related('mineral_id__relations')
    #     return qs

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # related = MineralLog.objects.select_related('relations')
    #     qs = qs.prefetch_related('mineral_relation')
    #     # fetched = qs.prefetch_related(Prefetch('relation_id', queryset=related))
    #     return qs

class MineralHistoryInline(admin.TabularInline):
    model = MineralHistory
    fields = ('discovery_year_min', 'discovery_year_max', 'discovery_year_note', 'first_usage_date', 'first_known_use',)
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

########## Names db tables ##########

class MineralNamePersonInline(admin.TabularInline):
    model = MineralNamePerson
    fields = ('person', 'born', 'died','role','gender','nationality_id')
    extra = 0

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('nationality_id')
        return qs

class MineralNameLanguageInline(admin.TabularInline):
    model = MineralNameLanguage
    fields = ('language_id', 'meaning', 'stem_1', 'stem_2', 'stem_3',)
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('language_id')
        return qs

class MineralNameInstitutionInline(admin.TabularInline):
    model = MineralNameInstitution
    fields = ('institution_name', 'note', 'country_id',)
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('country_id')
        return qs

def GrHierarchyInline(param):
    foreign_key = param
    class GroupInline(admin.TabularInline):
        model = GrHierarchy
        raw_id_fields = ('supergroup_id', 'group_id', 'subgroup_id','root_id', 'serie_id', 'mineral_id',)
        fk_name = foreign_key
        extra = 0
        verbose_name = 'hierarchy'
        verbose_name_plural = 'Groups'

    return GroupInline

@admin.register(MineralLog)
class MineralLogAdmin(admin.ModelAdmin):
    list_display = ('mineral_name', 'mineral_formula_html', 'get_statuses', 'get_ns_index',)
    list_filter = (StatusListFilter, 'id_class')
    ordering = ('mineral_name',)
    search_fields = ('mineral_name',)
    # list_select_related = ('id_class',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    def get_inline_instances(self, request, obj=None):
        print(obj)
        # status = obj.mineral_status.values_list('status_id', flat=True)
        # if Decimal('1.0') in status:
        #     fk_name = 'supergroup_id'
        # elif Decimal('1.1') in status:
        #     fk_name = 'group_id'
        # elif Decimal('1.2') in status:
        #     fk_name = 'subgroup_id'
        # elif Decimal('1.3') in status:
        #     fk_name = 'root_id'
        # elif Decimal('1.4') in status:
        #     fk_name = 'serie_id'
        # elif Decimal('0.0') in status:
        #     fk_name = 'mineral_id'
        # else:
        #     fk_name = 'mineral_id'
        # return [inline(self.model, self.admin_site) for inline in self.inlines]
        return  [
            MineralStatusInline(self.model, self.admin_site),
            MineralImpurityInline(self.model, self.admin_site),
            MineralIonTheoreticalInline(self.model, self.admin_site),
            MineralRelationInline(self.model, self.admin_site),
            MineralCountryInline(self.model, self.admin_site),
            MineralHistoryInline(self.model, self.admin_site),
            MineralNamePersonInline(self.model, self.admin_site),
            MineralNameLanguageInline(self.model, self.admin_site),
            MineralNameInstitutionInline(self.model, self.admin_site),
            # MsNamesPersonInline(self.model, self.admin_site),
            # MsNamesLanguageInline(self.model, self.admin_site),
            # GrHierarchyInline(fk_name)(self.model, self.admin_site), 
       ]

    # def get_form(self, request, obj=None, **kwargs):
    #     if obj:
    #         self.id_class = obj.id_class
    #     return super(MsSpeciesAdmin, self).get_form(request, obj, **kwargs)

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "id_subclass":
    #         kwargs["queryset"] = NsSubclass.objects.filter(id_class=self.id_class)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('id_class', 'id_subclass', 'id_family')
        queryset = queryset.prefetch_related('status')
        return queryset

@admin.register(StatusList)
class StatusListAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'description_short', 'description_long', 'description_group',)
    search_fields = ('status_id', 'description_short',)

@admin.register(NsClass)
class NsClassAdmin(admin.ModelAdmin):
    list_display = ('id_class', 'description',)
    ordering = ('id_class',)
    search_fields = ('id_class',)

@admin.register(NsSubclass)
class NsSubclassAdmin(admin.ModelAdmin):
    list_display = ('id_subclass', 'class_description', 'subclass_description',)
    ordering = ('id_class', 'id_subclass',)
    search_fields = ('id_subclass',)
    list_filter = ('id_class',)

    def class_description(self, obj):
        return obj.id_class.description

    def subclass_description(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('id_class')
        return queryset

@admin.register(NsFamily)
class NsFamilyAdmin(admin.ModelAdmin):
    list_display = ('id_family', 'class_description', 'subclass_description', 'family_description')
    ordering = ('id_class', 'id_subclass', 'id_family',)
    search_fields = ('id_family',)
    list_filter = ('id_class',)

    def class_description(self, obj):
        return obj.id_class.description

    def subclass_description(self, obj):
        return obj.id_subclass.description

    def family_description(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('id_class', 'id_subclass')
        return queryset

@admin.register(IonList)
class IonListAdmin(admin.ModelAdmin):
    list_display = ('ion_id', 'ion_type', 'ion_formula_html', 'variety_formula_html', 'ion_name', 'ion_class_id', 'ion_subclass_id', 'ion_group_id', 'ion_subgroup_id',)
    search_fields = ('formula',)
    ordering = ('ion_type_id',)
    list_filter = ('ion_type_id',('ion_class_id', DropdownFilter),('ion_subclass_id', DropdownFilter),('ion_group_id', DropdownFilter),('ion_subgroup_id', DropdownFilter),)
    # list_filter = ('ion_type_id','ion_class_id','ion_subclass_id', 'ion_group_id','ion_subgroup_id',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('ion_type_id', 'ion_class_id', 'ion_subclass_id', 'ion_group_id', 'ion_subgroup_id')
        return queryset

@admin.register(CountryList)
class CountryListAdmin(admin.ModelAdmin):
    list_display = ('country_id', 'country_name', 'alpha_2', 'alpha_3', 'country_code', 'region', 'sub_region', 'intermediate_region',)
    search_fields = ('country_name',)