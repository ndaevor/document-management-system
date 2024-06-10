from haystack import indexes
from .models import Document

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    file = indexes.CharField(model_attr='file')
    user_id = indexes.IntegerField(model_attr='user__id')

    def get_model(self):
        return Document

    def prepare_text(self, obj):
        return f"{obj.file.name} {obj.user.id}"
