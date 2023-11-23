import graphene
from graphene_django import DjangoObjectType 
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from .models import *
from .serializers import UserCreateSerializer , UserUpdateSerializer
from graphene_django.types import ErrorType
from graphql_jwt.decorators import login_required , superuser_required
import graphql_jwt 


class UserType(DjangoObjectType):
    '''
    User Model
    '''
    class Meta:
        model = User
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)
        fields = '__all__'

class UserConnection(graphene.relay.Connection):

    class Meta:
        node = UserType

class Query(graphene.ObjectType):
    viewer = graphene.Field(UserType)
    all_users = graphene.relay.ConnectionField(UserConnection)
    # user_by_id = DjangoFilterConnectionField(UserType)
    user_by_id = graphene.Field(UserType,id=graphene.ID(required=True))

    @login_required
    def resolve_viewer(self, info, **kwargs):
        return info.context.user
    
    @superuser_required
    def resolve_user_by_id(self,info , **kwargs):
        id = kwargs.get('id',)    
        try:
            return User.objects.get(id=id)
        except: 
            return None
    
    @superuser_required
    def resolve_all_users(self,info, **kwargs):
        return User.objects.all()

class CreateUserMutation(SerializerMutation):
    class Meta:
        model = User
        serializer_class = UserCreateSerializer
        model_operations = ['create',]
        lookup_field = 'id'
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if info.context.user.is_authenticated:
            raise ValueError('Not Allowed')
        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)

        if serializer.is_valid():
            return cls.perform_mutate(serializer, info)
        else:
            errors = ErrorType.from_errors(serializer.errors)
            return cls(errors=errors)  

class UpdateUserMutation(SerializerMutation):
    id = graphene.ID(required = True)

    class Meta:
        model = User
        serializer_class = UserUpdateSerializer
        model_operations = ['update',]
        lookup_field = 'id'

    @classmethod
    @login_required
    def get_serializer_kwargs(cls, root, info, **input):
        if 'id' in input:
            if not info.context.user.is_superuser:
                raise ValueError(f'Not Allowed, {input["id"]} , {info.context.user.id}')
            elif info.context.user.is_superuser:
                try:
                    instance = User.objects.get(id=input['id'])
                except User.DoesNotExist:
                    raise ValueError('Invalid ID')
        else:
            instance = info.context.user
        return {'instance': instance, 'data': input, 'partial': True}

class DeleteUserMutation(graphene.Mutation):
    ok = graphene.Boolean()
    errors = graphene.List(ErrorType)

    @classmethod
    def mutate(cls,root,info):
        try:
            user = info.context.user
            user.delete()
            return cls(ok=True)
        except Exception as e:
            print(e)
            return cls(ok=False)

class CustomJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)


    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(graphene.ObjectType):
    create_user_mutation = CreateUserMutation.Field()
    update_user_mutation = UpdateUserMutation.Field()
    delete_user_mutation = DeleteUserMutation.Field()
    token_auth = CustomJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    

schema = graphene.Schema(query=Query,mutation=Mutation)