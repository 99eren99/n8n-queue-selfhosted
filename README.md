Reference: https://www.idir.ai/en/blog/scale-n8n-like-the-ultimate-guide-to-queue-mode-docker</br></br>
Environment variables fixed for forms, webhook requests, runners, http serving etc.

>*To run:*
```bash
git clone https://github.com/99eren99/n8n-queue-selfhosted
cd n8n-queue-selfhosted
mv env .env
docker compose down ; docker compose up -d --build
```

>*Architecture:*
```
                    ┌─────────────────┐
                    │  Reverse Proxy  │
                    │  (Nginx/Traefik)│
                    └───────┬─────────┘
                            │
              ┌─────────────┼──────────────┐
              │             │              │
              ▼             │              ▼
      ┌──────────┐          │      ┌────────────────────┐
      │   MAIN   │          │      │     WEBHOOK        │
      │ Editor   │          │      │  Processor         │
      │ API      │          │      │  /webhook/*        │
      │ Triggers |          |      |  /webhook-waiting/*│
      │ &Runner  │          │      │ &Runner (sidecar)  │
      │ (sidecar)│          │      └──────┬─────────────┘
      └────┬─────┘          │             │
           │     ┌──────────┘             │
           │     │                        │
           ▼     ▼                        ▼
      ┌──────────────────────────────────────┐
      │              Redis (queue)           │
      └──────────────────┬───────────────────┘
                         │
                         ▼
                  ┌──────────┐
                  │  WORKER  │
                  │ &Runner  │
                  │ (sidecar)│
                  └──────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   PostgreSQL    │
              └─────────────────┘
```
