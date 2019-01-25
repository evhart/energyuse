#
# Dockerfile for deploying the Energyuse platform.
#
FROM python:2.7-alpine3.7 
LABEL maintainer="Grégoire Burel <evhart@users.noreply.github.com>"

# Set user environment:
ENV NB_USER energyuse
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

# Add user:
RUN adduser -D \
    -g "Default user" \
    -u ${NB_UID} \
    ${NB_USER}

WORKDIR /home/energyuse

RUN apk add --no-cache bash build-base mariadb mariadb-client mariadb-dev zlib zlib-dev jpeg jpeg-dev nodejs nodejs-npm && ln -s /lib/libz.so /usr/lib/
# RUN apk add --no-cache bash build-base postgresql postgresql-client postgresql-dev zlib zlib-dev jpeg jpeg-dev nodejs nodejs-npm && ln -s /lib/libz.so /usr/lib/

# Configure DB
RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql \
    && mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld \
    && /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 \
    && mysqladmin -u root password "XXpABFgap2yZWKtm"

RUN /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 \
    && echo "CREATE USER 'energyuse'@'localhost' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d';" > /tmp/sql \
    && echo "CREATE DATABASE energyuse;" >> /tmp/sql \
    && echo "GRANT ALL ON *.* TO 'energyuse'@'0.0.0.0' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d' WITH GRANT OPTION;" >> /tmp/sql \
    && echo "GRANT ALL ON *.* TO 'energyuse'@'127.0.0.1' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d' WITH GRANT OPTION;" >> /tmp/sql \
    && echo "GRANT ALL ON *.* TO 'energyuse'@'localhost' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d' WITH GRANT OPTION;" >> /tmp/sql \
    && echo "GRANT ALL ON *.* TO 'energyuse'@'::1' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d' WITH GRANT OPTION;" >> /tmp/sql \
    && echo "DELETE FROM mysql.user WHERE User='';" >> /tmp/sql \
    && echo "DROP DATABASE test;" >> /tmp/sql \
    && echo "FLUSH PRIVILEGES;" >> /tmp/sql \
    && cat /tmp/sql | mysql -u root --password="XXpABFgap2yZWKtm" \
    && rm /tmp/sql 

# # Install the requirements:
COPY requirements.txt /home/energyuse/requirements.txt
RUN pip install --no-cache -r requirements.txt

# # Install lessc:
RUN npm install less -g

# Copy files:
COPY . /home/${NB_USER}

# # Initialise server and DB:
RUN /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 \
    && source energyuse/settings.env \
    && python manage.py syncdb --noinput \
    && python manage.py loaddata fixtures/flatpages.json \
    && python manage.py collectstatic --noinput \
    && python manage.py compress 


EXPOSE 8000

# RUN gunicorn -b 0.0.0.0:8000 energyuse.wsgi
CMD ["sh","-c","/usr/bin/mysqld_safe --syslog --nowatch && source energyuse/settings.env && gunicorn energyuse.wsgi -b 0.0.0.0:8000"]
