# CarSharing

Acest proiect reprezintă o aplicație completă de car-sharing, dezvoltată ca parte a cursului **ISSA (Inginerie Software Specifică Automobilelor)** susţinut de echipa Continental la Facultatea de Informatică din Iaşi. Aplicația permite utilizatorilor să se înregistreze, să adauge metode de plată și documente, să închirieze mașini și să gestioneze procesul de închiriere.

## Tehnologii utilizate

Proiectul este construit folosind un stack modern de tehnologii, incluzând:

### Frontend
- **Angular**: Framework pentru dezvoltarea aplicațiilor web.
- **TypeScript**: Limbaj de programare tipizat pentru dezvoltarea aplicațiilor frontend.
- **Leaflet**: Bibliotecă pentru afișarea hărților interactive.
- **HTML5 & CSS3**: Structurarea și stilizarea interfeței utilizatorului.

### Backend
- **FastAPI**: Framework rapid pentru dezvoltarea API-urilor RESTful.
- **SQLAlchemy**: ORM pentru gestionarea bazei de date.
- **SQLite**: Bază de date utilizată pentru stocarea datelor aplicației.
- **APScheduler**: Scheduler pentru gestionarea sarcinilor recurente (ex. ștergerea închirierilor expirate).

### Altele
- **JWT (JSON Web Tokens)**: Pentru autentificarea utilizatorilor.
- **bcrypt**: Pentru securizarea parolelor utilizatorilor.
- **Flask**: Utilizat pentru gestionarea telematicii mașinilor.

## Funcționalități

1. **Autentificare și înregistrare utilizatori**
   - Utilizatorii se pot înregistra și autentifica folosind email și parolă.
   - Token-ul JWT este utilizat pentru autentificare.

2. **Adăugare metode de plată și documente**
   - Utilizatorii pot adăuga metode de plată și documente necesare pentru închirierea mașinilor.

3. **Harta interactivă**
   - Utilizatorii pot vizualiza mașinile disponibile pe o hartă interactivă și pot selecta o mașină pentru închiriere.

4. **Închiriere și returnare mașini**
   - Utilizatorii pot închiria mașini pentru o anumită perioadă de timp.
   - Sistemul gestionează starea mașinilor și verifică dacă acestea pot fi returnate.

5. **Gestionarea telematicii**
   - Datele telematice ale mașinilor (ex. locație, nivel combustibil, starea motorului) sunt gestionate printr-un server Flask.

6. **Scheduler pentru închirieri expirate**
   - Închirierile expirate sunt șterse automat, iar starea mașinilor este actualizată.
