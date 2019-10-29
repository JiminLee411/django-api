from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Music, Artist, Review
from .serializers import MusicSerializers, ArtistSerializers, ArtistDetailSerializers, ReviewSerializers
# Create your views here.

@api_view(['GET'])  # HTTP method
def index(request):
    '''
    음악 목록 정보
    '''
    musics = Music.objects.all()
    serializer = MusicSerializers(musics, many=True) # many=True : QuerySet이여서 필요
    return Response(serializer.data)
    
@api_view(['GET'])
def detail(request, music_pk):
    '''
    음악 상세 정보
    '''
    music = get_object_or_404(Music, pk=music_pk)
    serializer = MusicSerializers(music) # 하나의 dictionary이므로 many=True 없어도 돼
    return Response(serializer.data)

# 아티스트 목록
@api_view(['GET'])
def artist_index(request):
    '''
    아티스트 목록 정보
    '''
    artists = Artist.objects.all()
    serializer = ArtistSerializers(artists, many=True)
    return Response(serializer.data)

# 아티스트 상세보기
@api_view(['GET'])
def artist_detail(request, artist_pk):
    '''
    아티스트 상세 정보
    '''
    artist = get_object_or_404(Artist, pk=artist_pk)
    serialize = ArtistDetailSerializers(artist)
    return Response(serialize.data)

# 리뷰 작성
@api_view(['POST'])
def review_create(request, music_pk):
    serializer = ReviewSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(music_id=music_pk)
    return Response({'message': 'review가 등록 되었습니다.'})

@api_view(['PUT', 'DELETE'])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':
        serializer = ReviewSerializers(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        review.delete()
        return Response({'message': '성공적으로 삭제되었습니다.'})