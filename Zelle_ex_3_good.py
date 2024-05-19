"""GOOD CODE"""

import json

class ConferenceManager:
    def __init__(self, attendees_file='conferenceAttendees.json'):
        self.attendees = []
        self.attendees_file = attendees_file
        self.load_attendees()

    def load_attendees(self):
        with open(self.attendees_file, 'r') as file:
            data = json.load(file)
        self.attendees = [Attendee(attendee_data["name"], attendee_data["company"], attendee_data["state"], email)
                          for email, attendee_data in data.items()]

    def get_attendee(self, name):
        for attendee in self.attendees:
            if attendee.get_name() == name:
                return attendee

    def find_attendees_by_state(self, state):
        return [attendee for attendee in self.attendees if attendee.get_state() == state]

    def add_attendee(self, name, company, state, email):
        attendee = Attendee(name, company, state, email)
        self.attendees.append(attendee)

    def remove_attendee(self, name):
        self.attendees = [attendee for attendee in self.attendees if attendee.get_name() != name]

    def update_conference(self, output_file='conferencedAttendees1.json'):
        data = [vars(attendee) for attendee in self.attendees]
        with open(output_file, 'w') as outfile:
            json.dump(data, outfile, indent=4)

class Attendee:
    def __init__(self, name, company, state, email):
        self.name = name
        self.company = company
        self.state = state
        self.email = email

    def get_name(self):
        return self.name

    def get_company(self):
        return self.company

    def get_state(self):
        return self.state

    def get_email(self):
        return self.email

    def display_info(self):
        print("{0}  {1} {2} {3}".format(self.name, self.company, self.state, self.email))


def main():
    conference = ConferenceManager()
    conference.add_attendee("Carson", "Philadelphia Eagles", "PA, USA", "wentz@philaeagles.com")
    sean = conference.get_attendee("Carson")
    if sean:
        print(sean.get_company())
        print(sean.get_name())
        print(sean.get_state())
        print(sean.get_email())
        sean.display_info()
    else:
        print("Attendee not found.")
    conference.update_conference()
    state_attendees = conference.find_attendees_by_state("PA, USA")
    for attendee in state_attendees:
        print(attendee.get_name())

main()