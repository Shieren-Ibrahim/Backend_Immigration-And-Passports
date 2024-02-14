from django.shortcuts import render,redirect
from .models import User,Moving,Staying,PassPort,Holiday,LimitsOfDate,Ready1,PaperPassport,PaperMoving,PaperStaying
from django.contrib import  messages
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,date,timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import schedule
@csrf_exempt
def login(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                password=body['password']
                ssn=int(body['ssn'])
                #any_holiday()
                #ready=Ready1.objects.filter(ssn=ssn).all()
                try:
                        user=User.objects.get(ssn=ssn)

                        try:
                            any_holiday()
                            user=User.objects.get(password=password,ssn=ssn)
                            user_asJson=getAsJson(user)
                            del user_asJson['_state']
                            user_asJson['result']='true'
                            print('1gggggggggggggggggggggggggggggg') 
                            ready=Ready1.objects.filter(ssn=ssn).all()
                            #print(ready)
                            ready_passport=False
                            ready_moving=False
                            ready_staying=False	
                            print('3gggggggggggggggggggggggggggggg')
                            for obj in ready:
                                print('j')
                                if obj.ready == 1:
                                    ready_passport=True
                                elif obj.ready == 2:
                                    ready_moving=True
                                elif obj.ready ==3 :
                                    ready_staying=True
                                        
                            print('gggggggggggggggggggggggggggggg')       
                            confirm_passport=True
                            try:
                                confirm_passport=PassPort.objects.get(owner=user).confirm
                            except :
                                pass
                            confirm_moving=True
                            try:
                                confirm_moving=Moving.objects.get(owner=user).confirm
                            except :
                                pass
                            confirm_staying=True
                            try:
                                confirm_staying=Staying.objects.get(owner=user).confirm
                            except :
                                pass
                            passport_date=None
                            moving_date=None
                            staying_date=None
                                
                            if confirm_passport == False :
                                passport_date=PassPort.objects.get(owner=user).date
                            if confirm_moving == False :
                                moving_date=Moving.objects.get(owner=user).date
                            if confirm_staying == False :
                                staying_date=Staying.objects.get(owner=user).date

                            user_asJson['staying_date']=staying_date
                            user_asJson['moving_date']=moving_date
                            user_asJson['passport_date']=passport_date
                            user_asJson['ready_passport']=ready_passport
                            user_asJson['ready_moving']=ready_moving 
                            user_asJson['ready_staying']=ready_staying
                            user_asJson['confirm_passport']=confirm_passport
                            user_asJson['confirm_moving']=confirm_moving
                            user_asJson['confirm_staying']=confirm_staying
                                
                            return JsonResponse(user_asJson,safe=False)
                        except:
                            return JsonResponse({'result':'error password'}) 
                except:
                    return JsonResponse({'result':'error ssn'})
                
 
@csrf_exempt
def signup(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		password=body['password']
		ssn=body['ssn']
		name=body['name']
		try:
			user=User.objects.get(ssn=ssn)
			return JsonResponse({'result':'exists ssn'}) 
		except :
			user=User(username=name,password=password,ssn=ssn)
			user.save()
			user_asJson=getAsJson(user)
			del user_asJson['_state']
			user_asJson['result']='true'
			#mn=LimitsOfDate.objects.last().new_min
			#mx=LimitsOfDate.objects.last().new_max
			#user_asJson['mn']=mn
			#user_asJson['mx']=mx
			return JsonResponse(user_asJson,safe=False)
def getAsJson(obj):
	return json.loads(json.dumps(obj,default = lambda o:o.__dict__))


	
@csrf_exempt
def forgetten_password(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				print(body)
				ssn=body['ssn']
				try:
					password=User.objects.get(ssn=ssn).password
					print(password)
					password_asJson=getAsJson(password)
					return JsonResponse({'result':'true','password':password})
				except :
					return JsonResponse({'result':'false1'})
				


@csrf_exempt	
def bookPassport(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		interal=body['passportType']
		normal=body['passportPriority']
		date=body['bookingDate']
		print(date)
		print('_____________________')
		#date=to_date(body['bookingDate'])
		
		result=valid_date(date)
		if result != True :
			return JsonResponse(result)
		
		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		print('_____________________')
		try:
			passport=PassPort.objects.get(owner=user)
			return JsonResponse({'result':'exists booking'})
		except:
			
			passports=PassPort.objects.filter(date=date)
			
			
			if passports.count()<1 :
				
				passport=PassPort(internal=interal,normal=normal,date=date,owner=user).save()
				return JsonResponse({'result':'true'})
			else :
				return JsonResponse({'result':'invaled date'})

def to_date(d):
        d=d.strftime("%Y-%m-%d")
        return d
#datetime.strptime(d,'%Y-%m-%d')


def valid_date(date):
	try:
                date=datetime.strptime(str(date),'%Y-%m-%d')
                is_holiday=Holiday.objects.get(date=date)
                return {'result':'false','type':'1'}
	except:
		return True

@csrf_exempt
def bookMovment(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)
		print(body)
		print(body['movmentdate'])
		date=body['movmentdate']
		print(date)
		result=valid_date(date)
		if result != True :
			
			return JsonResponse(result)
      		
        	

		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		print('___________jj___________')
		try:
			moving=Moving.objects.get(owner=user)
			return JsonResponse({'result':'exists booking','type':'2'})
		except:
			movings=Moving.objects.filter(date=date)
			if movings.count()<1:
				moving=Moving(date=date,owner=user)
				moving.save()
				moving_asJson=getAsJson(moving)
				del moving_asJson['_state']
				moving_asJson['result']='true'
				return JsonResponse(moving_asJson,safe=False)
			else :
				return JsonResponse({'result':'false','type':'1'})
	return JsonResponse({'result':'false','type':'1'})


@csrf_exempt
def bookAccomodation(request):
	if request.method == 'POST':
		decoded_body=request.body.decode('utf-8')
		body=json.loads(decoded_body)

		date=body['bookingDate']
		result=valid_date(date)
		if result != True :
			return JsonResponse(result)

		ssn=int(body['ssn'])
		user=User.objects.get(ssn=ssn)
		try:
			staying=Staying.objects.get(owner=user)
			return JsonResponse({'result':'exists booking','type':'2'})
		except:
			stayings=Staying.objects.filter(date=date)
			if stayings.count()<1:
				staying=Staying(date=date,owner=user)
				staying.save()
				staying_asJson=getAsJson(staying)
				del staying_asJson['_state']
				staying_asJson['result']='true'
				return JsonResponse(staying_asJson,safe=False)
			else :
				return JsonResponse({'result':'false','type':'1'})
	return JsonResponse({'result':'false','type':'1'})

@csrf_exempt
def confirmationOfReservation(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				print('____________')
				ssn=int(body['ssn'])
				user=User.objects.get(ssn=ssn)
				try:
					passports=PassPort.objects.get(owner=user).date
					print('___vvv_________')
              		#print('___vvggv_________')
					#passpprts_asJson=getAsJson(passports)
					#del passports_asJson['_state']
					#passports_asJson['result']='true'
					return JsonResponse({'result':'true','date':passports})
				except:
					print('___vvv_________')
					return JsonResponse({'result':'false'})
				#return JsonResponse({'result':'false'})
@csrf_exempt
def confirmationOfReservationMR(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=int(body['ssn'])
				user=User.objects.get(ssn=ssn)
				try:
					movings=Moving.objects.get(owner=user).date
					return JsonResponse({'result':'true','date':movings})
					#movings_asJson=getAsJson(movings)
					#del movings_asJson['_state']
					#movings_asJson['result']='true'
					#return JsonResponse(movings_asJson,safe=False)
					#staying_asJson['result']='true'
      				
          			

				except:
					return JsonResponse({'result':'false'})
				#return JsonResponse({'result':'false'})
    
    
@csrf_exempt
def confirmationOfReservationAB(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=int(body['ssn'])
				user=User.objects.get(ssn=ssn)
				try:
					stayings=Staying.objects.get(owner=user).date
					#stayings_asJson=getAsJson(stayings)
					#del stayings_asJson['_state']
					#return JsonResponse(stayings_asJson,safe=False)
					return JsonResponse({'result':'true','date':stayings})
				except:
					return JsonResponse({'result':'false'})
				#return JsonResponse({'result':'false'})
@csrf_exempt
def cancellationOFResevation(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				PassPort.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})
@csrf_exempt
def cancellationOFResevationMR(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				Moving.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})
@csrf_exempt
def cancellationOFResevationAB(request):
	if request.method == 'POST':
				decoded_body=request.body.decode('utf-8')
				body=json.loads(decoded_body)
				ssn=body['ssn']
				user=User.objects.get(ssn=ssn)
				Staying.objects.get(owner=user).delete()
				return JsonResponse({'result':'true'})


@csrf_exempt
def confirm_passport(request):
	if request.method == 'POST':
                try:
                    decoded_body=request.body.decode('utf-8')
                    body=json.loads(decoded_body)
                    print(decoded_body)
                    ssn=body['ssn']
                    user=User.objects.get(ssn=ssn)
                    passport=PassPort.objects.get(owner=user)
                    passport.confirm=True
                    PassPort.objects.get(owner=user).delete()
                    passport.save()
                    return JsonResponse({'result':'true'})
                except:
                    return JsonResponse({'result':'false'})
@csrf_exempt
def confirm_staying(request):
	if request.method == 'POST':
                try:
                    decoded_body=request.body.decode('utf-8')
                    body=json.loads(decoded_body)
                    print(decoded_body)
                    ssn=body['ssn']
                    user=User.objects.get(ssn=ssn)
                    staying=Staying.objects.get(owner=user)
                    staying.confirm=True
                    Staying.objects.get(owner=user).delete()
                    staying.save() 
                    return JsonResponse({'result':'true'})
                except:
                 	return JsonResponse({'result':'false'})
@csrf_exempt
def confirm_moving(request):
	if request.method == 'POST':
                try:
                    decoded_body=request.body.decode('utf-8')
                    body=json.loads(decoded_body)
                    print(decoded_body)
                    ssn=body['ssn']
                    user=User.objects.get(ssn=ssn)
                    moving=Moving.objects.get(owner=user)
                    moving.confirm=True
                    Moving.objects.get(owner=user).delete()
                    moving.save()
                    return JsonResponse({'result':'true'})
                except:
                    return JsonResponse({'result':'false'})

def any_holiday():
	today=date.today()
	tomorrow=today+timedelta(days=1)
	print("rrrrrrrrrrrrrrrrrrr")
	print(tomorrow)
	try:
		is_holiday=Holiday.objects.get(date=tomorrow)
		passports=PassPort.objects.filter(date=tomorrow)
		movings=Moving.objects.filter(date=tomorrow)
		stayings=Staying.objects.filter(date=tomorrow)
		print("111111111")
		fill_passport(passports,tomorrow)
		fill_moving(movings,tomorrow)
		fill_staying(stayings,tomorrow)
		print("222222222222")
	except:
		pass
     
        
#schedule.every(1).hours.do(any_holiday)
#while True:
#	schedule.run_pending()
#	time.sleep(1)

def fill_passport(lt,tomorrow):
    for x in lt:
        i=1
        b=True
        while b:
            day=tomorrow+timedelta(days=i)
            try:
                is_holiday=Holiday.objects.get(date=day)
                print(is_holiday)
                i=i+1
            except:
                count=PassPort.objects.filter(date=day).count()
                if count<50 :
                    x.date=day
                    x.confirm=False
                    b=False
                    PassPort.objects.get(owner=x.owner).delete()
                    x.save()
                else:
                    i=i+1

def fill_moving(lt,tomorrow):
	for x in lt:
		i=1
		b=True
		while b:
			day=tomorrow+timedelta(days=i)
			try:
				is_holiday=Holiday.objects.get(date=day)
				i=i+1
			except:
				count=Moving.objects.filter(date=day).count()
				if count<50 :
					x.date=day
					x.confirm=False
					b=False
					Moving.objects.get(owner=x.owner).delete()
					x.save()
				else:
					i=i+1

def fill_staying(lt,tomorrow):
	for x in lt:
		i=1
		b=True
		while b:
			day=tomorrow+timedelta(days=i)
			try:
				is_holiday=Holiday.objects.get(date=day)
				i=i+1
			except:
				count=Staying.objects.filter(date=day).count()
				if count<50 :
					x.date=day
					x.confirm=False
					b=False
					Staying.objects.get(owner=x.owner).delete()
					x.save()
				else:
					i=i+1


def job():
	print('--------------------')
	today=date.today()
	PassPort.objects.filter(date=today).delete()
	Moving.objects.filter(date=today).delete()
	Staying.objects.filter(date=today).delete()

schedule.every().day.at("01:29").do(job)
#while True:
schedule.run_pending()
time.sleep(1)



@csrf_exempt
def paper(request):
	if request.method == 'POST':
                decoded_body=request.body.decode('utf-8')
                body=json.loads(decoded_body)
                print(decoded_body)
                type1=body['type']
                try:
                    if type1 == 1:
                    	paper=PaperPassport.objects.all()
                    elif type1 == 2:
                        paper=PaperMoving.objects.all()
                    elif type1 == 3:
                        paper=PaperStaying.objects.all()
                    data=''
                    for x in paper:
                        data=data+'\n'+x.papers
                    
                    return JsonResponse({'result':'true','data':data})
                   
                except:
                    return JsonResponse({'result':'false'})


