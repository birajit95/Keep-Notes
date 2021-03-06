from django.shortcuts import render
from Notes.serializers import NotesSerializer, LabelsSerializer, ArchiveNotesSerializer, TrashSerializer, AddLabelsToNoteSerializer,ListNotesSerializer, AddCollaboratorSerializer,ReminderSerializer
from Notes.permissions import IsOwner, IsCollaborator
from Notes.models import Notes, Labels
from authentication.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache
from rest_framework import status
import logging
from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger('django')

class CreateAndListNotes(generics.ListCreateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to create and get notes.
        --------
        Methods:
            get_queryset : User will get all the notes.
            perform_create : User will able to create new note.
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [success message and status code]
        """
        owner = self.request.user
        note = serializer.save(owner=owner)
        cache.set(str(owner)+"-notes-"+str(note.id), note)
        if cache.get(str(owner)+"-notes-"+str(note.id)):
            logger.info("Data is stored in cache")
        return Response({'success':'New note is created!!'}, status=status.HTTP_201_CREATED)
    
    def get_queryset(self): 
        """
            Args:
            Returns:
                [queryset]: [unique notes list for owner or collaborator]
        """
        owner = self.request.user
        return self.queryset.filter(Q(owner=owner)|Q(collaborator=owner), Q(isArchive=False,isDelete=False)).distinct()   
                          

class NoteDetails(generics.RetrieveUpdateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get or update note.
        --------
        Methods:
            get_queryset : User will get the note by id.
            perform_update : User will able to update note.
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsCollaborator)
    lookup_field="id"

    def perform_update(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [serialized note data and status code]
        """
        owner = self.request.user
        note = serializer.save()
        cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated note data is set")
        return Response({'response': note}, status=status.HTTP_200_OK)

    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [owned or shared note fetched by given id]
        """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated note data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(isDelete=False)
            logger.info("updated note data is coming form DB")
            if queryset:
                cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
            

class DeleteNote(generics.RetrieveDestroyAPIView):
    """
        Summary:
        --------
            This class will let authorized user to delete note.
        --------
        Methods:
            perform_destroy : User will able to delete fetched note.
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)
    lookup_field="id"

    def perform_destroy(self, instance):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [success message and status code]
        """
        owner = self.request.user
        cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        instance.delete()
        return Response({'response': 'Note is deleted permanently.'}, status=status.HTTP_204_NO_CONTENT)


class CreateAndListLabels(generics.ListCreateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to create and get labels.
        --------
        Methods:
            get_queryset : User will get all the labels.
            perform_create : User will able to create new label.
    """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [success message and status code]
        """
        owner = self.request.user
        label = serializer.save(owner=owner)
        cache.set(str(owner)+"-labels-"+str(label.id), label)
        if cache.get(str(owner)+"-labels-"+str(label.id)):
            logger.info("Label data is stored in cache")
        return Response({'success':'New label is created!!'}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [list of labels owned by user]
        """
        owner = self.request.user
        return self.queryset.filter(owner=owner)
        

