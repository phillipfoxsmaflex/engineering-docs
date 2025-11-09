# 🚀 Engineering Docs - Deployment Guide

## 🔍 Problem Identifiziert

Ihre PostgreSQL-Datenbank existiert bereits, aber **ohne jegliche Benutzer**. Das passiert, wenn die Datenbank-Initialisierung fehlgeschlagen ist, aber das Volume bereits erstellt wurde.

## 🛠️ Lösungsoptionen

### Option 1: Saubere Neuinitialisierung (⭐ EMPFOHLEN)

Diese Option löscht alle Daten und startet komplett neu:

```bash
# 1. Reset durchführen
./reset-database.sh

# 2. Sauberes Deployment starten
docker compose up --build
```

### Option 2: Existierende Datenbank reparieren

Falls Sie Daten behalten möchten (experimentell):

```bash
# Reparatur-Script ausführen
./fix-existing-database.sh
```

### Option 3: Manuelle Reparatur

Falls die Scripts nicht funktionieren:

```bash
# 1. Alle Container stoppen
docker compose down -v

# 2. Nur Datenbank starten
docker compose up -d db

# 3. In Container einloggen und manuell reparieren
docker compose exec db sh

# 4. Im Container:
su-exec postgres psql -d postgres
CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres_password';
CREATE DATABASE engineering_docs OWNER postgres;
\q

# 5. Alle Services starten
docker compose up -d
```

## 📋 Was die Fixes beheben

### ✅ Behobene Probleme:
1. **Script-Berechtigungen**: `create-user.sh` hat jetzt Ausführungsrechte
2. **Fehlende asyncpg**: Python-Dependency wurde zu requirements.txt hinzugefügt
3. **Database-User-Problem**: Robuste User-Erstellung implementiert
4. **Umgebungsvariablen**: `.env` Datei korrekt konfiguriert

### 🔧 Implementierte Verbesserungen:
- **reset-database.sh**: Vollständige Bereinigung aller Volumes und Container
- **fix-existing-database.sh**: Reparatur existierender Datenbanken
- **Verbesserte Initialisierung**: Robustere custom-init.sh Scripts
- **Bessere Fehlerbehandlung**: Detaillierte Logs und Fehlermeldungen

## 🎯 Erwartetes Verhalten nach dem Fix

Nach einem erfolgreichen Deployment sollten Sie sehen:

```
✅ PostgreSQL startet mit postgres superuser
✅ custom-init.sh erstellt appuser automatisch
✅ Backend verbindet sich erfolgreich als appuser
✅ Alle Services sind gesund und erreichbar
```

## 🔍 Logs überwachen

```bash
# Alle Services
docker compose logs -f

# Nur Backend
docker compose logs -f backend

# Nur Datenbank
docker compose logs -f db
```

## 🆘 Troubleshooting

### Problem: "role does not exist"
**Lösung**: Verwenden Sie `./reset-database.sh` für saubere Neuinitialisierung

### Problem: "Permission denied"
**Lösung**: Scripts haben jetzt korrekte Berechtigungen

### Problem: "ModuleNotFoundError: asyncpg"
**Lösung**: asyncpg wurde zu requirements.txt hinzugefügt

### Problem: Container startet nicht
**Lösung**: 
1. `docker compose down -v`
2. `./reset-database.sh`
3. `docker compose up --build`

## 📞 Support

Falls Probleme bestehen:
1. Führen Sie `./reset-database.sh` aus
2. Starten Sie mit `docker compose up --build`
3. Teilen Sie die Logs mit: `docker compose logs -f`