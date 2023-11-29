from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .forms import LoginForm, LogoutForm, ProfileSwitchForm, UploadForm, CommentForm
from .models import Video, Comment, Account
from .geo import get_ip, get_geo, get_location
import random, json, copy, re
import logging

# Create your views here.
database = {
    'profile': 'Default',
    #'ip': '127.0.0.1',
    #'location': 'N/A',
    'profile_data': [
        {
            'name': 'Science',
            'status': 'inactive',
        },
        {
            'name': 'Nature',
            'status': 'inactive',
        },
        # Add more video data as needed
    ],
    'video_data': [
        {
            'thumbnail_url': '0',
            'video_title': 'Test Video',
            'description': 'Test Description',
            'channel_name': 'Test Channel',
            'video_url': '0',
            'category': 'system',
        },
    ]
}

def shorten_description(description):
    if len(description) > 100:
        return description[:97] + "..."
    else:
        return description

def mark_active_profile(request, data):
    if request.session['authenticated'] == True:
        # Mark as authenticated for the template conditionals
        data['authenticated'] = True
        # Mark the active profile as active
        activeIdx = next((i for i, item in enumerate(data["profile_data"]) if item["name"] == request.session['profile']), None)
        # If no active profile has been selected, select the first one!
        if activeIdx is None:
            activeIdx = 0;
            request.session['profile'] = data["profile_data"][activeIdx]['name']   
        data["profile_data"][activeIdx]['status'] = 'active'
        data["profile"] = request.session['profile']

# Deduplicate code between index and watch by using a filter_recommendations function
def filter_recommendations(request, data, count):
    # Filter out any system videos
    data["video_data"] = list(filter(lambda video: video['category'] != 'system', data["video_data"]));
    
    if request.session['authenticated'] == True:
        # Filter out different categories
        data["video_data"] = list(filter(lambda video: video['category'] == request.session['profile'].lower(), data["video_data"]))
    
    # Randomize the order of video_data
    random.shuffle(data["video_data"])
    data["video_data"] = data["video_data"][:count]
    return data
    
def get_video_by_index(pk):
    try:
        # Retrieve the Video instance at the specified index
        video_instance = Video.objects.get(pk=pk)

        # Convert the Video instance to a dictionary
        video_data = {
            'thumbnail_url': video_instance.thumbnail,
            'video_title': video_instance.title,
            'description': video_instance.description,
            'channel_name': video_instance.channel,
            'video_url': video_instance.pk,
            'category': video_instance.genre,
        }

        return video_data

    except IndexError:
        # Handle the case where the specified index is out of range
        return None

def get_recommendations(query, genre, amount=10):
    # Start with all videos in the queryset
    matching_videos = Video.objects.all()

    # SINGLE WORD SEARCH
    # If query is provided, search in title and description
    #if query:
    #    matching_videos = matching_videos.filter(
    #        Q(title__icontains=query) | Q(description__icontains=query)
    #   )
    
    # MULTIQUERY OR-based SEARCH
    # If query is provided, split it into individual words and search in title and description
    if query:
        # Split the query into individual words
        query_words = re.findall(r'\b\w+\b', query)

        # Create a Q object with OR conditions for each word in title and description
        title_conditions = Q()
        description_conditions = Q()

        for word in query_words:
            title_conditions |= Q(title__icontains=word)
            description_conditions |= Q(description__icontains=word)

        # Apply the OR conditions to filter the matching videos
        matching_videos = matching_videos.filter(title_conditions | description_conditions)

    # If genre is provided, filter by genre
    if genre:
        matching_videos = matching_videos.filter(genre__icontains=genre)

    # Nothing was found?
    if matching_videos.count() == 0:
        return []
    # If the number of matching videos is less than the requested amount, return all matching videos
    elif matching_videos.count() <= amount:
        query_results = matching_videos
    else:
        # Retrieve a random sample of the specified size
        query_results = random.sample(list(matching_videos), amount)

    # Convert the queryset to an array of dictionaries
    random_videos_array = [
        {
            'thumbnail_url': str(video.thumbnail),
            'video_title': video.title,
            'description': video.description,
            'channel_name': video.channel,
            'video_url': video.pk,
            'category': video.genre,
        }
        for video in query_results
    ]
    # Just for aesthetic purposes, it gets boring to see the same results in same order over and over again!
    random.shuffle(random_videos_array)
    return random_videos_array

def index(request):
    if 'authenticated' not in request.session:
        request.session['authenticated'] = False
    if 'profile' not in request.session:
        request.session['profile'] = '';
    
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ProfileSwitchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Search for the given profile name and update its status
            request.session['profile'] = form.cleaned_data['profile'];
    
    # Grab an instance of the database for this user, so it's
    # as if the variable was declared in this function.
    data = copy.deepcopy(database)
    # Allow profile change
    mark_active_profile(request, data)
    
    # Obtain the active profile from the user's session
    if request.session['authenticated'] == True:
        genre = request.session['profile'].lower()
    else:
        genre = None
    # Grab 10 recommendations
    data['video_data'] = get_recommendations(None, genre, 10)
    
    # Geolocation data
    if request.session['authenticated'] == True:
        if 'ipv4' in request.session and 'geo' in request.session:
            data['ip'] = request.session['ipv4']
            data['location'] = get_location(request.session['geo'])
    
    return render(request, 'ytrecplus/home.htm', data)
    