class LabelDetails(generics.RetrieveUpdateDestroyAPIView):
    """
        Summary:
        --------
            This class will let authorized user to retrieve, update and delete label.
        --------
        Methods:
            get_queryset : User will get label by id.
            perform_update : User will able to update label.
            perform_destroy : User will able to delete label.
    """
    serializer_class = LabelsSerializer
    queryset = Labels.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_update(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [serialized label data and status code]
        """
        owner = self.request.user
        label = serializer.save(owner=owner)
        cache.set(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated label data is set")
        return Response({'response':label}, status=status.HTTP_200_OK)
    
    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [label fetched by given id and owned by user]
        """
        owner = self.request.user
        if cache.get(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated label data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(owner=owner)
            logger.info("updated label data is coming form DB")
            if queryset:
                cache.set(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset

    def perform_destroy(self, instance):
        """
            Args:
                instance : [fetched label object by id ]

            Returns:
                [Response]: [success message and status code]
        """
        owner = self.request.user
        cache.delete(str(owner)+"-labels-"+str(self.kwargs[self.lookup_field]))
        instance.delete()
        return Response({'response': 'Label is deleted.'}, status=status.HTTP_204_NO_CONTENT)


class ArchiveNote(generics.RetrieveUpdateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to archive note.
        --------
        Methods:
            get_queryset : User will get note by id.
            perform_update : User will able to update archive field value of fetched note.
    """
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [note owned by user is fetched with given id]
        """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated archive notes data is coming from cache")
            return queryset
        else:
            queryset = self.queryset.filter(isDelete=False, id=self.kwargs[self.lookup_field])
            logger.info("updated archive note data is coming form DB")
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
 
    def perform_update(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [serialized data of updated note and status code]
        """
        owner = self.request.user
        note = serializer.save(owner=owner)
        cache.set(str(owner)+"-notes-"+str(note.id), self.queryset.all())
        logger.info("udated archive note data is set")
        return Response({'response':note}, status=status.HTTP_200_OK)
    

class ArchiveNotesList(generics.ListAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get all archived notes.
        --------
        Methods:
            get_queryset : User will get all note with archive field value as true.   
    """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class = ArchiveNotesSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [archive note list owned by user]
        """
        owner = self.request.user
        return self.queryset.filter(Q(owner=owner),isArchive=True, isDelete=False)
        

class TrashUntrash(generics.RetrieveUpdateAPIView):
    """
        Summary:
        --------
            This class will let authorized user to move note to trash.
        --------
        Methods:
            get_queryset : User will get note by id.
            perform_update : User will able to update isDelete field value of fetched note.
    """
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field="id"

    def perform_update(self,serializer):
        """
            Args:
                serializer : [object of serializer_class to serailize note object]

            Returns:
                [Response]: [serialized data of updated note and status code]
        """
        owner = self.request.user
        if serializer.validated_data['isDelete']==True:
            note = serializer.save(owner=owner, trashedAt=datetime.now())
        else:
            note = serializer.save(owner=owner, trashedAt=None)
        if note.isDelete==True:
            cache.delete(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
        else:
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), self.queryset.all())
        logger.info("udated trashed note data is set")
        return Response({'response':note}, status=status.HTTP_200_OK)
        

    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [owned note by user is fetched with given id]
        """
        owner = self.request.user
        if cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field])):
            queryset = cache.get(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]))
            logger.info("udated trashed note data is coming from cache")
            return queryset

        else:
            queryset = self.queryset.filter(id=self.kwargs[self.lookup_field])
            logger.info("updated trashed note data is coming form DB")
            cache.set(str(owner)+"-notes-"+str(self.kwargs[self.lookup_field]), queryset)
            return queryset
        

