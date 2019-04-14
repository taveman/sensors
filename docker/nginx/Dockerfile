FROM nginx
MAINTAINER Yuiry

COPY --chown=nginx:nginx ["./controller_ssl.conf", "/etc/nginx/conf.d/"]
#RUN mkdir /etc/nginx/sites-enabled/ && chown nginx:nginx /etc/nginx/sites-enabled
#RUN ln -s /etc/nginx/sites-available/controller_ssl.conf /etc/nginx/sites-enabled/controller_ssl.conf

RUN mkdir /etc/nginx/ssl && chown nginx:nginx /etc/nginx/ssl
COPY --chown=nginx:nginx ["./controller_app.crt", "./controller_app.key", "/etc/nginx/ssl/"]
