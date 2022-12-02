FROM nginx

# Do this apt/pip stuff all in one RUN command to avoid creating large
# intermediate layers on non-squashable docker installs
RUN apt update && \
    apt install -y python python-dev libffi6 libffi-dev libssl-dev curl build-essential gettext-base && \
    curl -L 'https://bootstrap.pypa.io/get-pip.py' | python && \
    pip install -U cffi certbot && \
    apt remove --purge -y python-dev build-essential libffi-dev libssl-dev curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy in default nginx configuration (which just forwards ACME requests to
# certbot, or redirects to HTTPS, but has no HTTPS configurations by default).
RUN rm -f /etc/nginx/conf.d/*


COPY ./config/nginx/app.conf /etc/nginx/conf.d/default.conf

# making more dynamic
# COPY ./config/nginx/template.conf /etc/nginx/conf.d/template.conf
# CMD ["/bin/bash", "-c", "envsubst '$$NGINX_HOST'< /etc/nginx/conf.d/template.conf > /etc/nginx/conf.d/default.conf"]