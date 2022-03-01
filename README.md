[Dr. Rodrigo Carareto](http://lattes.cnpq.br/4506432912671820), [Insper](https://github.com/Insper), 2022.

# Real time Client-Server

## Objective

- An application (client) must send via serial UART transmission a sequence of commands (byte list) to another application (server). The commands will be shown below.
- The sequence must have between 10 and 30 commands, to be determined by the client (randomly). The server does not know how many commands it will receive.
- After the reception, the server must return to the client a message informing the number of commands that was received.
- As soon as the client receives the answer with this number, it can verify that all commands were received, and the process ends.
- If the number of commands informed by the server is not correct, the client must display a message warning of the inconsistency.
- If the server does not return anything within 10 seconds, the client must display a “time out” message
- The transmission must be done with two Arduinos. Each application will communicate with one of them.

## Commands
Following is the list of commands. Note that there are 6 different commands. Some consist of 1 byte, some of 2 bytes and
others consist of 4 bytes.
- Command 1: **00** **FF** **00** **FF** (4-byte command)
- Command 2: **00** **FF** **FF** **00** (4-byte command)
- Command 3: **FF** (1-byte command)
- Command 4: **00** (1-byte command)
- Command 5: **FF** **00** (2-byte command)
- Command 6: **00** **FF** (1-byte command)

## Install dependencies
```bash
$ pip install -r requirements.txt
```


## Running the program
Run server
```bash
$ python src/server.py
```

Run client
```bash
$ python src/client.py
```
