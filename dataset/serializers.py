from rest_framework import serializers
from .models import DatasetResource

class ViewDatasetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DatasetResource
        fields = (
            'id', 'image', 'annotation_file', 'image_visualized_lines', 'image_visualized_words'
        )
