# from rest_framework import serializers
# from posts.models import Post

# class PostListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'author', 'slug', 'content','publish',]

# class PostDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'author', 'title', 'slug', 'content','publish','draft']

# class PostCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'content','publish','draft']

from rest_framework import serializers
from posts.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class PostListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
        view_name = "api:detail",
        lookup_field = "slug",
        lookup_url_kwarg = "post_slug"
        )
    class Meta:
        model = Post
        fields = ['title', 'author', 'detail']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content','publish','draft']

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','author','title', 'slug', 'content','publish','draft', 'image', 'comments']

    def get_comments(self, obj):
        comment_queryset = Comment.objects.filter(object_pk=obj.id)
        comments = CommentListSerializer(comment_queryset, many=True).data
        return comments


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_type', 'object_pk','user','comment','submit_date']

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['object_pk','comment']



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data




from rest_framework_jwt.settings import api_settings

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate(self, data):
        user_obj = None

        username = data.get('username')
        password = data.get('password')

        if username == '':
            raise serializers.ValidationError("A username is required to login.")

        user = User.objects.filter(username=username)
        if user.exists():
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("This credentials, please try again.")

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        data["token"] = token
        return data