# Vivaan Farmhouse - Quick Setup Script
# Run this script to set up the project automatically

Write-Host "=== Vivaan Farmhouse - Setup Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "[1/6] Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "[1/6] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created!" -ForegroundColor Green
}

Write-Host "[2/6] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "[3/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host "[4/6] Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host "[5/6] Populating dummy data..." -ForegroundColor Yellow
python manage.py populate_data

Write-Host "[6/6] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Create admin user: python manage.py createsuperuser" -ForegroundColor White
Write-Host "2. Run server: python manage.py runserver" -ForegroundColor White
Write-Host "3. Visit: http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "4. Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
