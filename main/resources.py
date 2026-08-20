from import_export import resources
from .models import Service

class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service
        fields = (
            'id', 'order', 'code', 'name',
            'price_bhyt', 'price_non_bhyt', 'description'
        )
        import_id_fields = ('id',)
