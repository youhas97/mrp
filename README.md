# NFC - Ingripande App

Projekt-repo för grupp 11 i kandidatprojektskursen TDDD96.


Vikten är ett värde mellan 2 och 100 där större tal innebär viktigare uppgift,

Tid är ett värde mellan 1 och 5, ju större värde, desto närmare deadline

Svårighet & Betydelse antar värden mellan 1 och 10, där 10 innebär hur svårt/betydelsefullt arbetet är.

Vikten räknas ut med T*(S+B), där T=tid, S=svårighet, B=betydelse

## Använda pipenv för att jobba med Django

Se till att ha pipenv installerad. Om inte, kör:

`pip install pipenv`

För att installera alla dependencies kör `pipenv install`

Om du är Windows pleb och får problem med mysqclient så kör:

`pipenv uninstall mysqlclient`

Om du fortfarande har problem så saknar du säkert andra dependencies på din 
dator, exempel:

libbz2, pypiwin32, Visual C++ Build Tools.

För att använda pipenv kör `pipenv shell`, se till att du står i back-end/
och kör `python manage.py runserver XXXX`, där XXXX är valfri port.

Alternativt för att slippa pipenv shell, kör:

`pipenv run python manage.py runserver XXXX`.

Done.
