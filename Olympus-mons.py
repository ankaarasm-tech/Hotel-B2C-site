from nanodjango import Django
from django.db import models
from django import forms
from django.shortcuts import redirect
from datetime import date
from django.middleware.csrf import get_token
from django_ratelimit.decorators import ratelimit
from django.template import Template, Context
from django.http import HttpResponse


app = Django(
 INSTALLED_APPS=[
           'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.admin',  # <-- THIS WAS MISSING
    ],
 MIDDLEWARE=[
 'django.middleware.security.SecurityMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware',
 ]
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

@app.admin
class Users(models.Model):
 name = models.CharField(max_length=100)
 age = models.IntegerField()
 date = models.DateField(null=True, blank=True)
 email = models.EmailField(null=True, blank=True)
 dur = models.IntegerField(null=True, blank=True)
 def __str__(self):
  return self.name

class BookingForm(forms.ModelForm):
 class Meta:
  model = Users
  fields = ['name','age','date','email','dur']

 def clean_date(self):
  d = self.cleaned_data.get('date')
  if d and d < date.today():
   raise forms.ValidationError('Past date not allowed')
  return d
  
@app.route('/')
def index(request):
    token = get_token(request)
    html = '''
  <!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Olympus Hotel</title>
<style>
* {box-sizing: border-box;} html,body { margin: 0; padding: 0; overflow-x: hidden; }
body { display: flex; flex-direction: column; min-height: 100vh; font-family: sans-serif;}
h1 {font-size: clamp(75px, 8vw, 72px); font-family:cursive; text-align:center; color:#fff; margin: 0;}
header { background: dodgerblue; text-align: center; min-height: 40vh; padding:20px;}
.first-btn { display: block; width: 100%; max-width: 500px; margin: 10px auto; padding: 18px; text-align: center; text-decoration: none; font-weight: bold; border-radius: 8px; background: gold; color:#000; }
.services { display: flex; flex-wrap: wrap; gap: 25px; padding: 20px; justify-content: center; background: #fff; }
.service-card { width: 100%; max-width: 330px; min-height: 330px; background: #fff; border-radius: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.2); text-align: center; overflow: hidden; padding-bottom: 15px; }
.box { height: 230px; width: 100%; background: #eee; display: flex; align-items: center; justify-content: center; }
.reservations { display: flex; justify-content: center; padding: 20px; }
#form { background: #000; width: 100%; max-width: 400px; padding: 20px; border-radius: 10px; }
.reserve-title { font-family: serif; color: gold; font-size: 30px; text-align: center; }
output { color:gold; font-size: 20px;} output:after { content:".00"; }
input { padding: 15px; width: 100%; border-radius: 5px; border: 1px solid #333; }
span { color: gold; font-size:20px; }
#submit { width: 100%; padding: 15px; background: gold; border:none; border-radius: 5px; font-weight: bold; }
footer { color: #fff; background: #333; margin-top: auto; }
.footer-body { display: flex; flex-wrap: wrap; }
.footer-body > div { padding: 20px; }
.footer-body > div:first-child { flex: 1 1 200px; font-size: 150%; text-align: center; }
.footer-body > div:last-child { flex: 2 1 300px; }
.footer-body ul { list-style: none; margin: 0; padding: 0; text-align: center; }
.footer-body li > a { color: white; text-decoration: none; display: block; margin-bottom: 7px; }
.footer-copyright { width: 100%; background: #111; padding: 10px; text-align: center; color:gold; }
.msg { padding: 15px 18px; border-radius:50%; background: green; left:15px; bottom:20px; position: fixed; font-size: 22px; z-index: 99; }
.manager-link { color: #777!important; font-size: 12px; text-decoration: none; margin-left: 10px; border: 1px solid #444; padding: 4px 8px; border-radius: 4px;}
</style>
</head>
<body>
<header>
<header style="background: linear-gradient(rgba(30, 144, 255, 0.85), rgba(30, 144, 255, 0.85)), url('https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; text-align: center; min-height: 40vh; padding:40px 20px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
<h1 style="font-family: serif; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">Olympus Hotel</h1>
<p style="color: #fff; font-size: 18px; margin: 10px 0 25px 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Experience Luxury Above the Clouds</p>
<a href="/message" class="first-btn" style="max-width: 250px;">Message Us</a>
</header>

<main>
<div class="services">
<h2 style="width:100%; text-align:center;">Our Services Include</h2>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1517502884422-41eaead166d4?auto=format&fit=crop&w=600&q=80" alt="Conference Room" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>Our State of the Art Conference Rooms</p></div>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80" alt="Atlantic View" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>A Premium View of the Atlantic Ocean</p></div>
<div class="service-card"><div class="box">
  <img src="https://picsum.photos/id/1041/600/400" alt="Recreation site" style="width:100%; height:100%; object-fit:cover;">

</div><p>Wonderful Recreation for All Ages</p></div>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80" alt="food" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>And a Premium Cuisine made up of Local and International dishes</p></div>
</div>
<div class="reservations">
<form oninput="c.value=parseInt(a.value)*100" action="/reserve" method="POST" id="form">
<input type="hidden" name="csrfmiddlewaretoken" value="__TOKEN__">
<h2 class="reserve-title">Reservations</h2>
<input type="text" placeholder="Enter Name" required name="name"><br/><br/>
<input type="number" placeholder="Enter Age" min="18" required name="age"><br/><br/>
<input type="date" name="date" id="date-input"><br/><br/>
<input type="email" placeholder="Enter email" name="email" required><br/><br/>
<input type="number" placeholder="Enter Duration of Stay" required id="a" name="dur"><br/><br/>
<span>Cost: GH¢</span><output id="c">0</output><br/><br/>
<button type="submit" id="submit">Submit</button>
</form>
</div>
<a class="msg" href="https://wa.me/233541234567?text=Hello%20I%20want%20to%20book" style="text-decoration: none;">💬 </a>
</main>
<footer>
<div class="footer-body">
<div> Olympus-Mons Hotel</div>
<div>
<p> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis interdum dignissim nisl posuere efficitur. </p>
<ul>
<li><a href="#"> About </a></li>
<li><a href="#"> Contact </a></li>
<li><a href="#"> Terms & Conditions </a></li>
<li><a href="#"> Privacy Policy </a></li>
</ul>
</div>
</div>
<div class="footer-copyright">
© Ankaara Sankara Mwinwanma
<a href="/manager-login" class="manager-link">Manager Login</a>
</div>
</footer>
<script> const today = new Date().toISOString().split('T')[0]; document.getElementById('date-input').setAttribute('min',today); </script>
</body>
</html> 
      '''
    response = HttpResponse(html.replace('__TOKEN__',token))
    response['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; img-src 'self' data:;"
    return response

@app.route('/reserve')
@ratelimit(key='ip',rate='5/h',block=True)
def reserve(request):
    form = BookingForm(request.POST)
    if form.is_valid():
        form.save()
    return HttpResponse(''' 
     <!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Olympus Hotel</title>
<style>
* {box-sizing: border-box;} html,body { margin: 0; padding: 0; overflow-x: hidden; }
body { display: flex; flex-direction: column; min-height: 100vh; font-family: sans-serif;}
h1 {font-size: clamp(75px, 8vw, 72px); font-family:cursive; text-align:center; color:#fff; margin: 0;}
header { background: dodgerblue; text-align: center; min-height: 40vh; padding:20px;}
.first-btn { display: block; width: 100%; max-width: 500px; margin: 10px auto; padding: 18px; text-align: center; text-decoration: none; font-weight: bold; border-radius: 8px; background: gold; color:#000; }
.services { display: flex; flex-wrap: wrap; gap: 25px; padding: 20px; justify-content: center; background: #fff; }
.service-card { width: 100%; max-width: 330px; min-height: 330px; background: #fff; border-radius: 20px; box-shadow: 5px 5px 15px rgba(0,0,0,0.2); text-align: center; overflow: hidden; padding-bottom: 15px; }
.box { height: 230px; width: 100%; background: #eee; display: flex; align-items: center; justify-content: center; }
.reservations { display: flex; justify-content: center; padding: 20px; }
#form { background: #000; width: 100%; max-width: 400px; padding: 20px; border-radius: 10px; }
.reserve-title { font-family: serif; color: gold; font-size: 30px; text-align: center; }
output { color:gold; font-size: 20px;} output:after { content:".00"; }
input { padding: 15px; width: 100%; border-radius: 5px; border: 1px solid #333; }
span { color: gold; font-size:20px; }
#submit { width: 100%; padding: 15px; background: gold; border:none; border-radius: 5px; font-weight: bold; }
footer { color: #fff; background: #333; margin-top: auto; }
.footer-body { display: flex; flex-wrap: wrap; }
.footer-body > div { padding: 20px; }
.footer-body > div:first-child { flex: 1 1 200px; font-size: 150%; text-align: center; }
.footer-body > div:last-child { flex: 2 1 300px; }
.footer-body ul { list-style: none; margin: 0; padding: 0; text-align: center; }
.footer-body li > a { color: white; text-decoration: none; display: block; margin-bottom: 7px; }
.footer-copyright { width: 100%; background: #111; padding: 10px; text-align: center; color:gold; }
.msg { padding: 15px 18px; border-radius:50%; background: green; left:15px; bottom:20px; position: fixed; font-size: 22px; z-index: 99; }
.manager-link { color: #777!important; font-size: 12px; text-decoration: none; margin-left: 10px; border: 1px solid #444; padding: 4px 8px; border-radius: 4px;}
</style>
</head>
<body>
<header>
<header style="background: linear-gradient(rgba(30, 144, 255, 0.85), rgba(30, 144, 255, 0.85)), url('https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80'); background-size: cover; background-position: center; text-align: center; min-height: 40vh; padding:40px 20px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
<h1 style="font-family: serif; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">Olympus Hotel</h1>
<p style="color: #fff; font-size: 18px; margin: 10px 0 25px 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Experience Luxury Above the Clouds</p>
<a href="/message" class="first-btn" style="max-width: 250px;">Message Us</a>
</header>

<main>
<div class="services">
<h2 style="width:100%; text-align:center;">Our Services Include</h2>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1517502884422-41eaead166d4?auto=format&fit=crop&w=600&q=80" alt="Conference Room" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>Our State of the Art Conference Rooms</p></div>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80" alt="Atlantic View" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>A Premium View of the Atlantic Ocean</p></div>
<div class="service-card"><div class="box">
  <img src="https://picsum.photos/id/1041/600/400" alt="Recreation site" style="width:100%; height:100%; object-fit:cover;">

</div><p>Wonderful Recreation for All Ages</p></div>
<div class="service-card"><div class="box">
  <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80" alt="food" style="width:100%; height:100%; object-fit:cover;"/>
</div><p>And a Premium Cuisine made up of Local and International dishes</p></div>
</div>
<div class="reservations">
<form oninput="c.value=parseInt(a.value)*100" action="/reserve" method="POST" id="form">
<input type="hidden" name="csrfmiddlewaretoken" value="__TOKEN__">
<h2 class="reserve-title">Reservations</h2>
<input type="text" placeholder="Enter Name" required name="name"><br/><br/>
<input type="number" placeholder="Enter Age" min="18" required name="age"><br/><br/>
<input type="date" name="date" id="date-input"><br/><br/>
<input type="email" placeholder="Enter email" name="email" required><br/><br/>
<input type="number" placeholder="Enter Duration of Stay" required id="a" name="dur"><br/><br/>
<span>Cost: GH¢</span><output id="c">0</output><br/><br/>
<button type="submit" id="submit">Submit</button>
</form>
</div>
<a class="msg" href="https://wa.me/233541234567?text=Hello%20I%20want%20to%20book" style="text-decoration: none;">💬 </a>
</main>
<footer>
<div class="footer-body">
<div> Olympus-Mons Hotel</div>
<div>
<p> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis interdum dignissim nisl posuere efficitur. </p>
<ul>
<li><a href="#"> About </a></li>
<li><a href="#"> Contact </a></li>
<li><a href="#"> Terms & Conditions </a></li>
<li><a href="#"> Privacy Policy </a></li>
</ul>
</div>
</div>
<div class="footer-copyright">
© Ankaara Sankara Mwinwanma
<a href="/manager-login" class="manager-link">Manager Login</a>
</div>
</footer>
<script>

 const today = new Date().toISOString().split('T')[0]; document.getElementById('date-input').setAttribute('min',today); </script>
</body>
</html> 
    ''')
    return f"<h3>{form.errors.as_text()}</h3><a href='/'>Go Back</a>"


@app.route('/create-manager-once')
def create_manager(request):
    from django.contrib.auth.models import User
    from django.middleware.csrf import get_token
    token = get_token(request)
    
    if User.objects.filter(username='admin').exists():
        return HttpResponse("Admin already exists. <a href='/manager-login'>Login</a>")
    
    if request.method == 'POST':
        p1 = request.POST.get('password',)
        p2 = request.POST.get('confirm')
        if p1 != p2:
            return HttpResponse(f"<h2 style='color:red'>Passwords don't match!</h2><a href='/create-manager-once'>Try again</a>")
        if len(p1) < 4:
            return HttpResponse(f"<h2 style='color:red'>Too short!</h2><a href='/create-manager-once'>Try again</a>")
        User.objects.create_superuser('admin', 'admin@olympus.com', p1)
        return HttpResponse(f"Created! Username: admin | Password: {p1}<br><a href='/manager-login'>Login now</a>")
    
    return HttpResponse(f'''
    <form method="POST" style="background:#111; padding:30px; max-width:350px; margin:50px auto; border:1px solid gold; border-radius:15px;">
    <input type="hidden" name="csrfmiddlewaretoken" value="{token}">
    <h2 style="color:gold;">Create Manager</h2>
    <input name="password" type="password" placeholder="New Password" required style="width:100%; padding:10px; margin:5px 0;">
    <input name="confirm" type="password" placeholder="Confirm Password" required style="width:100%; padding:10px; margin:5px 0;">
    <button style="width:100%; padding:10px; background:gold; border:none; margin-top:10px; font-weight:bold;">Create</button>
    </form>
    ''')
    
@app.route('/reset-password')
def reset_password(request):
    from django.contrib.auth.models import User
    try:
        u = User.objects.get(username='admin')
        u.set_password('admin123')
        u.save()
        return HttpResponse("Password reset to admin123. <a href='/manager-login'>Login now</a>")
    except:
        return HttpResponse("No admin user found. Go to /create-manager-once first")

@app.route('/manager-login')
def manager_login(request):
    token = get_token(request)
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('/dashboard')
        return HttpResponse("""
        <!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Error Message</title>
  <style>
    body {background: #000;
    padding: 60px;}
  h1 {
    color:red;
    font-family:serif;
    text-align: center;
  }
  h2 {
    text-align: center;
  }
  </style>
</head>

<body>
  <h1>Wrong Password</h1>
<h2><a href="/manager-login">Try Again</a></h2>
</body>

</html>
        """)
    
    html = f'''
    <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#000; display:flex; justify-content:center; align-items:center; min-height:100vh; font-family:sans-serif;}}
    .card{{background:#111; padding:30px; border-radius:15px; width:100%; max-width:350px; border:1px solid gold;}}
    h2{{color:gold; text-align:center;}} input{{width:100%; padding:12px; margin:8px 0; border-radius:5px; border:1px solid #333;}}
    button{{width:100%; padding:12px; background:gold; border:none; border-radius:5px; font-weight:bold; cursor:pointer; margin-top:10px;}}
    </style></head><body>
    <form method="POST" class="card">
    <input type="hidden" name="csrfmiddlewaretoken" value="{token}">
    <h2>Manager Login</h2>
    <input name="username" placeholder="Username" required>
    <input name="password" type="password" placeholder="Password" required>
    <button>Login</button>
    <p style="color:#777; font-size:12px; text-align:center; margin-top:15px;">Olympus SaaS • Secure Access</p>
    </form></body></html>
    '''
    return HttpResponse(html)

@app.route('/dashboard')
@login_required(login_url='/manager-login')
def dashboard(request):
    bookings = Users.objects.all().order_by('-id')
    rows = "".join(f"<tr><td style='padding:10px; border-bottom:1px solid #333;'>{b.name}</td><td style='padding:10px; border-bottom:1px solid #333;'>{b.date}</td><td style='padding:10px; border-bottom:1px solid #333;'>{b.dur} days</td><td style='padding:10px; border-bottom:1px solid #333;'>{b.email}</td><td style='padding:10px; border-bottom:1px solid #333;'>GH¢{b.dur*100 if b.dur else 0}</td></tr>" for b in bookings)
    if not rows:
        rows = "<tr><td colspan=5 style='padding:20px; text-align:center; color:#777;'>No bookings yet</td></tr>"
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{{background:#0a0a0a; color:#fff; font-family:sans-serif; padding:20px;}}
    h1{{color:gold;}} table{{width:100%; background:#111; border-radius:10px; border-collapse:collapse; overflow:hidden;}}
    th{{background:gold; color:#000; padding:12px; text-align:left;}} a{{color:gold; text-decoration:none; border:1px solid gold; padding:6px 12px; border-radius:5px;}}
    .top{{display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:20px;}}
    </style></head><body>
    <div class="top"><h1>{bookings.count()} Bookings - Olympus</h1><div><a href="/">View Site</a> <a href="/logout" style="margin-left:10px;">Logout</a></div></div>
    <table><tr><th>Name</th><th>Date</th><th>Duration</th><th>Email</th><th>Revenue</th></tr>{rows}</table>
    <p style="margin-top:20px; color:#777;">Manager: {request.user.username} | Total Revenue: GH¢{sum((b.dur*100 if b.dur else 0) for b in bookings)}.00</p>
    </body></html>
    """)


if __name__ == "__main__":
    app.run()
    