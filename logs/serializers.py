from rest_framework import serializers


from .models import Page, Metric


class MetricSerializer(serializers.ModelSerializer):
    def save(self):
        self.validated_data['page'] = Page.objects.get(user=self.context['request'].user, code=self.context['view'].kwargs['page_code'])
        return super().save()

    class Meta:
        model = Metric
        fields = ['id', 'name', 'value']


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    metric_set = MetricSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'owner', 'date', 'content', 'metric_set']
