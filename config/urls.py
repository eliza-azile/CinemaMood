from django.contrib import admin
from django.urls import path
from django.http import JsonResponse, HttpResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy', 
        'service': 'CinemaMood',
        'version': '1.0.0',
        'message': 'Server is running correctly'
    })

def home(request):
    return HttpResponse('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>CinemaMood - Movie Recommendation Service</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                h1 { color: #2c3e50; margin-bottom: 20px; }
                .container { max-width: 800px; margin: 0 auto; }
                .btn { display: inline-block; margin: 15px; padding: 15px 30px; 
                       background: #3498db; color: white; text-decoration: none; 
                       border-radius: 8px; font-size: 18px; font-weight: bold; }
                .btn:hover { background: #2980b9; transform: translateY(-2px); }
                .status { background: #2ecc71; color: white; padding: 10px; 
                          border-radius: 5px; margin: 20px auto; width: 200px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 CinemaMood</h1>
                <p style="font-size: 20px; color: #555;">
                    Movie recommendation service based on mood analysis
                </p>
                
                <div class="status">
                    ✅ System Status: OPERATIONAL
                </div>
                
                <div style="margin: 40px 0;">
                    <a href="/health/" class="btn">🔧 System Health Check</a><br>
                    <a href="/admin/" class="btn">⚙️ Admin Panel</a><br>
                    <a href="/catalog/" class="btn">📺 Movie Catalog</a>
                </div>
                
                <p style="margin-top: 40px; color: #777;">
                    Successfully deployed on <strong>Render.com</strong> | 
                    <a href="https://github.com/eliza-azile/CinemaMood" style="color: #3498db;">
                        View on GitHub
                    </a>
                </p>
            </div>
        </body>
        </html>
    ''')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', home, name='home'),
]
