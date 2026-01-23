#!/bin/bash
# Zatrzymanie kontenerów i usunięcie wolumenów (czyści bazę danych) 
docker-compose down -v
# usuwanie kontenerów o tych samych nazwach
docker rm -f cassnadra kafka generator connector 2>/dev/null
# Budowanie i uruchomienie w tle
docker-compose up --build -d
echo "System został uruchomiony"
