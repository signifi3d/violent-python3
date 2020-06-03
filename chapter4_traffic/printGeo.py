'''
    Note:
        - GeoIP is deprecated now by GeoIP2. While MaxMind stlil provides
        its free City database, it has updated its system and makes use of
        a different file format. I have left the deprecated examples
        making use of pygeoip since it's still operable if you have the
        correct files, but I have also included updated versions of every
        example that makes use of it. Updated examples for any particular
        script can be found in a corresponding [scriptName]-updated.py file.
        You can go to https://dev.maxmind.com/geoip/geoip2/geolite2 to find
        out more about obtaining a newer style database.
    Changes:
        - region_name key to the gi dictionary changed to region_code to 
        work with updated pygeoip library.
'''
import pygeoip

gi = pygeoip.GeoIP("/opt/GeoIP/Geo.dat")


def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']

    print("[*] Target: " + tgt + " Geo-located. ")
    print("[+] " + str(city) + ", " + str(region) + ", "  + str(country))
    print("[+] Latitude: " + str(lat) + ", Longitude: " + str(long))


tgt = "173.255.226.98"
printRecord(tgt)
