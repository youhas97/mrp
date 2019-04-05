# NFC - Ingripande App

Projekt-repo för grupp 11 i kandidatprojektskursen TDDD96.


Vikten är ett värde mellan 2 och 100 där större tal innebär viktigare uppgift,

Tid är ett värde mellan 1 och 5, ju större värde, desto närmare deadline

Svårighet & Betydelse antar värden mellan 1 och 10, där 10 innebär hur svårt/betydelsefullt arbetet är.

Vikten räknas ut med T*(S+B), där T=tid, S=svårighet, B=betydelse

## Production mode (frontend)
Denna mode körs i heroku, och kan även köras lokalt (se starta frontend i 
production mode). Detta innebär att servern kommer att startas med node,
och behöver filerna som används i /dist/ mappen som skapas av `npm run build`.
Vue kommer även att ansluta till heroku backend url istället för lokalt i 
production mode.

## Development mode. (frontend)
Denna mode körs när man startar frontend med `npm run serve`. I denna mode
kommer vue att ansluta till backend med lokal uri på port 9000. Se till att
backend är startad med ssl på port 9000.

## Dependencies
Dependencies hanteras med npm för frontend och pipenv för backend. 

För att installera npm dependencies kör `npm install`.

För att installera pipenv dependencies kör `pipenv install`.

### Andra dependencies

Det finns vissa dependencies som måste finnas lokalt på datorn för att 
man ska kunna köra frontend/backend lokalt:

redis
npm
pipenv
pip

## Använda pipenv för att jobba med Django

Se till att ha pipenv installerad

`pip install pipenv`

För att installera alla dependencies kör `pipenv install`

För att använda pipenv kör `pipenv shell`

Done.

## Starta både frontend och backend samtidigt i en terminal.

Stå i root mappen och kör `pipenv run honcho start`.

## Starta frontend i production mode.

Stå i frontend mappen och kör `npm run build`.

Efter det exekvera `node server_local.js`, så kommer node starta en https server
på port 8000. 

## Starta frontend i developent mode.

Stå i frontend mappen och kör `npm run serve`.

## Starta backend på ssl port.

Stå i backend mappen och kör `pipenv run honcho -f ProcfileLocal start`.

honcho kommer att exekvera denna kommando:

`daphne -e ssl:9000:privateKey=server.key:certKey=server.crt mysite.asgi:application`

Detta kommando kan också exekveras utan honcho genom att köra 
`pipenv run [kommando]`.
