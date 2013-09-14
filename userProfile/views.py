from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.models import User
from django.template import RequestContext, loader

from post.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from userProfile.models import userProfile
from userProfile.forms import *
from django.contrib.auth.forms import PasswordChangeForm


#this obviously doesn't work... But it's a good base to work from.
### This Is the view for the user edit page.
@csrf_exempt
def edit(request):
    
    data = request.user
    profile = userProfile.objects.filter(user=data)[0]
    print(profile.bio)
    ## If loop true when user clicks the register button.
    if request.method == 'POST':
        #get data from the forms
        #form = PasswordChangeForm(data, request.POST)
        profileform = UserProfileForm(request.POST)
        pictureform = UserPictureForm(request.POST, request.FILES)
        #form.cleaned_data["user"]=data
        ## puts the users stuff in the database if its valid.
        if profileform.is_valid() and pictureform.is_valid():
            ###Create the user
            #data.username = form.cleaned_data["username"]
            #if form.cleaned_data["password"]:
                #data.password = form.cleaned_data["password"]###this is NOT how you set a password! Passwords are hashed.
            #    data.set_password(form.cleaned_data["password"])
            #    data.save()
            ###Create user's profile
            profile.bio = profileform.cleaned_data["bio"]
            #Create users picture.
            if pictureform.cleaned_data["filename"]:
                profile.filename=request.FILES["filename"]
            profile.save()
            if profile.filename=="stoopid":
                return render_to_response('editProfile.html', dict( user=request.user, msg="Your profile pic didn't work, unsupported or something. Don't worry though, you can use the cool default one I drew if you want. btw, don't click the submit button again."))
            return render_to_response('editProfile.html', dict( user=request.user, msg="success. btw, don't click the submit button again."))
        #returns form with error messages.
        else:
            return render_to_response('editProfile.html', dict( user=request.user, form2=profileform, form3=pictureform))
    
    ## Initializes the page with the forms.
    else:
        #form = PasswordChangeForm(data)
        profileform = UserProfileForm({'bio':profile.bio})
        pictureform = UserPictureForm({"filename":profile.filename})
        return render_to_response('editProfile.html', dict( user=request.user, form2=profileform, form3=pictureform))



def logout_user(request):
    logout(request)
    return redirect("/login")


def index(request, user):
    
    """bleh blebh bhel bleh, IM GOING INSANE.... I mean; user profile display stuff."""
    #I hate this vampire head ~alex
    """THE VAMPIRE HEAD FIXES ALL OF YOUR BROKEN CODE!!!, that is to say, as long as you never look at this code, it could be anything. We guarantee that whatever you imaging is better written then what actually is written."""
    userdata=User.objects.filter(username=user).get()
    
    posts=Post.objects.filter(author=userdata).order_by("-created") #'''~this needs to get the users posts.... not just you know, all the posts.... and now it does!'''

    #posts = Post.objects.all().order_by("-created")
    paginator = Paginator(posts, 3*3)


    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    #help(userposts)
    '''the correct answer was "print(userdata.get_profile().profilePicPath)"   '''  # <-- I have no idea what this means.
    print(userdata.profile.profilePicType)

#####		This fine code checks if the user has a renderable profile pic, and maybe gets the default one.
    if userdata.profile.profilePicType != "norender":
        from userProfile.models import userpicthumb
        usrpic = userdata.profile.filename.url
        thumbpic = userpicthumb.objects.get_or_create(fileobject = userdata.profile, filex = 128, filey = 128)[0]
        renderer = userdata.profile.profilePicType
    else:
        from filemanager.models import fileobject, thumbobject
        usrpic = fileobject.objects.exclude(filetype = "norender")[0]
        thumbpic =  thumbobject.objects.get_or_create(fileobject = usrpic, filex = 128, filey = 128)[0]
        renderer = usrpic.filetype
        usrpic = usrpic.filename.url

    c = RequestContext(request, dict(userPic = usrpic, userPicThumb = thumbpic.filename.url, renderer = renderer, usersname=user, bio=userdata.profile.bio, posts = posts))
    return render(request, "userProfile/index.html", c)


### This Is the view for the registration page.
@csrf_exempt
def register(request):
    
    ## If loop true when user clicks the register button.
    from django.contrib.auth.forms import UserCreationForm
    if request.method == 'POST':
        #get data from the forms
        form = UserCreationForm(request.POST)
        if form.is_valid():
            ###Create the user
            data = User();
            data.username = form.cleaned_data["username"]
           #data.password = form.cleaned_data["password"]###this is NOT how you set a password! Passwords are hashed.
            data.set_password(form.cleaned_data["password1"])
            data.save()
            ###Create user's profile
         #  profile = userProfile()
         #  profile.user = data
         #  profile.bio = profileform.cleaned_data["bio"]
         #  #Create users picture.
         #  try:
         #      profile.filename=request.FILES["filename"]
         #  except: "null"
         #  profile.save()
         #  if profile.filename=="stoopid":
         #      return render_to_response('register.html', dict( user=request.user, msg="Your profile pic didn't work, unsupported or something. Don't worry though, you can use the cool default one I drew if you want. btw, don't click the submit button again."))
            return render_to_response('register.html', dict( user=request.user, msg="success. btw, don't click the submit button again."))
        #returns form with error messages.
        else:
            return render_to_response('register.html', dict( user=request.user, form=form))
    
    ## Initializes the page with the forms.
    else:
        form = UserCreationForm()
        return render_to_response('register.html', dict( user=request.user, form=form))

### simple logout view, redirects users to the login page.
def logout_user(request):
    logout(request)
    return redirect("/login")

### Login page.
@csrf_exempt
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        usernamedata = request.POST.get('username')
        passworddata = request.POST.get('password')
        user = authenticate(username=usernamedata, password=passworddata)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're success'd the log in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username})