class TrashList(generics.ListAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get all trashed notes.
        --------
        Methods:
            get_queryset : User will get all note with isDelete field value as true.   
    """
    permission_classes=(permissions.IsAuthenticated, IsOwner)
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    
    def get_queryset(self):
        """
            Args:
            Returns:
                [queryset]: [trashed note list owned by user]
        """
        owner = self.request.user
        return self.queryset.filter(Q(owner=owner), isDelete=True)
        

class AddLabelsToNote(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to add label to the note.
        --------
        Methods:
            get: User will get the note by id.
            put: This method allows to add labels to fetched note.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddLabelsToNoteSerializer

    def put(self, request, note_id):
        """
            Args:
                note_id : [id of note provided in url]

            Returns:
                [Response]: [added label name and status code]
        """
        try:
            note = Notes.objects.get(Q(id = note_id), Q(owner=self.request.user)|Q(collaborator=self.request.user))
        except Notes.DoesNotExist:
            return Response({'response':'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        label_name = serializer.validated_data['label']
        try:
            label = Labels.objects.get(name=label_name, owner=self.request.user)
        except Labels.DoesNotExist:
            label = Labels.objects.create(name=label_name, owner=self.request.user)
        note.label.add(label.id)
        note.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request, note_id):
        """
            Args:
                note_id : [id of note provided in url] 
            Returns:
                [Response]: [serialized data of fetched note and status code]
        """
        note = Notes.objects.filter(Q(owner=self.request.user)|Q(collaborator=self.request.user),isDelete=False,id=note_id)
        if note:
            serializer = ListNotesSerializer(note,many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)


class ListNotesInLabel(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to get all notes with same label.
        --------
        Methods:
            get_queryset : User will get all note same label id given.   
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListNotesSerializer

    def get(self,request,label_id):
        """
            Args:
            Returns:
                [queryset]: [note list with a label given id and owned by user]
        """
        try:
            notes = Labels.objects.get(id=label_id,owner=self.request.user).notes_set.all()
        except:
            return Response({'response':'This label does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if notes:
            serializer = ListNotesSerializer(notes,many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'No notes with this label'}, status=status.HTTP_200_OK)

class SearchNote(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to search notes by title or content.
        --------
        Methods:
            get_queryset : It returns the notes having search query parameters.
            get: It returns the serailized notes list.
    """
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = NotesSerializer    
    token_param_config = openapi.Parameter('search',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    
    def get_queryset(self, queryset=None):
        """
            Args:
                queryset : [search query parameter]
            Returns:
                [note]: [fetched notes containing given search query]
        """
        notes = []
        owner = self.request.user
        if queryset:                
            searchlist = queryset.split(' ')
            for query in searchlist:
                if cache.get(query):
                    notes = cache.get(query)
                    logger.info("data is coming from cache")
                else:
                    notes = Notes.objects.filter(Q(title__icontains=query)|Q(content__icontains=query), Q(isArchive=False,isDelete=False),Q(owner=owner)|Q(collaborator=owner))
                    if notes:
                        cache.set(query, notes)  
        return notes

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        """
            Args:
                request : 
            Returns:
                [Response]: [serialized data of fetched notes and status code]
        """
        queryset = request.GET.get('search')
        if queryset:
            note = self.get_queryset(queryset)
        else:
            return Response({'response':'Give some search string!!!'})
        serializer = NotesSerializer(note, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCollaborator(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to add collaborators to a note.
        --------
        Methods:
            get: It returns the serailized note.
            put : It allows to add collaborators email in collaborator field of note.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = AddCollaboratorSerializer

    def put(self, request ,note_id):
        """
            Args:
                note_id : [id of note provided in url]

            Returns:
                [Response]: [added collaborator email and status code]
        """
        try:
            note = Notes.objects.get(Q(owner=self.request.user)|Q(collaborator=self.request.user),isDelete=False,id=note_id)
        except:
            return Response({'response':'note does not exist!!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        collaborator_email = serializer.validated_data['collaborator']
        try:
            collaborator = User.objects.get(email=collaborator_email)
        except:
            return Response({'This user email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if collaborator==request.user:
            return Response({'Detail': 'This email already exists!!!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note.collaborator.add(collaborator.id)
            note.save()
            return Response({'collaborator':collaborator_email}, status=status.HTTP_200_OK)


    def get(self,request, note_id):
        """
            Args:
                note_id : [id of note provided in url] 
            Returns:
                [Response]: [serialized data of fetched note and status code]
        """
        note = Notes.objects.filter(Q(owner=self.request.user)|Q(collaborator=self.request.user),isDelete=False,id=note_id)
        if note:
            serializer = ListNotesSerializer(note,many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)

class Reminder(generics.GenericAPIView):
    """
        Summary:
        --------
            This class will let authorized user to add reminder to a note.
        --------
        Methods:
            get_queryset : It returns the queryset of note by given id.
            get: It returns the serailized note.
            put : It allows to add reminder for fetched note if the data is valid.
    """
    serializer_class = ReminderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self, note_id, note=None):
        """
            Args:
                note_id : [unique id used to retrieve note]

            Returns:
                [queryset]: [note object with given id]
        """    
        return Notes.objects.get(Q(owner=self.request.user)|Q(collaborator=self.request.user),isDelete=False,id=note_id)
        
    def put(self,request, note_id):
        """
            Args:
                note_id : [id of note provided in url]

            Returns:
                [Response]: [serialized reminder data set to note and status code]
        """
        try:
            note = self.get_queryset(note_id)
        except:
            return Response({'response':'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reminder = serializer.validated_data['reminder']
        if reminder.replace(tzinfo=None) - datetime.now() < timedelta(seconds=0):
            return Response({'response':'Invalid Time Given'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note.reminder = reminder
            note.save()
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)

    def get(self,request, note_id):
        """
            Args:
                note_id : [id of note provided in url] 
            Returns:
                [Response]: [serialized data of fetched note and status code]
        """
        note = Notes.objects.filter(Q(owner=self.request.user)|Q(collaborator=self.request.user),isDelete=False,id=note_id)
        if note:
            serializer = ListNotesSerializer(note,many=True)
            return Response({'response':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, note_id):
        """
            Args:
                note_id : [id of note provided in url] 
            Returns:
                [Response]: [delete message and status code]
        """
        try:
            note = self.get_queryset(note_id)
        except:
            return Response({'response':'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if note.reminder is None:
            return Response({'response':'Reminder is not set'})
        else:
            note.reminder = None
            note.save()
            return Response({'response':'Reminder is removed'}, status=status.HTTP_200_OK)
        





        