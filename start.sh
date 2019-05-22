echo "Cleaning up previous deployment"
rm -rf venv

echo "Activating virtual environment"
python3.6 -m venv venv
. venv/bin/activate

echo "Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

echo "Starting service"
python -m src.app &
