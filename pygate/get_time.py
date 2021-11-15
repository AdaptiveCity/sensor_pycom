import time
import socket
import ssl

def datetime_to_tuple(datetime_now):
    # E.g. 'Date: Thu, 11 Nov 2021 16:38:25 GMT'
	month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	split_datetime = datetime_now.strip().split(' ')
    # ['Thu,', '11', 'Nov', '2021', '16:38:25']
	print(split_datetime)
	day = int(split_datetime[1])
	month = month_name.index(split_datetime[2]) + 1 # Note javascript uses 0..11 for month, Pycom RTC uses 1..12
	year = int(split_datetime[3])
	split_time = split_datetime[4].split(':')
	return (year, month, day, int(split_time[0]), int(split_time[1]), int(split_time[2]))

def get_current_time():
    s = socket.socket()
    #s = ssl.wrap_socket(s)

    host = 'cdbb.uk'
    addr = socket.getaddrinfo(host,443)[0][-1]
    s.connect(addr)
    print('socket connected')
    # it is possible to attach additional HTTP headers in the line below, but note to always close with \r\n\r\n
    httpreq = 'GET / HTTP/1.1 \r\nHOST: '+ host + '\r\nConnection: close \r\n\r\n'
    print('http request: \n', httpreq)
    s.send(httpreq)

    time.sleep(1)

    rec_bytes = s.recv(10000)

    response_str = str(rec_bytes)
    datetime_now = (response_str.strip().split('Date:'))[1].split('GMT')[0]
    
    s.close()

    return(datetime_to_tuple(datetime_now))
