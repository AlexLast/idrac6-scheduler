# idrac6-scheduler

The API for the iDRAC6 Express is complicated at best with little to no documentation. This simple script can be used to interact via the frontend and schedule the following actions in an automated fashion:

 - Power server on
 - Power server off

Example usage:

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py -u root -p password -i 10.0.13.17 -a power_on
```
