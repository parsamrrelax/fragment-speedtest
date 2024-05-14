
# Automatically speedtest fragment with different values

This code helps to check different fragment values inside vless configs
This code will only work on Linux. So if you're using windows you should use WSL.

First go ahead and clone this project
```bash
git clone https://github.com/parsamrrelax/fragment-speedtest
```
and cd into it
```bash
cd fragment-speedtest
```

You need to install requests in order to use this code
```bash
pip3 install requests
```

## So now you have to modify your config files.
If you're using ws config:
- open configws.json config file in your favorite editor
- from your own vless config replace:
		1. address
		2. port
		3. id
		4. servername
		5. host

If you're using grpc config:
- open config.json config file in your favorite editor
- from your own vless config replace:
		1.address
		2. port
		3. id
		4. servername
		5. servicename
		6. make sure your config is on gun and not on multi

**If you are using grpc config you must pass --grpc when running the code**


## Modify your interval and length for the tests.
Open fragment.txt inside an editor and on each line enter a value you want to test. example file included.
If you want to test each interval with different lengths open length.txt and write length values inside of it. example file included.
**If you want to test length values you must pass --length when running the code**

## Arguments
by default this code only tests the upload speed of a 5MB file:
Testing larger files sizes results in more accurate results.
In order to do so run with `--filesize {a number in MB}` so `--filesize 10` will do the test with a 10MB file.

In order to run download speed test as well run with `--download`

If your config file was grpc run with `--grpc`

If you want to check the length run with `--length`

## Examples

run with 10MB file with download
```bash
python3 fragmentchecker.py --download --filesize 10
```

run with testing length on a grpc config
```bash
python3 fragmentchecker.py --length --grpc
```