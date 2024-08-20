from django.contrib import admin
from .models import Taxonomy

class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_id', 'abundance_score', 'relative_abundance', 'unique_matches_frequency')
    
    list_filter = ('name', 'tax_id', 'abundance_score', 'relative_abundance', 'unique_matches_frequency')
    
    search_fields = ('name', 'tax_id')

admin.site.register(Taxonomy, TaxonomyAdmin)
