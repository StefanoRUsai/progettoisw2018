# README #

# Progetto ISW 2018 Gruppo12 #
## Progetto Sistema di webApp Booking progettato con framework Django ##
### Giorgia Campanile, Edoardo Cittadini, Marta Pibiri, Mario Taccori, Stefano R. Usai ###

Sviluppo di un’applicazione Web per la gestione di delle prenotazioni di hotel online
(Booking.com).
In cui un utente si possa registrare al sistema come Albergatore. Una volta loggato un albergatore
viene mandato nella propria Home.

Dalla Home un Albergatore può vedere la lista delle Prenotazioni effettuate dagli utenti del
sistema.

Cliccando su “Lista Hotel” si va alla pagina di gestione degli Hotel. In questa pagina viene
presentata una lista degli Hotel gestiti dall’Albergatore come mostrato in Figura 2.
Cliccando “Aggiungi Hotel” è possibile inserire un nuovo Hotel (nome, descrizione, città e
indirizzo).

Cliccando su un Hotel si va alla pagina di gestione dell’Hotel come mostrato in Figura 3. Da
qui è possibile vedere le informazioni dell’Hotel e la lista delle camere presenti.
Cliccando su “Aggiungi Camera” è possibile aggiungere una nuova camere (numero, posti
letto e servizi e costo)

Un utente non registrato accede alla pagina di ricerca di una camera inserendo la città, il
numero di posti letto, la data di check-in e quella di check-out. Il sistema recupera tutte le
camere che soddisfano i criteri di ricerca e sono disponibili in quel periodo.
Cliccando su una camera è possibile prenotarla. Viene richiesto all’utente di inserire una
email e i dati di pagamento con Carta di Credito (numero, anno e mese di scadenza e
codice CVV), il sistema deve dare la possibilità di salvare i dati di pagamento per
prenotazioni future. Al termine del pagamento viene creata una Prenotazione (email,
camera, data check-in, data check-out).

