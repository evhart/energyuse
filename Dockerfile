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

RUN apk add --no-cache bash pv build-base mariadb mariadb-client mariadb-dev zlib zlib-dev jpeg jpeg-dev nodejs nodejs-npm && ln -s /lib/libz.so /usr/lib/

# Configure DB
RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql \
    && mkdir -p /run/mysqld && chown mysql:mysql /run/mysqld \
    && /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 \
    && mysqladmin -u root password "XXpABFgap2yZWKtm"

RUN /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 \
    && echo "CREATE USER 'energyuse'@'localhost' IDENTIFIED BY 'wG4bbnKSV7Y4ue9d';" > /tmp/sql \
    && echo "CREATE DATABASE energyuse DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;" >> /tmp/sql \
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


# Load backup if a backup directory is specified (a context directory with media backup and sql.gz file):
#  docker build -t evhart/energyuse:latest --build-arg BACKUP=./backup . (the directory needs to be in the context)
ARG BACKUP=""
RUN if [ "$BACKUP" = "" ] ; then  \
            /bin/echo -e "\033[1;31mNo backup provided.\033[0m" ; \
        else \
            /bin/echo -e "\033[1;32mBackup directory provided: ${BACKUP}.\033[0m" ; \
            source energyuse/settings.env ; \
            /usr/bin/mysqld_safe --syslog --nowatch && sleep 5 ; \
            mysql -u 'root' --password="XXpABFgap2yZWKtm" -e "DROP DATABASE energyuse; CREATE DATABASE energyuse DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;" ; \
            mysql -u 'root' --password="XXpABFgap2yZWKtm" -e "SET global net_buffer_length=1048576; SET global max_allowed_packet=1073741824; SET foreign_key_checks = 0" ; \ 
            count=`ls -l ${BACKUP}/*.sql.gz | grep -v ^l | wc -l` ; \
            c_count=0 ; \
            for filename in ${BACKUP}/*.sql.gz; do \
                [ -e "${filename#/}" ] || continue ; \
                c_count=$((c_count+1)) ; \
                /bin/echo -e "\033[1;32m (${c_count}/${count}) Processing: ${filename#/}.\033[0m" ; \
                /usr/bin/pv -f ${filename#/} | gunzip | mysql -u 'root' --password="XXpABFgap2yZWKtm" -D energyuse ; \
            done ; \
            mkdir -p ./live/export/media && cp -r ${BACKUP}/media/* ./live/export/media ; \
            rm -R $BACKUP ; \  
            mysql -u 'root' --password="XXpABFgap2yZWKtm" -e "SET foreign_key_checks = 1" ; \           
    fi

EXPOSE 8000
CMD ["sh","-c","/usr/bin/mysqld_safe --syslog --nowatch && sleep 5 && source energyuse/settings.env && gunicorn energyuse.wsgi -b 0.0.0.0:8000"]
