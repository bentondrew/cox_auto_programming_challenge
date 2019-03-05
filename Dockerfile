FROM alpine:3.9
RUN apk add --no-cache python3 && \
    pip3 install --upgrade pip && \
    pip3 install requests pytest mock && \
    addgroup -S -g 1000 python_user && \
    adduser -u 1000 -S -G python_user -h /home/python_user -s /sbin/nologin -D python_user && \
    chown -R python_user:python_user /home/python_user
WORKDIR /home/python_user
COPY service/ .
COPY tests/ ./tests
COPY src/ /usr/lib/python3.6/site-packages/cox_auto_app
RUN chmod +x ./service
USER python_user
ENTRYPOINT ["./service"]
