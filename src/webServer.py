
''' Atanasov Atanas Todorov / Progetto di Reti / Traccia 2 / Web Server '''

import http.server
import socketserver
import sys
import signal

# Struttura dati che contiene il nome dei file presenti nei percorsi
pages = [("index.html", "html/index.html"),
            ("", "html/index.html"), 
            ("contatti.html", "html/contatti.html"),
            ("prenotazioni.html","html/prenotazioni.html"),
            ("appuntamenti.html", "html/appuntamenti.html")]

# Classe handler
class MyHandler (http.server.SimpleHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print(self.headers)
        if self.path[:4] == "/res":
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.research()        
        
    # Funzione per la ricerca della pagina
    def research(self):
        cont = 0
        for page in pages:
            if page[0] == self.path[1:]:
                page = open(page[1]).read()
                self.do_HEAD()
                self.wfile.write(bytes(page, "utf8"))
                found = True
                break
            else:
                cont += 1
                if cont == len(pages):
                    found = False
        if found == False:
            self.do_HEAD()
            self.wfile.write(bytes("404 Error Page not found", "utf8"))



# Il numero della porta può essere fornito da riga di comando (default 8080)
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080
print("Server is waiting on port", port)

handler = MyHandler

# Il server deve essere abilitato alla gestione di più richieste contemporaneamente
server = socketserver.ThreadingTCPServer(('',port), handler)

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