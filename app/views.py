from rest_framework.decorators import api_view, permission_classes
from .models import User, Ticket, FollowUp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ticketSerializer, followupSerializer

@api_view(['POST'])
def email_registration(request):
    try:
        email = request.data['email']
        password = request.data['password']
        name = request.data['name']
    except KeyError:
        return Response({"message": "please provide email and passsword"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        User.objects.get(email=email)
        return Response({"message": "already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        User.objects.create_user(email=email, password=password, name=name, dept='customer')
        return Response({"message": "registration successful"},  status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ticket(request):
    owner = request.user
    title = request.data['title']
    description = request.data['desc']
    tags = request.data['tags']
    stat = 'waiting'

    Ticket.objects.create(owner=owner, title=title, description=description, tags=tags, status=stat, department='Unassigned')

    return Response({"message": "success"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_tickets(request):
    owner = request.user
    tickets = Ticket.objects.filter(owner=owner)
    data = ticketSerializer(tickets, many=True).data

    return Response({"message": "success", "data": data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ticket(request, id):

    # find ticket
    ticket = Ticket.objects.get(id=id)
    followups = FollowUp.objects.filter(ticket=ticket)
    data = followupSerializer(followups, many=True).data
    response = {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "followups": data
    }

    return Response({"message": "success", "data": response}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_followup(request):
    ticket_id = request.data['ticket']
    ticket = Ticket.objects.get(id=ticket_id)
    author = request.user
    content = request.data['update']
    FollowUp.objects.create(author=author, ticket=ticket, content=content)

    return Response({"message": "success"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_dept(request):
    receiving = request.data['receiving']
    ticket_id = request.data['ticket']
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.department = receiving
    ticket.save()
    return Response({"message": "success"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_queries_by_dept(request):
    user = request.user
    tickets = Ticket.objects.filter(department=user.dept)
    data = ticketSerializer(tickets, many=True).data
    return Response({"message": "success", "data": data}, status=status.HTTP_200_OK)