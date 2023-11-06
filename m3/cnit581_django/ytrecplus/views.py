from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import LoginForm, LogoutForm, ProfileSwitchForm, UploadForm
import random, json, copy

# Create your views here.
database = {
    'profile': 'Default',
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
        {
            'thumbnail_url': '1',
            'video_title': 'Madagascar - Mystical Island Paradise in the Indian Ocean | Free Documentary Nature',
            'description': 'Madagascar is a wondrous land, full of mythical secrets, strange cultures, and exotic nature. Its shadowy, damp virgin forests are filled with eerie sounds. The cry of the lemurs lures us into an enchanted world. It is no surprise that the native inhabitants developed an unusually spiritual relationship with nature, affected by animal legends, myths, taboos, and ancestor worship.',
            'channel_name': 'Free Documentary - Nature',
            'video_url': '1',
            'category': 'nature',
        },
        {
            'thumbnail_url': '2',
            'video_title': 'A Journey Through the Magical Wildlife of Chile | Full Documentary',
            'description': 'An intimate and classic journey through this wild country. We witness magical moments of nature, from a cougar mother playing tenderly with her cubs to the rare desert flowering, where different animals take advantage of the opportunity the flowers give them. From Vampire Bats to Blue Whales we see a small sample of the enormous natural beauty of this country.',
            'channel_name': 'Free High-Quality Documentaries',
            'video_url': '2',
            'category': 'nature',
        },
        {
            'thumbnail_url': '3',
            'video_title': 'Exploring The Underwater World | 4K UHD | Blue Planet II | BBC Earth',
            'description': 'This bold cinematic experience takes viewers on a magical adventure across the greatest, yet least known, parts of our planet our oceans. Since Blue Planet aired in 2001, our understanding of life beneath the waves has completely changed. Travelling from the icy polar seas to the vibrant blues of the coral atolls, this series shares these astonishing new discoveries. Meet the strange octopuses lurking in the depths of the Antarctic Ocean. Watch giant trevally fish leap to catch birds in mid-air. And ride on the back of a hammerhead shark as it attacks. Inspiring awe and wonder, Blue Planet II reveals surprising new places, charismatic new characters and extraordinary new behaviours.',
            'channel_name': 'BBC Earth',
            'video_url': '3',
            'category': 'nature',
        },
        {
            'thumbnail_url': '4',
            'video_title': 'Enter the Savage Kingdom: Ultimate Predators | Watch Now on Nat Geo WILD',
            'description': 'Ruthless predators and powerful prey are embroiled in rivalry, betrayal, and battle, in a never-ending crusade for survival, with characters so wild and ambitious and conflict so cutthroat, that no diction can do it justice. Each episode presents the battle from one character\'s point of view exposing the front lines of clan warfare from a mother\'s sacrifice to a father\'s rage at his own son.',
            'channel_name': 'Nat Geo WILD',
            'video_url': '4',
            'category': 'nature',
        },
        {
            'thumbnail_url': '5',
            'video_title': "Days of Summer - Nature's Peak Performance | Free Documentary Nature",
            'description': 'Long days, plenty of food, idleness, and la Dolce Vita for us, this is what summer is all about. But nature can\'t afford to take a holiday. On the contrary, the long hours of sunshine demand peak performance all around. Animals and plants must use these warm and heady days to grow and reproduce.',
            'channel_name': 'Free Documentary - Nature',
            'video_url': '5',
            'category': 'nature',
        },
        {
            'thumbnail_url': '6',
            'video_title': 'One Hour Of Your Favourite BBC Earth Moments | BBC Earth',
            'description': 'From hippos causing mayhem to three cheeky cheetahs, enjoy the moments of wonder that have captured the minds of the incredible BBC Earth community over the last year.',
            'channel_name': 'BBC Earth',
            'video_url': '6',
            'category': 'nature',
        },
        {
            'thumbnail_url': '7',
            'video_title': 'The Last Paradise on Earth - The Amazing Serengeti | Full Documentary',
            'description': 'The story of a lion and cheetah family who struggle to survive from climate change in the Serengeti. Two lions are born in the scorched dry season. Kali, the mother, as her milk dries out from starvation, desperately eats a dead hippo to feed her cubs. Moto, a solitary, male cheetah finds love with Nyota but when she disappears one day he searches the endless plains for her and makes a surprise discovery.',
            'channel_name': 'Free High-Quality Documentaries',
            'video_url': '7',
            'category': 'nature',
        },
        {
            'thumbnail_url': '8',
            'video_title': 'Wild Faces of Switzerland',
            'description': 'Marmots work hard all summer to feed incessantly and lay down enough fat reserves to pass the cold season in hibernation. But this is not to be confused with a refreshing night\'s sleep: far from it. This is more like a life-threatening emergency state. Scientists have found out that marmots repeatedly need to come round from their hibernation and have a proper sleep if they are to survive the hostile winter at all.',
            'channel_name': 'Free High-Quality Documentaries',
            'video_url': '8',
            'category': 'nature',
        },
        {
            'thumbnail_url': '9',
            'video_title': 'Wild Canada - The Wild West | Full Episode',
            'description': 'This episode features the region between the Western Canadian Pacific coastline and the Rocky Mountains - and it reveals the secrets of this lush land. The salmon run is one of our planet\'s greatest migrations. This sudden abundance of food attracts thousands of black bears. The mountain ranges further inland are the home of the Golden eagle. This bird can pick up double its bodyweight: in a dramatic sequence, a golden eagle grabs a dall sheep lamb and carries its prey away - for the benefit of its own chicks.',
            'channel_name': 'Free High-Quality Documentaries',
            'video_url': '9',
            'category': 'nature',
        },
        {
            'thumbnail_url': '10',
            'video_title': 'Gazelle [Animal Documentary]',
            'description': 'Following a herd of Thomson\'s gazelles, a species that uses swift, "life-saving legs" to survive attacks by predators on Africa\'s Serengeti Plains. Included: their flight from cheetahs (their "greatest enemy"), jackals and hyenas; how "Tommies" travel in herds.',
            'channel_name': 'Alpacaworld',
            'video_url': '10',
            'category': 'nature',
        },
        {
            'thumbnail_url': '11',
            'video_title': 'One Hour Of Mind-Blowing Mysteries Of The Atom | Full Documentary',
            'description': 'Have you ever found yourself pondering the mysteries of the atom? In this documentary, we\'re diving into some of the most thought-provoking questions that bridge the gap between the microscopic world of atoms and the expanse of the universe.',
            'channel_name': 'Big Scientific Questions',
            'video_url': '11',
            'category': 'science',
        },
        {
            'thumbnail_url': '12',
            'video_title': 'Exploring the Euclid Mission with Neil deGrasse Tyson and Jason Rhodes',
            'description': 'What are dark energy and dark matter? Neil deGrasse Tyson and Chuck Nice learn about the Euclid Mission and our latest efforts to uncover the secrets of The Dark Universe with JPL Researcher, Jason Rhodes.',
            'channel_name': 'StarTalk',
            'video_url': '12',
            'category': 'science',
        },
        {
            'thumbnail_url': '13',
            'video_title': 'What Happens If You Destroy A Black Hole?',
            'description': 'Black holes can destroy everything but can they be destroyed? What happens if we push physics to the absolute limits, maybe even break it and the universe in the process? Let\'s create a tiny black hole, about the mass of our moon, in the Kurzgesagt Labs and try to rip it apart',
            'channel_name': 'Kurzgesagt - In a Nutshell',
            'video_url': '13',
            'category': 'science',
        },
        {
            'thumbnail_url': '14',
            'video_title': 'Debunking Monty Hall problem fallacy',
            'description': 'I did a realistic simulation of Monty Hall problem and proved that switching choice never influences the outcome. In this simulation I acknowledge a very simple fact, that most of the "high IQ-ers" somehow always overlook. Any sane person will always change initial choice, if it was revealed to be a goat by the host. Therefore, first choice does not matter. It never influences the end outcome.',
            'channel_name': 'ScienceDiscoverer',
            'video_url': '14',
            'category': 'science',
        },
        {
            'thumbnail_url': '15',
            'video_title': 'Scientists Announce a Puzzling Discovery At The Large Hadron Collider',
            'description': 'The Higgs boson is considered to be the cornerstone of the Standard Model of particle physics. Its discovery in 2012 created ripples in the scientific community as it was the last missing piece of the Standard Model. However, the model is not the final word or the theory of everything. There are many things that it cannot explain, and for that, researchers at CERN are hunting for signs of new physics - and they might have got one!',
            'channel_name': 'The Secrets of the Universe',
            'video_url': '15',
            'category': 'science',
        },
        {
            'thumbnail_url': '16',
            'video_title': 'Not all scientific studies are created equal - David H. Schwartz',
            'description': 'Every day, we are bombarded by attention grabbing headlines that promise miracle cures to all of our ailments -- often backed up by a "scientific study." But what are these studies, and how do we know if they are reliable? David H. Schwartz dissects two types of studies that scientists use, illuminating why you should always approach the claims with a critical eye.',
            'channel_name': 'TED-Ed',
            'video_url': '16',
            'category': 'science',
        },
        {
            'thumbnail_url': '17',
            'video_title': 'Bad science: AI used to target kids with disinformation on YouTube - BBC World Service',
            'description': 'YouTube channels that use AI to make videos which include false science information are being recommended to children as “educational content”, the BBC’s Global Disinformation Team has found.  We identified over 50 channels in more than 20 languages using AI to create videos with pseudo-science or conspiracy theories. With millions of views in their channels, creators make money from placed ads.',
            'channel_name': 'BBC World Service',
            'video_url': '17',
            'category': 'science',
        },
        {
            'thumbnail_url': '18',
            'video_title': 'Have Scientists Achieved Fusion Technology?: Forbes Breaks Down The Breakthroughs 2023 May Offer',
            'description': 'Forbes Science Editor Alex Knapp joins "Forbes Talks" to discuss the scientific breakthroughs 2023 may bring us.',
            'channel_name': 'Forbes',
            'video_url': '18',
            'category': 'science',
        },
        {
            'thumbnail_url': '19',
            'video_title': 'Amazing Scientific Discoveries Made by Ordinary People',
            'description': 'Amazing scientific discoveries aren\'t always made by renowned scientists! Here\'s a few examples of times ordinary people unlocked some incredible discoveries! Let\'s check it out!',
            'channel_name': 'SciShow',
            'video_url': '19',
            'category': 'science',
        },
        {
            'thumbnail_url': '20',
            'video_title': '10 Unusual Recent Scientific Discoveries',
            'description': 'An exploration of 10 Unusual Recent Scientific Discoveries of interest.',
            'channel_name': 'John Michael Godier',
            'video_url': '20',
            'category': 'science',
        },
        # Add more video data as needed
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
    # Grab 10 recommendations
    data = filter_recommendations(request, data, 10)
    
    return render(request, 'ytrecplus/home.htm', data)

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
            if form.cleaned_data['username'] == 'user' and form.cleaned_data['password'] == '1234':
                request.session['authenticated'] = True;
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
    
def upload(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UploadForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            newvideo = {
                'thumbnail_url': '0',
                'video_title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'channel_name': form.cleaned_data['channel'],
                'video_url': len(database['video_data']),
                'category': form.cleaned_data['category'],
            }
            database['video_data'].append(newvideo)
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
            database['video_data'][param]['video_title'] = form.cleaned_data['title']
            database['video_data'][param]['description'] = form.cleaned_data['description']
            database['video_data'][param]['channel_name'] = form.cleaned_data['channel']
            database['video_data'][param]['category'] = form.cleaned_data['category']
            # redirect to a new URL:
        return redirect(index)

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.session['authenticated'] == False:
            return redirect(index)
        form = UploadForm(initial={
            'title':database['video_data'][param]['video_title'],
            'description':database['video_data'][param]['description'],
            'channel':database['video_data'][param]['channel_name'],
            'category':database['video_data'][param]['category'],
            })

    return render(request, 'ytrecplus/manage.htm', {"form": form})
    
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
    # Grab 6 recommendations
    data = filter_recommendations(request, data, 6)
    
    # Current video data
    if param is None or param == '':
        param = 1
    data["current_video"] = database["video_data"][param]
    
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

    # Filter video_data entries that contain the query in video_title or description
    matching_entries = [video for video in database['video_data'] if query in video['video_title'].lower() or query in video['description'].lower()]

    # Prepare the context data to pass to the template
    data = {
        'profile': copy.deepcopy(database['profile']),
        'profile_data': copy.deepcopy(database['profile_data']),
        'video_data': matching_entries,
    }
    # Allow profile change
    mark_active_profile(request, data)
    # Grab 6 recommendations
    data = filter_recommendations(request, data, 8)
    
    for video in data['video_data']:
        video['description'] = shorten_description(video['description'])
    
    return render(request, 'ytrecplus/search.htm', data)