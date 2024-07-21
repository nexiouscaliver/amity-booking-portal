sudo apt update
sudo apt install python3-pip python3-dev nginx -y
sudo pip3 install virtualenv
rm -rf AmityApp
mkdir AmityApp && cd AmityApp
virtualenv env
source env/bin/activate
pip3 install flask gunicorn
pip3 -r install requirements.txt
git clone https://github.com/nexiouscaliver/amity-booking-portal.git
cd amity-booking-portal
mv amiity-booking-portal/* .
rm -rf amity-booking-portal
python initapp.py
gunicorn --bind 0.0.0.0:8000 wsgi:app
# sudo cp amity-booking-portal.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl start amity-booking-portal
# sudo systemctl enable amity-booking-portal
# sudo cp amity-booking-portal /etc/nginx/sites-available/
# sudo ln -s /etc/nginx/sites-available/amity-booking-portal /etc/nginx/sites-enabled
# sudo chmod 775 -R /home/myFlaskApp
# sudo systemctl restart nginx
