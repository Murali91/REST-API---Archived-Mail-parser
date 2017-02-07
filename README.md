# REST-API---Archived-Mail-parser

Below are the steps to be followed in order to use this API
1.	GET request without any domain will show the welcome screen.
 
2.	POST request has to be sent since we post the path and keyword details in order to get the header data.

3.	URL should be ending with ‘/path’ to indicate that path and keyword details is being sent.
 
4.	Path and keyword values are attached as parameters in the body of the POST request.
 
5.	Parameter names should be “path” and “keyword”.

6.	If the request is a success, then success message is returned else corresponding error message is returned.
 
7.	Output file will be stored in a directory with the timestamp in its name under the current working directory.

