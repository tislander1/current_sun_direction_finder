import time
import math as m

def calculate_sun_direction(longitude, latitude, now):
    '''Returns three tuples.
        Tuple 1: (Right ascension, Declination) of the sun in degrees.
        Tuple 2: (Altitude, Azimuth) of the sun,
        Tuple 3: A unit vector (East, North, Up) pointing at the sun.

        References:
        https://en.wikipedia.org/wiki/Position_of_the_Sun
        http://www.stargazing.net/kepler/altaz.html        
    '''

    # https://en.wikipedia.org/wiki/Position_of_the_Sun

    #from calendar import timegm
    y2k = 946684800 #timegm(time.strptime("1 Jan 00", "%d %b %y"))
    
    n = (now - y2k)/(24*60*60)          # days_since_y2k
    L = 280.460 + 0.9856474 * n         #mean longitude of sun, deg
    g = 357.528 + 0.9856003 * n         #mean anomaly of sun, deg
    lam = L + 1.915*m.sin(g*m.pi/180) + 0.020*m.sin(2*g*m.pi/180) #ecliptic longitude of sun, deg
    beta = 0 #ecliptic latitude of sun never exceeds 0.00033 deg
    R = 1.00014 - 0.01671*m.cos(g*m.pi/180) - 0.00014*m.cos(2*g*m.pi/180) #distance of earth from sun
    eps = 23.439 - 0.0000004*n                          #approx obliquity of the ecliptic
    RA = m.atan(m.cos(eps*m.pi/180)*m.tan(lam*m.pi/180))  #right ascension
    DEC = m.asin(m.sin(eps*m.pi/180)*m.sin(lam*m.pi/180)) #declination

    lat = latitude * m.pi/180
    lon = longitude * m.pi/180

    #http://www.stargazing.net/kepler/altaz.html

    now_gw = time.gmtime(now)   #greenwich time of now
    UT =  now_gw.tm_hour + (now_gw.tm_min + now_gw.tm_sec/60.0)/60.0 #universal time in decimal hours
    LST = (100.46 + 0.985647 * n + longitude + 15.0 * UT) % 360.0 #local sidereal time (deg)
    HA = LST*(m.pi/180) - RA                                            #hour angle (rad)
    sin_altitude = m.sin(DEC)*m.sin(lat) + m.cos(DEC)*m.cos(lat)*m.cos(HA) #sine of altitude
    ALT = m.asin(sin_altitude)                                          #altitude (rad)

    cos_AZ = (m.sin(DEC) - m.sin(ALT)*m.sin(lat)) / (m.cos(ALT)*m.cos(lat))
    AZ = m.acos(cos_AZ)
    if m.sin(HA)<0:
        AZ = AZ
    else:
        AZ = 2*m.pi - AZ
    k_east = m.cos(ALT)*m.sin(AZ)
    k_north = m.cos(ALT)*m.cos(AZ)
    k_up = m.sin(ALT)

    return (((180/m.pi)*RA, (180/m.pi)*DEC),
            ((180/m.pi)*ALT, (180/m.pi)*AZ),
            (k_east, k_north, k_up))
    # (Right Ascension, Dec) of sun,
    # (Altitude, Azimuth) of sun,
    # Cartesian unit vector (east, north, up) pointing to sun
   

longitude_E = -104.990302
latitude_N = 39.739212
(RA_DEC, ALT_AZ, E_N_U) =calculate_sun_direction(longitude_E, latitude_N, time.time())
print( "(Right ascension, Declination) in degrees:", RA_DEC )
print( "(Altitude, Azimuth) in degrees:", ALT_AZ )
print( "(East, North, Up) unit vector:", E_N_U )