def authenticate_user(username, passphrase):
    try:
        account = Account.objects.get(username=username, passphrase=passphrase)
        return True  # Authentication successful
    except Account.DoesNotExist:
        return False  # Authentication failed

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            if authenticate_user(form.cleaned_data['username'], form.cleaned_data['password']):
                request.session['authenticated'] = True;
                # Economize on API requests by only requesting upon login and caching results afterwards
                request.session['ipv4'] = get_ip()
                request.session['geo'] = get_geo(request.session['ipv4'])
                request.session['username'] = form.cleaned_data['username']
                return redirect(index)
            else:
                return HttpResponse("Wrong password")
        
        # try the logout form
        form = LogoutForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['authenticated'] = False;
            # redirect to a new URL:
            return redirect(index)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'ytrecplus/login.htm', {"form": form})
    
def create_video(thumbnail, title, description, channel, genre):
    # Create and save a new Comment instance
    new_video = Video(thumbnail=thumbnail, title=title, description=description, channel=channel, genre=genre)
    new_video.save()
    
def upload(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            create_video(0, form.cleaned_data['title'], form.cleaned_data['description'], form.cleaned_data['channel'], form.cleaned_data['category'])
            # redirect to a new URL:
        return redirect(index)

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.session['authenticated'] == False:
            return redirect(index)
        form = UploadForm(initial={'category':'science'})

    return render(request, 'ytrecplus/upload.htm', {"form": form})
    
def manage(request, param):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            video_instance = Video.objects.get(pk=param)
            video_instance.title = form.cleaned_data['title']
            video_instance.description = form.cleaned_data['description']
            video_instance.channel = form.cleaned_data['channel']
            video_instance.genre = form.cleaned_data['category']
            video_instance.save()
            # redirect to a new URL:
        return redirect(index)

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.session['authenticated'] == False:
            return redirect(index)
        video_instance = Video.objects.get(pk=param)
        form = UploadForm(initial={
            'title':video_instance.title,
            'description':video_instance.description,
            'channel':video_instance.channel,
            'category':video_instance.genre,
            })

    return render(request, 'ytrecplus/manage.htm', {"form": form})

def get_comments_for_video(video_id):
    # Retrieve all comments for the specified video ID, ordered by date in descending order
    comments = Comment.objects.filter(video=video_id).order_by('-date')

    # Convert the queryset to an array of dictionaries
    comments_list = [
        {
            'name': comment.name,
            'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string in desired format
            'text': comment.text,
        }
        for comment in comments
    ]

    return comments_list
    
def watch(request, param):
    if 'authenticated' not in request.session:
        request.session['authenticated'] = False
    if 'profile' not in request.session:
        request.session['profile'] = '';
    
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ProfileSwitchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Search for the given profile name and update its status
            request.session['profile'] = form.cleaned_data['profile'];
    
    # Grab an instance of the database for this user, so it's
    # as if the variable was declared in this function.
    data = copy.deepcopy(database)
    # Allow profile change
    mark_active_profile(request, data)
    
    # Obtain the active profile from the user's session
    if request.session['authenticated'] == True:
        genre = request.session['profile'].lower()
    else:
        genre = None
    # Grab 6 recommendations
    data['video_data'] = get_recommendations(None, genre, 6)
    
    # Current video data
    if param is None or param == '':
        param = 1
    data["current_video"] = get_video_by_index(param)
    
    data["current_video"]["comments"] = get_comments_for_video(param)
    
    if request.session['authenticated'] == True:
        data["username"] = request.session['username']
    
    return render(request, 'ytrecplus/watch.htm', data)
    
def search(request):
    if 'authenticated' not in request.session:
        request.session['authenticated'] = False
    if 'profile' not in request.session:
        request.session['profile'] = '';
    
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ProfileSwitchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # Search for the given profile name and update its status
            request.session['profile'] = form.cleaned_data['profile'];#
        # Redirect back to index since the POST request destroys the query string
        return redirect(index)
    
    query = request.GET.get('query', '')  # Retrieve the 'query' parameter from the GET parameters

    # Perform a case-insensitive search in video_title and description
    query = query.lower()  # Convert the query to lowercase for case-insensitive search
    
    # Obtain the active profile from the user's session
    if request.session['authenticated'] == True:
        genre = request.session['profile'].lower()
    else:
        genre = None
    # Grab 8 recommendations
    matching_entries = get_recommendations(query, genre, 8)

    # Prepare the context data to pass to the template
    # Grab an instance of the database for this user, so it's
    # as if the variable was declared in this function.
    data = copy.deepcopy(database)
    # Allow profile change
    mark_active_profile(request, data)
    
    # Add in the search results found earlier
    data['video_data'] = matching_entries
    
    for video in data['video_data']:
        video['description'] = shorten_description(video['description'])
    
    return render(request, 'ytrecplus/search.htm', data)
    
    
def create_comment(video, name, text):
    # Create and save a new Comment instance
    new_comment = Comment(video=video, name=name, text=text)
    new_comment.save()
    
def submit_comment(request):
    form = CommentForm(request.POST)

    # Only allow commenting for authenticated users
    if form.is_valid() and 'authenticated' in request.session:
        comment = form.cleaned_data['text']
        video = form.cleaned_data['video'] 
        create_comment(video, request.session['username'], comment)
        return JsonResponse({'success': True })
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)