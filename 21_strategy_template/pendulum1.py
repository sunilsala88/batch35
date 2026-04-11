#pip install pendulum

import pendulum as dt
time_zone = 'Asia/Kolkata'
# time_zone='America/New_York'
ct= dt.now(time_zone)
print(ct)

start_hour,start_min=9,15
#end time
end_hour,end_min=15,15


start_time=dt.datetime(ct.year,ct.month,ct.day,start_hour,start_min,1,tz=time_zone)
print(start_time)

end_time=dt.datetime(ct.year,ct.month,ct.day,end_hour,end_min,0,tz=time_zone)
print(end_time)

while True:
    ct= dt.now(time_zone)
    print(ct)
    if ct>start_time and ct<end_time:
        print("we are in trading hours")
        #run your strategy code here
    else:
        print("we are not in trading hours")