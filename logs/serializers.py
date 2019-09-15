import bleach

from rest_framework import serializers


from .models import Page, Metric


class MetricSerializer(serializers.ModelSerializer):
    def save(self):
        self.validated_data['page'] = Page.objects.get(owner=self.context['request'].user, date=self.context['view'].kwargs['page_date'])
        return super().save()

    class Meta:
        model = Metric
        fields = ['id', 'name', 'value']


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    metric_set = MetricSerializer(many=True, read_only=True)

    def validate_content(self, data):
        return bleach.clean(data, tags=bleach.sanitizer.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'hr'], strip=True, strip_comments=True)

    class Meta:
        model = Page
        fields = ['id', 'owner', 'date', 'content', 'metric_set']
