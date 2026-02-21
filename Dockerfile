FROM nginx:alpine

# Metadata
LABEL maintainer="Morphology Atlas Project"
LABEL description="Interactive web application for morphological terminology"

# Copy all project files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY data /usr/share/nginx/html/data
COPY images /usr/share/nginx/html/images
COPY assets /usr/share/nginx/html/assets

# Create default nginx configuration
RUN echo 'server { \
    listen 80; \
    server_name localhost; \
    root /usr/share/nginx/html; \
    index index.html; \
    gzip on; \
    gzip_vary on; \
    gzip_comp_level 6; \
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
    location ~* \\.json$ { \
        add_header Content-Type application/json; \
        add_header Access-Control-Allow-Origin *; \
    } \
    location ~* \\.(png|jpg|jpeg|gif|ico|svg)$ { \
        expires 30d; \
        add_header Cache-Control "public, immutable"; \
    } \
    location ~* \\.(css|js)$ { \
        expires 7d; \
        add_header Cache-Control "public"; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
