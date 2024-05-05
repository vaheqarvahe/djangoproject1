from .forms import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
import os
from email.mime.image import MIMEImage

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import stripe


@api_view(['POST'])
def sign_in(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"massage": "invalid info"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        token, check = Token.objects.get_or_create(user=user)
        print()
        return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_genre(request):
    genre = Genre.objects.all()
    print(genre)
    serializer = GenreSerializer(instance=genre, many=True)
    return Response({"genre": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_country(request):
    country = Country.objects.all()
    serializer = CountrySerializer(instance=country, many=True)
    return Response({"country": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_year(request):
    year = Year.objects.all()
    serializer = YearSerializer(instance=year, many=True)
    return Response({"year": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_translation(request):
    translation = Translation.objects.all()
    serializer = TranslationSerializer(instance=translation, many=True)
    return Response({"translation": serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_film(request):
    data = request.POST.copy()
    data["user"] = request.user.id
    form = FilmForm(data, request.FILES)
    if form.is_valid():
        form.save()
        return Response({"massage": "added"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_film(request):
    data = request.data.copy()
    data["user"] = request.user.id
    film_id = data.get('id')
    film_instance = Film.objects.get(id=film_id, user=request.user)
    form = FilmForm(data, request.FILES, instance=film_instance)
    if form.is_valid():
        form.save()
        return Response({"message": "Film updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    data = User.objects.get(id=request.user.id)
    serializer = UserSerial(data)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_film(request, pk):
    one_film = Film.objects.get(id=pk)
    serializer = FilmSerializer(instance=one_film)
    return Response({"film": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_film(request):
    all_film = Film.objects.all()
    serializer = FilmSerializer(instance=all_film, many=True)
    return Response({"films": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_search(request):
    text = request.GET.get('text')
    print(text)
    search = Film.objects.filter(name__icontains=text)
    serializer = FilmSerializer(instance=search, many=True)
    return Response({"film": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_by_genre(request):
    genre = request.GET.get("genre")
    print(genre)
    search = Film.objects.filter(genre=genre)
    serializer = FilmSerializer(instance=search, many=True)
    return Response({"film": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_film(request, pk):
    delete_film = Film.objects.get(id=pk)
    delete_film.delete()
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def sign_up(request):
    form = UserForm(request.data)
    if form.is_valid():
        print(form)
        form_info = form.save()  # {first_name: "pxooso"}
        form_info.is_active = False
        form_info.save()
        confirmation_token = default_token_generator.make_token(form_info)
        html_message = render_to_string("myapp/message.html",
                                        {
                                            'username1': request.data["username"],
                                            "user_id": form_info.id,
                                            "token": confirmation_token,
                                        })
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="sign up",
            body=plain_message,
            from_email=None,
            to=[request.data["email"]]
        )
        message.attach_alternative(html_message, "text/html")

        with (open(os.path.join(os.getcwd(), "static\\images\\netflix.jpg"), "rb")
              as img_file):
            image_data = img_file.read()
            image = MIMEImage(image_data)
            image.add_header('Content-ID', 'vazgen')
            message.attach(image)
        message.send()
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activate(request):
    user_id = request.GET.get('user_id')  # 36
    confirmation_token = request.GET.get('confirmation_token')  # 3645fas65d4f65
    user = User.objects.get(id=user_id)
    # print(default_token_generator.check_token(user, confirmation_token))
    if user is None:
        return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
    if not default_token_generator.check_token(user, confirmation_token):
        return Response(
            'Please request another confirmation email by signing in.', status=status.HTTP_400_BAD_REQUEST)
    user.is_active = True
    user.save()
    return Response({"message": 'Email successfully confirmed', "done": True}, status=status.HTTP_200_OK)


stripe.api_key = "sk_test_51P8jBVP5bKRaxDGPxEvFtCKkKltv2NrO00H0Dz45Bpgfb6Q9HWJgTUeZ60iLAvMLbrkzpN7jVymj1L7AplcGscD800U0yEpvqk"


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request, pk):
    film = Film.objects.get(id=pk)
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency="usd"
    )
    existing_payment = AcceptPayment.objects.filter(film=film, user=request.user).exists()
    print("barev", existing_payment)
    if existing_payment:
        return Response({"message": "Payment already exists for this film"}, status=status.HTTP_400_BAD_REQUEST)
    payment = AcceptPayment.objects.create(film=film, user=request.user)
    return Response({'client_secret': intent.client_secret, "payment.id": payment.id}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
