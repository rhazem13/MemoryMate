from events.Event import Event


class CaregiverAgendaEvent(Event):

    def getData(self, sender_id, reciever_id, args=None):
        data = dict()
        data['user_id'] = reciever_id
        data['title'] = "لقد نسيت أخذ الدواء"
        data['type'] = "important"
        data['body'] = {
            "content": "لقد نسيت اخذ الدواء",
            "agenda_id": args['agenda_id']
        }
