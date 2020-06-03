'''
    Note:
        - This is the printGeo.py script updated for the newest version
        of MaxMind's database format.
'''
import geoip2.database

gi = geoip2.database.Reader("/opt/GeoIP/GeoLite2-City.mmdb")


def printRecord(tgt):
    rec = gi.city(tgt)
    city = rec.city.name
    region = rec.subdivisions.most_specific.name
    country = rec.country.name
    long = rec.location.longitude
    lat = rec.location.latitude

    print("[*] Target: " + tgt + " Geo-located. ")
    print("[+] " + str(city) + ", " + str(region) + ", " + str(country))
    print("[+] Latitude: " + str(lat) + ", Longitude: " + str(long))


tgt = "173.255.226.98"
printRecord(tgt)
