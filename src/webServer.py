
''' Progetto di programmazione di reti - Atanasov Atanas Todorov - Python Web Server '''

import http.server
import socketserver
import sys
import signal

# Il numero della porta può essere fornito da riga di comando (default 8080)
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080
print("Server is waiting on port", port)


# Il server deve essere abilitato alla gestione di più richieste contemporaneamente
server = socketserver.ThreadingTCPServer(('',port), http.server.SimpleHTTPRequestHandler)

# Assicura che da tastiera usando la combinazione
# di tasti Ctrl-C termini in modo pulito tutti i thread generati
server.daemon_threads = True  
# Il Server acconsente al riutilizzo del socket anche se ancora non è stato
# rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  

# Fuzione che permette di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print('Exiting web server (Ctrl+C pressed)')
    try:
        if(server):
            server.server_close()
    finally:
        sys.exit(0)

# Interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

# Entra nel loop infinito
try:
    while True:
        server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()