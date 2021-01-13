from rest_framework import serializers
from Notes.models import Notes, Labels
from rest_framework.renderers import JSONRenderer

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete','owner_id']
        extra_kwargs = {'isDelete': {'read_only': True},'isArchive': {'read_only': True}, 'owner_id': {'read_only': True}}  

class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model= Labels
        fields=['name','owner']
        extra_kwargs = {'owner':{'read_only':True}}

class ArchiveNotesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isArchive','isDelete','owner_id']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True}, 'isDelete': {'read_only': True},'owner_id': {'read_only': True}}   

class TrashSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Notes
        fields=['title','content','isDelete','isArchive','owner_id']
        extra_kwargs = {'title': {'read_only': True},'content': {'read_only': True},'isArchive':{'read_only':True}, 'owner_id': {'read_only': True}}   


class AddLabelsToNoteSerializer(serializers.ModelSerializer):
    
    label =serializers.PrimaryKeyRelatedField(many=True, queryset=Labels.objects.all())
    class Meta:
        model = Notes
        fields=['title','content','label','owner']
        extra_kwargs = {'owner': {'read_only': True}, 'title': {'read_only': True}, 'content': {'read_only': True}}
