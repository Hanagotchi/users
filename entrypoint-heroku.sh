#!/bin/bash

uvicorn main:app --host 0.0.0.0 --port ${PORT} &
arq worker.WorkerSettings &
python clock.py 