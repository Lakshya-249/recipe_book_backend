from turtle import title
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from api.serializers import CategorySerializer, ChefSerializer, RecipeSerializer, ReviewSerializer, UserSerializer
from api.models import Category, Chef, Recipe, Review


# Create your views here.
class ChefView(viewsets.ReadOnlyModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer

    @action(detail=True,methods=['get'])
    def recipes(self,request,pk=None):
        try:
            chef = Chef.objects.get(pk=pk);
            recipes = Recipe.objects.filter(chef=chef)
            serializer = RecipeSerializer(recipes,many=True,context={'request':request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'message':'Chef not found'},status=404)
        
    @action(detail=False,methods=['get'],url_path="search-name")
    def search_name(self,request):
        try:
            name = request.query_params.get('name', None)
            if name is not None:
                chef = Chef.objects.filter(username=name)
                serializer = ChefSerializer(chef,many=True,context={'request':request})
                return Response(serializer.data)
            return Response({"message":"name field required but not given"},status=400)
        except Exception as e:
            return Response({'message':'An internal error occured'},status=404)
        
    @action(detail=False,methods=['get'],url_path="search-rname")
    def search_rname(self,request):
        name = request.query_params.get("name",None)
        if name is not None:
            chef = Chef.objects.filter(username=name)
            recipes = Recipe.objects.filter(chef=chef[0])
            serializer = RecipeSerializer(recipes,many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"message":"name field required but not given"},status=400)

class RegisterView(APIView):
    def post(self, request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            chefSerializer = ChefSerializer(data=request.data)
            if chefSerializer.is_valid():
                chefSerializer.save()
                nuser = Chef.objects.get(username=request.data['username'])
                nuser.password =  make_password(request.data['password'])
                nuser.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializers.data})
        return Response(serializers.errors,status=400)
    
class LoginView(APIView):
    def post(self, request):
        user = get_object_or_404(User, username = request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'message':'Invalid Credentials'},status=400)
        token,created = Token.objects.get_or_create(user=user)
        serilizer = UserSerializer(instance=user)
        return Response({"token": token.key,"user":serilizer.data })

class CreateRecipeView(generics.CreateAPIView,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

class RecipeView(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=True,methods=['get'])
    def reviews(self,request,pk=None):
        recipe = Recipe.objects.get(pk=pk);
        reviews = Review.objects.filter(recipe=recipe)
        serializer = ReviewSerializer(reviews,many=True,context={'request':request})
        return Response(serializer.data)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True,methods=['get'])
    def recipes(self,request,pk=None):
        category = Category.objects.get(pk=pk);
        recipes = Recipe.objects.filter(category=category)
        serializer = RecipeSerializer(recipes,many=True,context={'request':request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='search-cat')
    def search_cat(self, request):
        name = request.query_params.get('name', None)
        if name is not None:
            # print(name)
            cat = Category.objects.filter(name__icontains=name)
            serializer = CategorySerializer(cat, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"error": "Name parameter is required"}, status=400)
        
    @action(detail=False, methods=['get'], url_path='search-rcat')
    def search_rcat(self,request):
        name = request.query_params.get("name",None)
        if name is not None:
            category = Category.objects.filter(name=name)
            if(len(category) == 0 and name in ["Recent_Dishes","More_by_Online_Kitchen","Specials"]):
                nres = Recipe.objects.all().order_by('-recipe_id')[:6]
                serializer = RecipeSerializer(nres,many=True,context={'request':request})
                return Response(serializer.data,status=200)
            recipes = Recipe.objects.filter(category=category[0])
            serializer = RecipeSerializer(recipes,many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"message":"name field required but not given"},status=400)
    

class ReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]


class SearchApiView(APIView):
    def get(self,request):
        name = request.query_params.get('name',None)
        if name is not None:
            category = Category.objects.filter(name__startswith=name)
            if (len(category)!=0): 
                nserializer = CategorySerializer(category,many=True,context={'request':request})
                return Response(nserializer.data)
            recipes = Recipe.objects.filter(title__icontains=name)[:10]
            if (len(recipes)==0):
                return Response([{"title":"No Results"}],status=200)
            serializer = RecipeSerializer(recipes,many=True,context={'request':request})
            return Response(serializer.data)
        return Response({"message":"name field required but not given"},status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def testdata(request):
    return Response({'message':'Hello World'})