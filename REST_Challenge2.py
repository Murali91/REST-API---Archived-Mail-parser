from flask import Flask,request,jsonify
import tarfile,os,sys,time,re

app = Flask(__name__)

def createdir(): #create a dir with the name as output_<timestamp> and a file within it named as "output" in which the content will be written
	datetime = time.strftime("%c") #calculate timestamp
	tstmp = re.sub('[:/ ]', '_', datetime)
	tstmp = "output_"+tstmp
	os.mkdir(tstmp)
	file = open(os.path.join(tstmp,"output.txt"),'a')
	return tstmp,file

def response(status,code,data):
    resp_data = {
    'STATUS':status,
    'DATA':data
        }
    response = jsonify(resp_data)
    response.status_code = code
    return response
 
 
def success(code, data):
    return response("SUCCESS",code, data)
 
def failure(code,data):
    return response("FAILURE",code,data)

def parser(handler,keyword,output):
	files = handler.getnames()
	directory = files.pop(0) #removes first entry in the list since it will be the dir name
		
	try:
		for file in files:
			fileObj = handler.getmember(file)
			extract = handler.extractfile(fileObj)
			content = extract.read().splitlines() #strores the content of the message file in a string split by '\n'
			output.write("\n\n===========Parsed content of filename %s==============\n" %(file))
			for item in keyword:
				if not (item.endswith(':')): 
					item = item+':'					
				for line in content:
					if line.startswith(item): #searches for the keyword in each line to get the value
						output.write("%s |" %(line))
						break
					else:
						continue

	except AttributeError:
		return failure(500,"Incorrect value for the file handler")
	except ValueError:
		return failure(500,"Error in accessing elements of list")
	except IOError:
		return failure(500,"Error in writing files to disk")
	except tarfile.TarError:
		return failure(500,"Error in perfroming operations on the tarfile")
	except:
		return failure(500,"Error in parsing the files for input keywords.")



@app.route('/')
def welcome():
	welcome = '''

:::       ::: :::::::::: :::         ::::::::   ::::::::  ::::    ::::  ::::::::::
:+:       :+: :+:        :+:        :+:    :+: :+:    :+: +:+:+: :+:+:+ :+:       
+:+       +:+ +:+        +:+        +:+        +:+    +:+ +:+ +:+:+ +:+ +:+       
+#+  +:+  +#+ +#++:++#   +#+        +#+        +#+    +:+ +#+  +:+  +#+ +#++:++#  
+#+ +#+#+ +#+ +#+        +#+        +#+        +#+    +#+ +#+       +#+ +#+       
 #+#+# #+#+#  #+#        #+#        #+#    #+# #+#    #+# #+#       #+# #+#       
  ###   ###   ########## ##########  ########   ########  ###       ### ##########

*****************************************************************************
                  Outlook Archived Mail Parser  v1.0								
                                                                               
 	Results will be in the output_"timestamp" directory under 		
			the current working directory           							
																				
*****************************************************************************
'''
	return welcome


@app.route('/path',methods = ['POST'])
def validate_path():
	try:
		try:
			path = request.form.get('path')
			keyword = list(request.form.get('keyword').split(','))
		except:
			raise Exception("Error in accessing the form data.")
		directory,output = createdir()
		if path.endswith('.tar.gz') or path.endswith('.tgz'): #checks for the valid file extension
			try:
				handler = tarfile.open(path,'r:gz')
			except:
				raise Exception("Unable to open the tar file")
		elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
			try:
				handler = tarfile.open(path,'r:bz2')
			except:
				raise Exception("Unable to open the tar file")
		else:
			if not os.path.exists(path): #checks if the path itself is valid for any file
				return failure(400,"Path seems to be incorrect. Please try again with the different input")
			else:
				return failure(404,"Incorrect file extension. Please try again with the path of a tar file that has to be parsed.")
		#return "Validation Successful!! Processing the File.........."
		parser(handler,keyword,output)
		return success(200,"Request has been processed successfully. Output has been stored in directory path")
	except Exception as e:
		return failure(500,e.message)



if __name__ == '__main__':
	app.run	(port = 5000)