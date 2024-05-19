import json


class confMan:
    def __init__(self):
        self.attendees = self.load_attendees()

    def load_attendees(self):
        attendees_data = self.load_attendees_data()
        attendees = []
        for nr, info in attendees_data.items():
            attendee_info = [info["name"], info["company"], info["state"], info["email"], nr]
            attendees.append(attendee_info)

        attendees_2 = []
        for nr in attendees:
            attendee = self.getAttendee(nr[0], attendees)
            attendees_2.append(attendee)
        return attendees_2

    def load_attendees_data(self):
        filename = open('conferenceAttendees.json', 'r', encoding='utf-8')
        data = json.load(filename)
        return data

    def create_attendee(self, attendee_into):
        name, company, state, email, nr = attendee_into
        attendee = Attendee(name, company, state, email, nr)
        return attendee

    def getAttendee(self, name, attendees):
        for attendee_into in attendees:
            attendee = self.create_attendee(attendee_into)
            if attendee.name == name:
                return attendee
        return None

    def makeAttendee(self, name, company, state, email, nr):
        attendee_name = name
        attendee_company = company
        attendee_state = state
        attendee_email = email
        attendee_nr = nr
        for attendee in self.attendees:
            if attendee.name == name and attendee.nr == nr:
                print("Attendee already exists!")
                return
        attendee = Attendee(attendee_name, attendee_company, attendee_state, attendee_email, attendee_nr)
        self.attendees.append(attendee)

    def findAttendeeByName(self, name, nr):
        for attendee in self.attendees:
            if attendee.name == name and attendee.nr == nr:
                info = self.printAttendeeInfo(attendee)
                return attendee
        return None

    def findAttendeesByState(self, state):
        attendees_by_name = []
        for attendee in self.attendees:
            if attendee.state == state:
                attendees_by_name.append(attendee.name)

        attendee_names = ''
        for name in attendees_by_name:
            if attendee_names == '':
                attendee_names = attendee_names + name
            else:
                attendee_names = attendee_names + ', '
                attendee_names = attendee_names + name

        print(attendee_names)

    def printAttendeeInfo(self, attendee):
        print(attendee.name)
        print(attendee.company)
        print(attendee.email)
        print(attendee.state)
        print(attendee.nr)

    def delAttendee(self, name, nr):
        for attendee in self.attendees:
            if attendee.name == name and attendee.nr == nr:
                self.attendees.remove(attendee)
                break

    def updateConference(self):
        attendees = []
        for attendee in self.attendees:
            attendee_dict = {}
            attendee_dict['name'] = attendee.name
            attendee_dict['company'] = attendee.company
            attendee_dict['state'] = attendee.state
            attendee_dict['email'] = attendee.email
            attendee_dict['nr'] = attendee.nr
            attendees.append(attendee_dict)

        with open('conferencedAttendees1.json', 'w', encoding='utf-8') as outfile:
            json.dump(attendees, outfile, indent=4, separators=(',', ': '))


class Attendee:
    def __init__(self, name, company, state, email, nr):
        self.name = name
        self.company = company
        self.state = state
        self.email = email
        self.nr = nr

    def displayInfo(self):
        print(self.name)
        print(self.company)
        print(self.email)
        print(self.state)
        print(self.nr)


def main():
        conference = confMan()
        conference.makeAttendee("Carson", "Philadelphia Eagles", "PA, USA", "wentz@philaeagles.com", 3)
        conference.makeAttendee("Carson", "Philadelphia Eagles", "PA, USA", "wentz@philaeagles.com", 3)
        conference.makeAttendee("Liza", "Philadelphia Eagles", "PA, USA", "liza@philaeagles.com", 4)
        byName = conference.findAttendeeByName("Carson", 3)
        print(byName.displayInfo())
        conference.findAttendeesByState("PA, USA")
        conference.updateConference()
        conference.delAttendee("Carson", 3)


main()
