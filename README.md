Как я получил отчет.

1. docker compose up --build -d
2. docker restart reports-api
3. curl -v http://localhost:8000/
(возможно снова docker restart reports-api)
4. curl -v http://localhost:8080/
5. python pkce_generator.py

Берем code_challenge, вставляем в запрос ниже и запускаем

http://localhost:8080/realms/reports-realm/protocol/openid-connect/auth
    ?client_id=reports-frontend
    &response_type=code
    &redirect_uri=http://localhost:3000/callback
    &scope=openid
    &code_challenge_method=S256
    &code_challenge=*вставить значение*

Login: prothetic1
Password: prothetic123

Далее следует редирект, в Url которого есть code. Используем его и code_verifier, полученный ранее, в скрипте:
curl -X POST "http://localhost:8080/realms/reports-realm/protocol/openid-connect/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=authorization_code" \
    -d "client_id=reports-frontend" \
    -d "code=*вставить значение*" \
    -d "redirect_uri=http://localhost:3000/callback" \
    -d "code_verifier=*вставить значение*"

Откроется страничка с кнопкой download report, по которой скачивается отчет в формате json.
