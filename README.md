### Install

```
/bin/bash <(curl -s https://raw.githubusercontent.com/dalibor91/pymail/master/install.sh)
```
### Uninstall

```
/bin/bash <(curl -s https://raw.githubusercontent.com/dalibor91/pymail/master/uninstall.sh)
```

### Note 
This is not fully tested, all data is saved in plain text in sqlite database on server on which it run

### How it works

Py mailer starts server instance listening on some port that you define, and whenever you want to send new email to someone you make new HTTP POST request on that port, also you can enable authentification for requests.

- First you add servers, where you define which ip, port and should users authentificate to send emails.
- Second you add email addreses you want to use and from which emails would be sent 
- Third you assign email addreses to servers
- Fourth you assign which users can access which server (this is using basic auth for authentification)

When user makes request and everything is ok, server stores data in queque and this queque is latter emptyed (usally with cronjob that does that)


### Servers

```
#add server 
pymail -m server -f add -a ip=0.0.0.0 port=4444 auth=1

#list servers
pymail -m server -f list 

#update server 
pymail -m server -f update -a id=1 port=4445

#remove server 
pymail -m server -f remove -a id=1

#start server 
pymail -m server -f start -a id=1

#stop server 
pymail -m server -f stop -a id=1

#restart server 
pymail -m server -f restart -a id=1

#list users assigned to server 
pymail -m server -f list -a id=1 users

#list emails assigned to server 
pymail -m server -f list -a id=1 emails 

#add email to server 
pymail -m server -f addemail -a server=1 email=1

#remove emial from server 
pymail -m server -f removeemail -a server=1 email=1

#add user to server 
pymail -m server -f adduser -a server=1 user=1

#remove user from server 
pymail -m server -f removeuser -a server=1 user=1

```

### Users

```
#add user 
pymail -m user -f add -a username=test password=test 

#remove user 
pymail -m user -f remove -a id=1

#list users 
pymail -m user -f list 

#update users 
pymail -m user -f update -a id=1 username=test1 password=test5

```

### Emails

```
#add email 
pymail -m email -f add -a email=test@gmail.com username=test@gmail.com password=123 host=gmail.com port=465 tls=1

#remove email 
pymail -m email -f remove -a id=1

#update email
pymail -m email -f update -a id=1 password=123456

```

### Queque

```
To see all emials that were stored in queque 
pymail -m queque -f list 

#to add json file with data in queque 
pymail -m queque -f add -a path=/path/to/file.json
#or
pymail -f load -a file=/path/to/file.json

#to remove record from queque 
pymail -m queque -f remove -a id=1

#to list failed emails from queque
pymail -m queque -f list -a failed

#to list done email from queqeu 
pymail -m queque -f list -a done

#to list waiting emails in queque 
pymail -m queque -f list -a waiting

#to resend some email from queque 
pymail -m queque -f resend -a id=1

#to send all waiting emails in queque
#this usally is added to crontab
pymail -m queque -f sendwaiting

#to resend all failed emails 
pymail -m queque -f sendfailed

```

Sample of how json data sent to server should look 

```
{
	"from": "john@doe.com",
	"recieve": {
		"to" : [
			{
				"email": "test@gmail.com",
				"name": "John Doe"
			}
		], 
		"cc": [
			{
				"email": "john.doe1@gmail.com",
				"name": "john doe"
			}
		],
		"bcc": [
			{
				"email": "john.doe2@gmail.com",
				"name": "jogn"
			}
		]
	}, 
	"subject": "This is test", 
	"body": "this is some body to send", 
	"attach": [
		{
		"name": "test.txt", 
		"content": "VGhpcyBpcyB0ZXN0"
		}
	]
}

```


### test 

When you set up everything you can run some tests to see if this thing works 
Note: make sure that 
```
pymail -m queque -f sendwaiting
```
is in crontab or run it manualy after you add files to send 


Testing with json file without auth 
```
pymailerclientf -h localhost -p 9999 -f test.json
```

Testing with json file with auth 
```
pymailerclientf -h localhost -p 9999 -f test.json -login test:test
```


Testing without json file and without auth 
```
echo "test" | pymailerclient -h localhost -p 9999 -s "This is just command line test" -f "test@gmail.com" -t "test@gmail.com"
```


Testing without json file and with auth 
```
echo "test" | pymailerclient -h localhost -p 9999 -s "This is just command line test" -f "test@gmail.com" -t "test@gmail.com" -login test:test
```





