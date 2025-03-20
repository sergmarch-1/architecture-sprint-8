После запуска контейнеров, reports-api отваливается, вероятно т.к. запускается перед keycloak => docker restart reports-api => reports-api больше не отваливается.

Проверка подключения контейнера reports-api к Keycloak успешна:
$ docker exec -it reports-api sh
# curl -v http://architecture-sprint-8-keycloak-1:8080/realms/reports-realm/protocol/openid-connect/certs


