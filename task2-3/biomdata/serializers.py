# myapp/serializers.py

from rest_framework import serializers

class TaxonomySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    tax_id = serializers.IntegerField()
    abundance_score = serializers.FloatField()
    relative_abundance = serializers.FloatField()
    unique_matches_frequency = serializers.IntegerField()

    def create(self, validated_data):
        return Taxonomy.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.tax_id = validated_data.get('tax_id', instance.tax_id)
        instance.abundance_score = validated_data.get('abundance_score', instance.abundance_score)
        instance.relative_abundance = validated_data.get('relative_abundance', instance.relative_abundance)
        instance.unique_matches_frequency = validated_data.get('unique_matches_frequency', instance.unique_matches_frequency)
        instance.save()
        return instance
