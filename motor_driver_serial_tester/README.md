# Motor Driver Serial Tester

Simple python cli program to test communications with arduino to control two `28BYJ-48`
motors.

# To run the program

1. Create and activate virtual environment

```bash
cd arduino_comm

python3 -m venv .venv

source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run script

```bash
./drive
```

The script will run with default device `/dev/ttyACM0` and baud rate `115200`. To
override this pass device and baud rate as:

```bash
./drive /dev/ttyUSB0 9600
```
