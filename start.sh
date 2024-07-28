# Check if virtual environment folder exists
if [ ! -d "env" ]; then
    # Create virtual environment
    python3 -m venv env
fi

# Activate virtual environment
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

cd src

# Migrate database
python manage.py makemigrations
python manage.py migrate

# Run the Django server
python manage.py runserver

# Deactivate virtual environment
deactivate

cd ..