from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Table
from .serializers import TableSerializer

# Web Views
@login_required
def table_list_view(request):
    tables = Table.objects.all()
    return render(request, 'tables/table_list.html', {'tables': tables})

@login_required
def update_table_status_view(request, pk, new_status):
    table = get_object_or_404(Table, pk=pk)
    if new_status in [choice[0] for choice in Table.Status.choices]:
        table.status = new_status
        table.save()
        messages.success(request, f"Table #{table.number} status updated to {table.get_status_display()}.")
    else:
        messages.error(request, "Invalid status choice.")
    return redirect('table_list')

# REST API ViewSet
class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def occupy(self, request, pk=None):
        table = self.get_object()
        table.mark_occupied()
        return Response({'status': 'Table marked as OCCUPIED', 'table': TableSerializer(table).data})

    @action(detail=True, methods=['post'])
    def reserve(self, request, pk=None):
        table = self.get_object()
        table.mark_reserved()
        return Response({'status': 'Table marked as RESERVED', 'table': TableSerializer(table).data})

    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        table = self.get_object()
        table.mark_available()
        return Response({'status': 'Table marked as AVAILABLE', 'table': TableSerializer(table).data})
