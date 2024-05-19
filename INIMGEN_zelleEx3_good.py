import json as json


class ConferenceManager:
    # Class for all conference attendees
    def __init__(self):
        self.attendees = []
        self.json_object = json.loads(open('conferenceAttendees.json', 'r').read())
        for object in self.json_object.keys():
            attendee = Attendee(self.json_object[object]["name"], self.json_object[object]["company"],
                                self.json_object[object]["state"], self.json_object[object]["email"])
            self.attendees.append(attendee)

    def getAttendee(self, name):
        for attendee in self.attendees:
            if attendee.get_name() == name:
                return attendee

    # Returns a list of all attendees of the conference
    def findByState(self, state):
        return [attendee.get_name() for attendee in self.attendees if attendee.get_state() == state]

    def addAttendee(self, name, company, state, email):
        attendee = Attendee(name, company, state, email)
        self.attendees.append(attendee)

    # Updates the conference attendees file after adding and deleting them
    def updateConference(self):
        data = [vars(attendee) for attendee in self.attendees]
        with open('conferencedAttendees1.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def deleteAttendee(self, name):
        for attendee in self.attendees:
            if attendee.get_name() == name:
                self.attendees.remove(attendee)
                break


class Attendee:
    # Attendee of the Conference
    def __init__(self, name, company, state, email):
        self.name = name
        self.company = company
        self.state = state
        self.email = email

    # methods for returning name and state of an attendee to abide by the Larmani GRASP pattern
    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

    # Displays all information of an attendee
    def displayInfo(self):
        print("{0}  {1} {2} {3}".format(self.name, self.company, self.state, self.email))


def main():
    conference = ConferenceManager()
    sean = conference.getAttendee("John Doe")
    print(sean.get_name())
    sean.displayInfo()
    conference.addAttendee("Carson", "Philadelphia Eagles", "PA, USA", "wentz@philaeagles.com")
    conference.addAttendee("Liza", "Philadelphia Eagles", "PA, USA", "liz@philaeagles.com")
    list = conference.findByState("PA, USA")
    print(list)
    conference.deleteAttendee("Liza")
    conference.updateConference()

main()