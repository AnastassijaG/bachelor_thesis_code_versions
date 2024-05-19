"""BAD CODE"""
import json

class ConferenceManager:
    def __init__(self):
        self.attendees = []
        filename = open('conferenceAttendees.json', 'r')
        json_string = filename.read()
        self.json_object = json.loads(json_string)
        for k in self.json_object.keys():
            attendee_data = self.json_object[k]
            attendee = {
                "name": attendee_data["name"],
                "company": attendee_data["company"],
                "state": attendee_data["state"],
                "email": k
            }
            self.attendees.append(attendee)
        filename.close()

    def update_conference(self):
        data = []
        for attendee in self.attendees:
            data.append(attendee)
        with open('conferencedAttendees1.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

def main():
    conference = ConferenceManager()
    conference.attendees.append({
        "name": "Carson",
        "company": "Philadelphia Eagles",
        "state": "PA, USA",
        "email": "wentz@philaeagles.com"
    })
    for attendee in conference.attendees:
        if attendee["name"] == "Carson":
            print(attendee["company"])
            print(attendee["name"])
            print(attendee["state"])
            print(attendee["email"])
            print("{0}  {1} {2} {3}".format(attendee["name"], attendee["company"], attendee["state"], attendee["email"]))
            break
    conference.update_conference()
    for attendee in conference.attendees:
        if attendee["state"] == "PA, USA":
            print(attendee["name"])

main()