# pyjob
Scheduler for runing python scripts  - something like crontab 


To list all availible jobs run 
```
python main.py list
```

To run specific job run 
```
python main.py run dummy_job
```

To run all jobs , this should be called every X seconds ( 60 sec ) or it can be less
```
python main.py all
```

To cleanup all lock files, logs and properties run 
```
python main.py cleanup
```
